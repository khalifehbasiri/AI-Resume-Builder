# Maintaining the skill

## Layout

`.agents/skills/headhunter-resume` is the portable installable directory. `SKILL.md` contains the workflow and routes to focused references; `assets/inventory.json` is an empty starting template; `scripts/resume_tools.py` provides deterministic offline checks. Repository-level scripts build the source catalog, validate the package, and install a copy. Tests use synthetic data only.

## Optional private source catalog

No copied third-party catalog is distributed. If you have appropriately obtained source snapshots for local use, the importer can prepare a searchable file without changing the installed skill. The interview and resume workflow does not require this step.

The published sources offer two CSV tabs and episode **sheet HTML**, which preserves hyperlinks. The enclosing `pubhtml` page only loads the actual sheet and does not contain the rows. Keep local snapshots under ignored `tmp/research/`.

```text
CSV: https://docs.google.com/spreadsheets/d/e/2PACX-1vRg7oze-BnheKtSvQH2ApktuRYyWaXOuvE9hgke4puccxX4Gs5I9-xAfxaKgRoYxYh6W1DlyqSA9e2c/pub?single=true&output=csv&gid=1421544187
CSV: https://docs.google.com/spreadsheets/d/e/2PACX-1vRg7oze-BnheKtSvQH2ApktuRYyWaXOuvE9hgke4puccxX4Gs5I9-xAfxaKgRoYxYh6W1DlyqSA9e2c/pub?single=true&output=csv&gid=0
HTML: https://docs.google.com/spreadsheets/d/e/2PACX-1vRg7oze-BnheKtSvQH2ApktuRYyWaXOuvE9hgke4puccxX4Gs5I9-xAfxaKgRoYxYh6W1DlyqSA9e2c/pubhtml/sheet?headers=false&gid=1421544187
```

Then run, using the actual snapshot date:

```sh
python scripts/build_catalog.py --episodes tmp/research/episodes.csv --qualifications tmp/research/qualifications.csv --html tmp/research/episodes-sheet.html --date 2026-09-09
python -m unittest discover -s tests -v
python scripts/validate_package.py
```

The default output is `career-data/reference-catalog.json`, excluded from Git. Pass it to `resume_tools.py search` using `--catalog`. Review counts, recovered links, and source labels locally. Date and input SHA-256 hashes are stored in the catalog. Rows whose source links cannot be established remain null. Do not commit the output or copy it into the skill directory. An import does not mean the videos were reviewed. Add a timestamped research note only after inspecting real content.

## Behavioral verification

Run the scenarios in `tests/behavioral-scenarios.md` with the skill in an isolated workspace. Give the evaluator the scenario and minimum inputs, not the expected answer. Review its output for unsupported claims, relevant questions, scope control, and useful delivery. Do not use actual candidate data as a committed fixture.

The optional built-in skill-creator validator checks skill frontmatter and unfinished scaffolds. If available, run its `scripts/quick_validate.py` against the skill folder; it needs PyYAML. Repository checks require no third-party packages.

## Update an installed copy

Keep edits in the repository source of truth. The installer intentionally refuses to overwrite an existing copy. Compare the existing installed folder with the updated skill, preserve any local edits, and replace it deliberately after review. Alternatively, use the repository copy directly in Codex. Do not install two identical skills into the same discovery scope.

## Before pushing

Review the staged file list. Keep candidate data, copied source catalogs, raw captions, original third-party guides, tokens, temporary downloads, and runtime dependencies excluded. This is a public repository: check the full history of any branches you publish, not only their current files. The MIT License applies to original project material, not linked third-party sources.
