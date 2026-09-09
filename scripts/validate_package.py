"""Validate portable skill resources and local Markdown links without dependencies."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents/skills/headhunter-resume"


def main():
    errors = []
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    if not text.startswith("---\nname: headhunter-resume\ndescription: "):
        errors.append("Skill name/description frontmatter is invalid")
    markdown_files = list(SKILL.rglob("*.md")) + list((ROOT / "docs").rglob("*.md")) + list(ROOT.glob("*.md"))
    for path in markdown_files:
        for dest in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if dest.startswith(("https://", "http://", "#")):
                continue
            if not (path.parent / dest.split("#")[0]).exists():
                errors.append(f"Broken local link: {path.relative_to(ROOT)} -> {dest}")
    for name in ("LICENSE", "README.md", "CONTRIBUTING.md", ".agents/skills/headhunter-resume/agents/openai.yaml", ".agents/skills/headhunter-resume/assets/inventory.json"):
        if not (ROOT / name).is_file():
            errors.append(f"Required release file missing: {name}")
    if (SKILL / "references/catalog.json").exists():
        errors.append("Third-party catalog must not be bundled in the public skill")
    if not (SKILL / "LICENSE").is_file() or (SKILL / "LICENSE").read_text(encoding="utf-8") != (ROOT / "LICENSE").read_text(encoding="utf-8"):
        errors.append("The standalone skill must include the project license")
    for path in SKILL.rglob("*"):
        if path.is_file() and path.suffix in {".py", ".md", ".json", ".yaml"}:
            content = path.read_text(encoding="utf-8")
            if "C:\\Users\\" in content or "C:/Users/" in content:
                errors.append(f"Nonportable local path: {path.relative_to(ROOT)}")
    result = {"ok": not errors, "errors": errors, "markdown_files_checked": len(markdown_files), "catalog_bundled": False}
    print(json.dumps(result, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
