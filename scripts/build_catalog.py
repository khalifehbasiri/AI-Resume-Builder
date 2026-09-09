"""Convert published source snapshots into the skill's offline reference catalog."""

import argparse
import csv
import hashlib
import json
import re
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
SHEET = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRg7oze-BnheKtSvQH2ApktuRYyWaXOuvE9hgke4puccxX4Gs5I9-xAfxaKgRoYxYh6W1DlyqSA9e2c/pubhtml"


def youtube_url(value):
    parsed = urlparse(value.strip())
    if parsed.hostname in {"www.google.com", "google.com"}:
        params = parse_qs(parsed.query)
        return youtube_url((params.get("q") or params.get("url") or [""])[0])
    video_id = ""
    if parsed.hostname == "youtu.be":
        video_id = parsed.path.strip("/")
    elif parsed.hostname in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
        video_id = parse_qs(parsed.query).get("v", [""])[0]
    return f"https://www.youtube.com/watch?v={video_id}" if re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id) else None


class SheetParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.row = None
        self.cell = None

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.row = []
        elif tag == "td" and self.row is not None:
            self.cell = {"text": "", "links": []}
        elif tag == "a" and self.cell is not None:
            self.cell["links"].append(dict(attrs).get("href", ""))
        elif tag == "br" and self.cell is not None:
            self.cell["text"] += "\n"

    def handle_data(self, data):
        if self.cell is not None:
            self.cell["text"] += data

    def handle_endtag(self, tag):
        if tag == "td" and self.cell is not None:
            self.row.append(self.cell)
            self.cell = None
        elif tag == "tr" and self.row is not None:
            if self.row:
                self.rows.append(self.row)
            self.row = None


def build(episodes_csv, qualifications_csv, html_path, snapshot_date):
    date.fromisoformat(snapshot_date)
    parser = SheetParser()
    parser.feed(html_path.read_text(encoding="utf-8"))
    if not parser.rows:
        raise ValueError("HTML has no table rows; download pubhtml/sheet, not the enclosing pubhtml page")
    link_map = {}
    for row in parser.rows:
        if len(row) >= 3:
            key = (row[0]["text"].strip(), row[1]["text"].strip(), row[2]["text"].strip())
            links = [youtube_url(link) for link in row[2]["links"]]
            resolved = next((link for link in links if link), None)
            if resolved:
                link_map[key] = resolved
    episodes = []
    with episodes_csv.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            title, episode, label = (row.get(key, "").strip() for key in ("Job Title", "Episode", "Link to Episode"))
            if not title:
                continue
            if not episode.isdigit():
                raise ValueError(f"Unexpected episode number for {title}: {episode}")
            url = youtube_url(label) or link_map.get((title, episode, label))
            episodes.append({"job_title": title, "episode": int(episode), "url": url, "link_label": label, "release_date": row.get("Release Date", "").strip(), "good_resume": row.get("Good Resume", "").strip(), "content_status": "indexed_only"})
    qualifications = []
    with qualifications_csv.open(encoding="utf-8-sig", newline="") as handle:
        for raw in csv.DictReader(handle):
            row = {key.strip(): value.strip().replace("\r\n", "\n").replace("\r", "\n") for key, value in raw.items() if key}
            if row.get("Job Title"):
                qualifications.append({"job_title": row["Job Title"], "qualifications": row.get("Quilfications", row.get("Qualifications", "")), "last_updated": row.get("Last Updated", "")})
    return {"snapshot_date": snapshot_date, "market": "United States; verify role, seniority, and local market", "sources": [SHEET + "#gid=1421544187", SHEET + "#gid=0"], "input_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (episodes_csv, qualifications_csv, html_path)}, "episodes": episodes, "qualifications": qualifications}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episodes", type=Path, required=True)
    parser.add_argument("--qualifications", type=Path, required=True)
    parser.add_argument("--html", type=Path, required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--output", type=Path, default=ROOT / "career-data/reference-catalog.json")
    args = parser.parse_args()
    catalog = build(args.episodes, args.qualifications, args.html, args.date)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(catalog, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"episodes": len(catalog["episodes"]), "qualifications": len(catalog["qualifications"]), "resolved_urls": sum(bool(r["url"]) for r in catalog["episodes"])}))


if __name__ == "__main__":
    main()
