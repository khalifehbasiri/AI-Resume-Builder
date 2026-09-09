"""Install an independent copy of the skill; refuse to overwrite an existing install."""

import argparse
import shutil
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / ".agents" / "skills" / "headhunter-resume"


def install(destination):
    destination = Path(destination).expanduser().resolve()
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / SOURCE.name
    if target.exists() or target.is_symlink():
        raise FileExistsError(f"Already exists: {target}. Review the existing installation before updating.")
    shutil.copytree(SOURCE, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "catalog.json"))
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path, default=Path.home() / ".agents" / "skills", help="Parent skills directory; default ~/.agents/skills")
    args = parser.parse_args()
    try:
        print(f"Installed: {install(args.destination)}")
    except (OSError, shutil.Error) as exc:
        parser.exit(1, f"Install failed: {exc}\n")


if __name__ == "__main__":
    main()
