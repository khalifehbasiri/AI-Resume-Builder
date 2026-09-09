# Using the skill

First follow one of the [installation methods in the README](../README.md#install). For a concrete example of the interview and resulting resume section, see the [fictional walkthrough](EXAMPLE.md).

## A complete workflow

1. Invoke `$headhunter-resume` and describe your goal. Include an existing resume if available, target role/level/market, and any relevant profile or project links. For tailoring, include the job posting.
2. Codex extracts your existing information and checks accessible sources. It should tell you if a source could not be read and can continue from your answers or exports.
3. Codex maps target qualifications to evidence and asks a few specific questions at a time. For example, it may ask whether your GitHub workflow only ran tests or also deployed an application. "No", "unknown", and "skip" are valid answers.
4. After enough information is established, Codex drafts the resume and checks that the wording matches your contribution and verified facts. It highlights genuine gaps instead of adding missing qualifications.
5. You receive the resume, qualification map, and a concise explanation of changes and unresolved issues. Review dates, titles, contact information, attribution, and outcomes before using it.

A review-only request returns findings before suggested edits. You can request a first draft at any point; uncertain claims remain outside the resume. New candidates get separate inventories. A new target for the same candidate reuses the existing evidence and selects the most relevant projects again.

## Formats

Resume inputs can be accessible PDF, DOCX, LaTeX, Markdown, or pasted text. Codex uses its installed readers; scanned or complex documents may need visual/OCR verification. If extraction fails, provide a readable export or the relevant text.

The portable baseline is editable Markdown. Ask for DOCX or PDF when those document tools are available in your Codex environment. The skill instructs Codex to inspect the rendered pages before calling a formatted file verified; these export tools are not bundled here. The skill does not submit job applications or modify your profiles.

## Saved work

Default location within your working project:

```text
career-data/candidate-01/
  inventory.json
  draft-claims.json
  qualification-map.md
output/
  resume.md
```

`inventory.json` holds career evidence, source IDs, experiences, target requirements, and open questions. `draft-claims.json` maps each factual resume statement to evidence IDs. The qualification map explains supported, partial, unknown, and explicitly absent qualifications. You can choose another location or request conversation-only work. Files in a different working project need that project's own ignore rules; this repository's `.gitignore` does not protect every directory on your machine.

To resume later, explicitly point Codex at the inventory. The skill cannot remember files it cannot access, and does not store your career history in a global profile.

## Helper commands

From the repository root:

```sh
python .agents/skills/headhunter-resume/scripts/resume_tools.py validate career-data/candidate-01/inventory.json
python .agents/skills/headhunter-resume/scripts/resume_tools.py audit career-data/candidate-01/inventory.json career-data/candidate-01/draft-claims.json
```

Exit 0 means the structural check passed; exit 1 means validation findings; exit 2 means a command/data read error. Passing does not prove the facts, determine hiring fit, or ensure every resume sentence was included in the manifest. Codex must still inspect meaning and complete coverage.

Optional local catalog search requires a user-supplied file; no third-party catalog is bundled:

```sh
python .agents/skills/headhunter-resume/scripts/resume_tools.py search "software engineer" --kind episodes --catalog career-data/reference-catalog.json
```

The [maintenance guide](MAINTENANCE.md) describes optional imports. Search is case-insensitive and matches all supplied terms in the job title; it does not perform semantic matching or search the video transcript. A null episode URL is an unresolved source link. A future release date is not confirmation of current public availability. The interview and resume workflow does not need a catalog.

## Source access

LinkedIn works through an available authorized browser/connector, an export, or pasted content. GitHub inspection may use public pages, a connected GitHub account, or a local repository. Portfolios and supporting links should belong to you or describe your work. Share only material relevant to your candidacy; confidential employer details can be generalized accurately.

Source access is read-only within this workflow. Never give the skill passwords or paste tokens into an inventory. A fork or an organization repository is not evidence that you implemented every feature. Explain your role and contributions when asked.
