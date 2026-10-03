# Maintaining the skill

## Layout

`.agents/skills/headhunter-resume` is the canonical Agent Skills package. `SKILL.md` contains the workflow and routes to focused references; `assets/inventory.json` is an empty starting template; `scripts/resume_tools.py` provides deterministic offline checks. `portable/headhunter-resume-prompt.md` is the generated, single-file provider-neutral edition. Repository-level scripts build that prompt, build an optional source catalog, validate the package, and install a skill copy. Tests use synthetic data only.

## Rebuild the portable prompt

Do not hand-edit `portable/headhunter-resume-prompt.md`. It is assembled from the canonical skill instructions, references, and empty inventory template:

```sh
python scripts/build_portable_prompt.py
python scripts/build_portable_prompt.py --check
```

The prompt deliberately excludes executable Python source and OpenAI-specific UI metadata. It includes the readable bank template, Jake-based LaTeX source, and upstream template license so single-file users can use the same assets. Its compatibility preamble explains how to fall back when an AI host lacks files, browsing, code execution, or rendering. The test suite and package validator fail when the committed prompt is stale.

## Methodology and schema changes

Keep source/adaptation reasons in the skill's `references/methodology.md`, provenance in `references/research.md`, and rights in `THIRD_PARTY_NOTICES.md`. Do not copy personal candidate rules into universal defaults. The page target defaults to one for standard applications; explicitly different deliverables retain their own requirements.

Version-1 inventories remain supported. Optional preferences, public links, grouping, metrics, delivery status, and correction references are documented in `references/evidence.md`. Update validators, tests, the empty inventory, and documentation together when their structure changes. A confirmed correction retires its referenced prior claims from both draft audits and supported requirement mappings.

Keep the upstream Jake MIT notice with the template and in the portable prompt. When copying the template into a standalone resume, preserve its embedded source comment notice. Compile a synthetic populated copy, inspect page count/rendering/text/links, and record actual results without committing candidate data or generated PDFs. A source-only check does not establish the finished document's quality.

An optional reproducible local check is available when `pdflatex`, `pdfinfo`, `pdftotext`, and `pdftoppm` are on PATH:

```sh
python scripts/check_template.py
```

It populates the template with a fictional three-role/three-project sample under ignored `tmp/template-check/`, requires one page without overfull boxes, checks extracted ordering/common words/separators and embedded destinations, and renders a PNG. Inspect that PNG manually. This optional check is separate from dependency-free CI, installs no tools, and does not access live accounts or certify ATS parsing.

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

Keep edits in the repository source of truth. The installer intentionally refuses to overwrite an existing copy. Compare the existing installed folder with the updated skill, preserve any local edits, and replace it deliberately after review. Alternatively, use the repository copy directly in a compatible agent host. Do not install two identical skills into the same discovery scope. For products without folder-based skill discovery, use the generated portable prompt instead of inventing a product-specific directory.

## Before pushing

Rebuild the portable prompt, then review the staged file list. Keep candidate data, copied source catalogs, raw captions, original third-party guides, tokens, temporary downloads, and runtime dependencies excluded. This is a public repository: check the full history of any branches you publish, not only their current files. The MIT License applies to original project material, not linked third-party sources.
