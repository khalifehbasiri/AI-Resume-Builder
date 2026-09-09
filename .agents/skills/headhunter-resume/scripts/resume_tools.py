"""Offline catalog lookup and structural evidence audits. Python 3.10+, stdlib only."""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


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

    for rid, req in tables["requirements"].items():
        require_text(req, "text", rid)
        if req.get("priority") not in ("required", "preferred"):
            errors.append(f"{rid}.priority is invalid")
        status = req.get("assessment")
        if status not in ("supported", "partial", "unknown", "absent"):
            errors.append(f"{rid}.assessment is invalid")
        refs = references(req, "claim_ids", tables["claims"], rid)
        if status == "supported":
            if not refs or any(tables["claims"].get(ref, {}).get("status") != "confirmed" or tables["claims"].get(ref, {}).get("ownership") == "unknown" for ref in refs):
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
