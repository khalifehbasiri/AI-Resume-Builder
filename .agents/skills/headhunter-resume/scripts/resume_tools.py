"""Offline catalog lookup and structural evidence audits. Python 3.10+, stdlib only."""

import argparse
import json
import re
import sys
from collections import deque
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def public_url(value):
    if not nonempty(value):
        return False
    try:
        parsed = urlsplit(value)
        return parsed.scheme in ("http", "https") and bool(parsed.hostname) and parsed.username is None and parsed.password is None
    except ValueError:
        return False


def superseded_claim_ids(data):
    """Confirmed corrections with known ownership retire prior evidence IDs."""
    return {ref for claim in data["claims"]
            if claim["status"] == "confirmed" and claim["ownership"] != "unknown"
            for ref in claim.get("supersedes", [])}


def validate_inventory(data):
    errors = []
    if not isinstance(data, dict):
        return ["Inventory must be an object"]
    if type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        errors.append("schema_version must be 1")
    if not nonempty(data.get("candidate_id")):
        errors.append("candidate_id must be a nonempty string")
    target = data.get("target")
    if not isinstance(target, dict):
        errors.append("target must be an object")
    else:
        if target.get("mode") not in ("scratch", "improve", "tailor", "base", "review"):
            errors.append("target.mode is invalid")
        for key in ("role", "seniority", "market"):
            if not isinstance(target.get(key), str):
                errors.append(f"target.{key} must be a string")

    tables = {}
    for group in ("sources", "experiences", "claims", "requirements"):
        rows = data.get(group)
        tables[group] = {}
        if not isinstance(rows, list):
            errors.append(f"{group} must be an array")
            continue
        for index, row in enumerate(rows):
            if not isinstance(row, dict) or not nonempty(row.get("id")):
                errors.append(f"{group}[{index}] must have a nonempty string id")
                continue
            if row["id"] in tables[group]:
                errors.append(f"Duplicate {group} id: {row['id']}")
            tables[group][row["id"]] = row

    def require_text(row, field, context):
        if not nonempty(row.get(field)):
            errors.append(f"{context}.{field} must be a nonempty string")

    def references(row, field, table, context):
        refs = row.get(field)
        if not isinstance(refs, list) or not all(nonempty(r) for r in refs):
            errors.append(f"{context}.{field} must be an array of IDs")
            return []
        for ref in refs:
            if ref not in table:
                errors.append(f"{context}.{field}: unknown reference {ref}")
        return refs

    if "preferences" in data:
        prefs = data["preferences"]
        if not isinstance(prefs, dict):
            errors.append("preferences must be an object")
        else:
            if "page_target" in prefs and (type(prefs["page_target"]) is not int or prefs["page_target"] < 1):
                errors.append("preferences.page_target must be a positive integer")
            if "template" in prefs:
                require_text(prefs, "template", "preferences")
            if "required_experience_ids" in prefs:
                references(prefs, "required_experience_ids", tables["experiences"], "preferences")
            if "excluded_keywords" in prefs and (not isinstance(prefs["excluded_keywords"], list) or not all(nonempty(k) for k in prefs["excluded_keywords"])):
                errors.append("preferences.excluded_keywords must be an array of strings")

    for sid, source in tables["sources"].items():
        for field in ("kind", "locator", "accessed", "note"):
            require_text(source, field, sid)
        try:
            date.fromisoformat(source.get("accessed", ""))
        except (ValueError, TypeError):
            errors.append(f"{sid}.accessed must be YYYY-MM-DD")

    for eid, experience in tables["experiences"].items():
        require_text(experience, "kind", eid)
        for field in ("title", "organization", "description"):
            if field not in experience or (experience[field] is not None and not nonempty(experience[field])):
                errors.append(f"{eid}.{field} must be a nonempty string or null while unknown")
        start, end = experience.get("start"), experience.get("end")
        valid_dates = True
        for field, value in (("start", start), ("end", end)):
            if value is None or (field == "end" and value == "present"):
                continue
            if not isinstance(value, str) or not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", value):
                errors.append(f"{eid}.{field} must be YYYY-MM, null, or present for end")
                valid_dates = False
        if valid_dates and start and end and end != "present" and start > end:
            errors.append(f"{eid}: end precedes start")
        if "employer_group" in experience and experience["employer_group"] is not None and not nonempty(experience["employer_group"]):
            errors.append(f"{eid}.employer_group must be a nonempty string or null")
        if "public_links" in experience:
            links = experience["public_links"]
            if not isinstance(links, list):
                errors.append(f"{eid}.public_links must be an array")
            else:
                for index, link in enumerate(links):
                    context = f"{eid}.public_links[{index}]"
                    if not isinstance(link, dict):
                        errors.append(f"{context} must be an object")
                        continue
                    if link.get("kind") not in ("github", "demo", "product", "other"):
                        errors.append(f"{context}.kind is invalid")
                    require_text(link, "label", context)
                    if not public_url(link.get("url")):
                        errors.append(f"{context}.url must be an HTTP(S) URL without embedded credentials")

    correction_graph = {cid: [] for cid in tables["claims"]}
    for cid, claim in tables["claims"].items():
        require_text(claim, "text", cid)
        if claim.get("status") not in ("confirmed", "unconfirmed", "conflict", "rejected"):
            errors.append(f"{cid}.status is invalid")
        if claim.get("ownership") not in ("personal", "team", "unknown"):
            errors.append(f"{cid}.ownership is invalid")
        eid = claim.get("experience_id")
        if eid is not None and (not isinstance(eid, str) or eid not in tables["experiences"]):
            errors.append(f"{cid}.experience_id is unknown")
        refs = references(claim, "source_ids", tables["sources"], cid)
        if claim.get("status") == "confirmed":
            if not refs:
                errors.append(f"{cid}: confirmed claim needs a source")
            require_text(claim, "confirmation", cid)
        if not isinstance(claim.get("keywords"), list) or not all(nonempty(k) for k in claim.get("keywords", [])):
            errors.append(f"{cid}.keywords must be an array of strings")
        if "delivery_status" in claim and claim["delivery_status"] not in ("planned", "prototype", "implemented", "released", "production"):
            errors.append(f"{cid}.delivery_status is invalid")
        if "metric" in claim:
            metric = claim["metric"]
            if not isinstance(metric, dict):
                errors.append(f"{cid}.metric must be an object")
            else:
                if metric.get("kind") not in ("scope", "outcome", "adoption"):
                    errors.append(f"{cid}.metric.kind is invalid")
                if metric.get("qualifier") not in ("exact", "approximate", "minimum", "range"):
                    errors.append(f"{cid}.metric.qualifier is invalid")
                for field in ("value", "population", "attribution"):
                    require_text(metric, field, f"{cid}.metric")
                for field in ("baseline", "outcome", "window"):
                    if field not in metric or (metric[field] is not None and not nonempty(metric[field])):
                        errors.append(f"{cid}.metric.{field} must be a nonempty string or null")
        if "supersedes" in claim:
            refs = references(claim, "supersedes", tables["claims"], cid)
            correction_graph[cid] = [ref for ref in refs if ref in tables["claims"]]
            if cid in refs:
                errors.append(f"{cid}.supersedes cannot reference itself")
            for ref in correction_graph[cid]:
                if claim.get("experience_id") != tables["claims"][ref].get("experience_id"):
                    errors.append(f"{cid}.supersedes: {ref} belongs to a different experience")

    # Kahn's algorithm avoids recursion depth limits in a long correction history.
    indegree = dict.fromkeys(correction_graph, 0)
    for refs in correction_graph.values():
        for ref in refs:
            indegree[ref] += 1
    ready = deque(cid for cid, degree in indegree.items() if degree == 0)
    visited = 0
    while ready:
        cid = ready.popleft()
        visited += 1
        for ref in correction_graph[cid]:
            indegree[ref] -= 1
            if indegree[ref] == 0:
                ready.append(ref)
    if visited != len(correction_graph):
        errors.append("Claim supersedes references contain a cycle")

    superseded = {ref for cid, refs in correction_graph.items()
                  if tables["claims"][cid].get("status") == "confirmed" and tables["claims"][cid].get("ownership") in ("personal", "team")
                  for ref in refs}

    for rid, req in tables["requirements"].items():
        require_text(req, "text", rid)
        if req.get("priority") not in ("required", "preferred"):
            errors.append(f"{rid}.priority is invalid")
        status = req.get("assessment")
        if status not in ("supported", "partial", "unknown", "absent"):
            errors.append(f"{rid}.assessment is invalid")
        refs = references(req, "claim_ids", tables["claims"], rid)
        if status == "supported":
            if not refs or any(ref in superseded or tables["claims"].get(ref, {}).get("status") != "confirmed" or tables["claims"].get(ref, {}).get("ownership") == "unknown" for ref in refs):
                errors.append(f"{rid}: supported requirement needs confirmed claims with known ownership")

    for field in ("open_questions", "notes"):
        if not isinstance(data.get(field), list) or not all(isinstance(x, str) for x in data.get(field, [])):
            errors.append(f"{field} must be an array of strings")
    return errors


