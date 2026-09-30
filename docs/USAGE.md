# Using AI Resume Builder

Choose the edition that fits your AI product:

- Use the [single-file portable prompt](../portable/headhunter-resume-prompt.md) with ordinary chats, uploaded project instructions, custom assistants, APIs, and local model runners.
- Use the [Agent Skills package](../.agents/skills/headhunter-resume/SKILL.md) when the host can discover a `SKILL.md` folder and load its referenced files.

For a concrete interview and resulting resume section, see the [fictional walkthrough](EXAMPLE.md).

## Universal prompt setup

Place the entire portable prompt in the highest-priority instruction field the product makes available. Depending on the product, that may be a system prompt, project instruction, custom-assistant instruction, knowledge attachment, or ordinary chat attachment. Then ask the model to follow the file for the current resume task.

This is portable behavior, not universal auto-installation. Models and host applications differ in context length, attachment handling, tool access, and how faithfully they follow long instructions. A small local model may need the shorter `SKILL.md` plus only the reference relevant to the current step.

## A complete workflow

1. Describe your goal. Include an existing resume if available, the target role/level/market, and relevant profile or project links. For specific tailoring, include the job posting.
2. The AI extracts existing information and checks only sources it can actually access. If a source is unavailable, paste or upload an export, or continue from your answers.
3. The AI maps target qualifications to evidence and asks a few specific questions at a time. For example, it may ask whether a GitHub workflow only ran tests or also deployed an application. "No", "unknown", and "skip" are valid answers.
4. After enough information is established, the AI drafts the resume and checks that wording matches your contribution and verified facts. Genuine gaps stay visible instead of becoming invented qualifications.
5. You receive the resume, qualification map, and a concise explanation of changes and unresolved issues. Review dates, titles, contact information, attribution, and outcomes before using it.

A review-only request returns findings before suggested edits. You can request a first draft at any point; uncertain claims remain outside the resume. New candidates get separate inventories. A new target for the same candidate can reuse an inventory that you save and provide again.

## Formats and tools

Resume inputs can be PDF, DOCX, LaTeX, Markdown, or pasted text when the chosen AI host can read them. Scanned or complex documents may need visual/OCR verification. If extraction fails, provide a readable export or the relevant text.

Editable Markdown is the universal output baseline. Ask for DOCX or PDF when suitable document tools are available. The instructions require rendered pages to be inspected before a formatted file is called verified; without a renderer, the AI should clearly state that limitation.

Browsing, connectors, repositories, code execution, and file storage are optional capabilities. The prompt tells the AI to use them only when available and authorized. It must not imply that it opened a link, private account, or file that it could not access.

## Saved work

When file storage is available, the default layout is:

```text
career-data/candidate-01/
  inventory.json
  draft-claims.json
  qualification-map.md
output/
  resume.md
```

`inventory.json` holds career evidence, source IDs, experiences, target requirements, and open questions. `draft-claims.json` maps each factual resume statement to evidence IDs. The qualification map explains supported, partial, unknown, and absent qualifications.

If the host has no persistent files, ask it to return the inventory as a JSON code block and save that text yourself. Upload or paste it in a later chat to continue. No model should claim durable hidden memory as a substitute for saved evidence.

## Optional helper commands

The full package includes offline, standard-library Python checks:

```sh
python .agents/skills/headhunter-resume/scripts/resume_tools.py validate career-data/candidate-01/inventory.json
python .agents/skills/headhunter-resume/scripts/resume_tools.py audit career-data/candidate-01/inventory.json career-data/candidate-01/draft-claims.json
```

Exit 0 means the structural check passed; exit 1 means validation findings; exit 2 means a command/data-read error. Passing does not prove the facts, determine hiring fit, or ensure every resume sentence was included in the manifest. The AI and candidate must still inspect meaning and coverage. If Python is unavailable, the portable prompt instructs the AI to perform the same checks manually.

Optional local catalog search requires a user-supplied file; no third-party catalog is bundled:

```sh
python .agents/skills/headhunter-resume/scripts/resume_tools.py search "software engineer" --kind episodes --catalog career-data/reference-catalog.json
```

The [maintenance guide](MAINTENANCE.md) describes optional imports. The interview and resume workflow does not need a catalog.

## Source access and privacy

LinkedIn can be supplied through an authorized browser/connector, an export, or pasted content. GitHub inspection may use public pages, an authorized connected account, or a local repository. Share only material relevant to your candidacy; confidential employer details can be generalized accurately.

Never paste passwords or access tokens into a chat or inventory. A fork or organization repository is not evidence that you implemented every feature. Explain your role and contributions when asked. Review the privacy and data-retention settings of the AI provider you choose before uploading personal documents.
