# AI Resume Builder

A vendor-neutral AI resume coach that helps people identify and explain their **actual experience**, with evidence tracking and checks against fabricated qualifications.

It interviews you about your work, projects, and education, then helps build, improve, tailor, or review a resume. It can use accessible resumes, job postings, LinkedIn exports, GitHub repositories, portfolios, and other relevant sources—or start with only your answers.

Inspired by the Headless Headhunter's qualification-first approach. Independently developed; not affiliated with or endorsed by the creator.

## Works across AI providers

The resume methodology does not depend on Codex, OpenAI, or a particular model. Two editions are included:

- **Universal single-file prompt:** [`portable/headhunter-resume-prompt.md`](portable/headhunter-resume-prompt.md) works in chat products, custom assistants, APIs, and local model runners that can accept a sufficiently long instruction file or prompt.
- **Agent Skills package:** [`.agents/skills/headhunter-resume`](.agents/skills/headhunter-resume) provides progressive loading, references, an inventory template, offline Python checks, and optional OpenAI/Codex UI metadata.

There is no universal cross-company auto-install standard. Automatic skill discovery and tool access depend on the host application, not the underlying model. The universal prompt is the compatibility layer: it gives the same core workflow to any sufficiently capable instruction-following model. Features gracefully fall back when the host has no browsing, file storage, Python, PDF/DOCX reader, or document renderer.

## Quick start with any AI model

1. Download [`headhunter-resume-prompt.md`](portable/headhunter-resume-prompt.md), or use its [raw GitHub version](https://raw.githubusercontent.com/khalifehbasiri/AI-Resume-Builder/main/portable/headhunter-resume-prompt.md).
2. Add the file to the highest-priority instruction area your AI product provides:
   - upload or attach it in a chat;
   - paste it into a project, custom-assistant, or system-instruction field; or
   - use its full text as the system/developer prompt in an API or local model runner.
3. Start with a request such as:

```text
Follow the attached Headhunter Resume instructions. Help me build a resume
for junior software engineering roles in Canada. Interview me first. I have
an existing resume, a GitHub profile, and two projects.
```

If the product does not retain attachments or instructions between chats, attach the prompt again next time. If its context window is too small for the full prompt plus your documents, use the Agent Skills package in a compatible agent runtime or provide the core skill and only the relevant reference files.

## Install the full Agent Skills package

Use this option when your AI agent supports folder-based skills with a `SKILL.md` entrypoint. Check that product's documentation for its skill directory and invocation syntax; folder locations are platform-specific.

Clone or download the repository:

```sh
git clone https://github.com/khalifehbasiri/AI-Resume-Builder.git
cd AI-Resume-Builder
```

Copy the package to a skills directory of your choice:

```sh
python scripts/install_skill.py --destination /path/to/your/agent/skills
```

On Windows, `py -3` can be used instead of `python`. The installer requires Python 3.10 or newer, uses no third-party packages, prints the installed path, and refuses to overwrite an existing folder.

### Codex adapter

Codex can use the repository-scoped package directly from `.agents/skills/headhunter-resume`. To install it for reuse, ask Codex:

```text
Use $skill-installer to install the headhunter-resume skill from:
https://github.com/khalifehbasiri/AI-Resume-Builder/tree/main/.agents/skills/headhunter-resume
```

The included `agents/openai.yaml` only supplies OpenAI/Codex interface metadata. It does not affect the portable instructions or prevent other agents from using the package.

## What you receive

- An editable resume or review.
- A qualification map showing supported, partial, unknown, and absent requirements.
- Unresolved gaps and a concise change note.
- Optionally, a reusable local evidence inventory and claim audit.

The workflow supports building from scratch, improving an existing resume, tailoring to a posting, creating a role-family base resume, and review-only requests. It asks a few relevant questions at a time; "no", "unknown", and "skip" are valid answers.

See the [fictional walkthrough](docs/EXAMPLE.md) or the [provider-neutral usage guide](docs/USAGE.md).

## Capability fallbacks

The package grants no account or tool access by itself.

- If a profile or private repository is inaccessible, paste or export the relevant content.
- If file persistence is unavailable, the AI keeps the evidence bank in the conversation and can return copyable JSON.
- If Python cannot run, the AI performs the structural evidence checks manually.
- If PDF/DOCX rendering is unavailable, editable Markdown is the baseline and formatted export remains unverified.

The skill does not submit applications, send messages, publish profiles, or guarantee interviews. Automated checks validate structure and evidence references; they cannot prove that a candidate statement is true. Review the final resume yourself.

## Your data

The included Python helpers have no network calls or telemetry. Your chosen AI provider may process uploaded documents and use connected services according to that provider's policies and your account settings.

The default saved-work folders, `career-data/` and `output/`, are ignored by this repository. Keep personal resumes and inventories out of GitHub issues and pull requests. Local storage is not encryption and may be on a synced drive. You can request conversation-only work.

## Sources and transparency

The writing approach was informed by the supplied Headless Headhunter guide and reviewed caption segments from **two videos**, not the entire channel. The guided interview, evidence bank, portable prompt builder, and Python helpers are original project additions developed with AI assistance.

Source attribution, timestamps, and explicit adaptations are documented in [research notes](.agents/skills/headhunter-resume/references/research.md) and [methodology](.agents/skills/headhunter-resume/references/methodology.md). Original guides, transcripts, and copied source catalogs are not distributed. The optional local catalog described in [maintenance](docs/MAINTENANCE.md) is not required.

### Repository history

This public repository is the canonical project. It began on September 9, 2026, from a deliberately sanitized release snapshot after private source research. Earlier research commits are not part of the public Git history because they included a copied third-party catalog that is not licensed for redistribution. Subsequent development is preserved here as focused commits on `main`.

## Build and validate

The committed universal prompt is generated from the canonical skill resources. After changing those resources, rebuild it:

```sh
python scripts/build_portable_prompt.py
python -m unittest discover -s tests -v
python scripts/validate_package.py
```

CI verifies the prompt is current and runs the test suite on Windows and Linux with Python 3.10 and 3.13. See [validation notes](docs/VALIDATION.md).

## License

Original code, instructions, documentation, and synthetic examples are available under the [MIT License](LICENSE). Third-party source materials are not covered by that license. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