def audit_draft(inventory, draft):
    errors = validate_inventory(inventory)
    if errors:
        return errors
    if not isinstance(draft, dict) or not isinstance(draft.get("claims"), list) or not draft["claims"]:
        return ["Draft must contain a nonempty claims array"]
    claims = {c["id"]: c for c in inventory["claims"]}
    superseded = superseded_claim_ids(inventory)
    for index, row in enumerate(draft["claims"]):
        if not isinstance(row, dict) or not nonempty(row.get("text")):
            errors.append(f"draft[{index}]: text is required")
            continue
        refs = row.get("evidence_ids")
        if not isinstance(refs, list) or not refs or not all(nonempty(ref) for ref in refs):
            errors.append(f"draft[{index}]: nonempty evidence_ids required")
            continue
        for ref in refs:
            claim = claims.get(ref)
            if claim is None:
                errors.append(f"draft[{index}]: unknown evidence {ref}")
            elif claim["status"] != "confirmed" or claim["ownership"] == "unknown":
                errors.append(f"draft[{index}]: {ref} is not confirmed with known ownership")
            elif ref in superseded:
                errors.append(f"draft[{index}]: {ref} was superseded by a confirmed correction")
    return errors


def search_catalog(query, kind, limit=5, catalog_path=None):
    if not query.strip() or limit < 1:
        raise ValueError("Query must be nonempty and limit positive")
    if catalog_path is None:
        raise ValueError("No catalog bundled. Pass --catalog with a local reference catalog; see the repository's docs/MAINTENANCE.md.")
    catalog = load_json(catalog_path)
    terms = query.casefold().split()
    results = []
    for row in catalog[kind]:
        haystack = row["job_title"].casefold()
        if all(term in haystack for term in terms):
            results.append(row)
    results.sort(key=lambda r: (r["job_title"].casefold() != query.casefold(), -int(r.get("episode") or 0), r["job_title"].casefold()))
    return {"snapshot_date": catalog["snapshot_date"], "market": catalog["market"], "total_matches": len(results), "results": results[:limit]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate", help="Check inventory structure and references")
    validate.add_argument("inventory")
    audit = sub.add_parser("audit", help="Check draft evidence references; not semantic truth")
    audit.add_argument("inventory")
    audit.add_argument("draft")
    search = sub.add_parser("search", help="Search a user-supplied local job-title catalog")
    search.add_argument("query")
    search.add_argument("--kind", choices=("episodes", "qualifications"), default="episodes")
    search.add_argument("--limit", type=int, default=5)
    search.add_argument("--catalog", type=Path, required=True, help="Local catalog JSON; no third-party catalog is bundled")
    args = parser.parse_args(argv)
    try:
        if args.command == "search":
            result = search_catalog(args.query, args.kind, args.limit, args.catalog)
            code = 0
        else:
            inventory = load_json(args.inventory)
            errors = validate_inventory(inventory) if args.command == "validate" else audit_draft(inventory, load_json(args.draft))
            result = {"ok": not errors, "errors": errors, "scope": "Structural checks only; manually review claim meaning and complete resume coverage."}
            code = 1 if errors else 0
    except (OSError, ValueError, KeyError) as exc:
        result, code = {"ok": False, "errors": [str(exc)]}, 2
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
