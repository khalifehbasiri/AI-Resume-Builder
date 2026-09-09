# AI Resume Builder

An AI-assisted resume coach that helps people identify and explain their **actual experience**, with evidence tracking and checks against fabricated qualifications.

This free, open-source **Codex skill** interviews you about your work, projects, and education, then helps you build, improve, tailor, or review a resume. It can use your accessible LinkedIn, GitHub, portfolio, and other relevant sources. You can also start with just your answers.

Inspired by the Headless Headhunter's qualification-first approach. Independently developed; not affiliated with or endorsed by the creator.

## Install

You need a Codex environment that supports local skills. This is not a standalone website, browser extension, or ordinary ChatGPT prompt. The project adds no API subscription or API-key requirement; your normal Codex access and usage limits still apply.

### Option 1: Ask Codex to install it

Paste this into Codex:

```text
Use $skill-installer to install the headhunter-resume skill from:
https://github.com/khalifehbasiri/AI-Resume-Builder/tree/main/.agents/skills/headhunter-resume
```

Start a new turn after installation. If it does not appear in the skill selector, restart Codex. This installs the skill for reuse; you do not need to keep this repository open.

### Option 2: Install from the repository

Requires Git and Python 3.10 or newer. No third-party Python packages are required.

```sh
git clone https://github.com/khalifehbasiri/AI-Resume-Builder.git
cd AI-Resume-Builder
```

On Windows:

```powershell
py -3 scripts/install_skill.py
```

On macOS or Linux:

```sh
python3 scripts/install_skill.py
```

The script copies the skill to `~/.agents/skills/headhunter-resume`, where `~` is your user home directory. It prints the full installation path and refuses to overwrite an existing installation. If the Windows Python launcher is unavailable, use `python` instead of `py -3`.

No Git? Download the repository using **Code > Download ZIP**, extract it, open a terminal in the extracted folder, and run the same installation command.

### Option 3: Try it in this repository

Clone or download the repository and open its folder in Codex. The skill is already in `.agents/skills/headhunter-resume`; no installation command is needed. Python is only required when running the helper scripts. Avoid installing another copy if the repository copy is enough for you.

Local skill locations and discovery behavior are described in the [official Codex skill documentation](https://learn.chatgpt.com/docs/build-skills). Codex's built-in installer may use its configured skills directory instead of the standalone installer's `~/.agents/skills`; use the path it reports when updating or uninstalling.

## Start using it

```text
Use $headhunter-resume to help me build a resume for junior software
engineering roles in Canada. Interview me about my experience first.
I have an existing resume, a GitHub profile, and two projects.
```

You can instead ask it to review without rewriting, tailor to a specific posting, or start from scratch. Supply the files or URLs you want it to consider. It asks a few relevant questions at a time; "no", "unknown", and "skip" are valid answers.

You receive an editable resume or review, a qualification map, and unresolved gaps. For example, a teammate's AWS work should stay attributed to that teammate. The skill should not turn it into your AWS experience.

See the [fictional walkthrough](docs/EXAMPLE.md) for an interview and its resulting resume section, or the [usage guide](docs/USAGE.md) for formats, saved evidence, and helper commands.

## What it supports

- Build from scratch, improve a resume, tailor to a posting, create a role-specific base resume, or review only.
- Discover relevant details through questions about personal contribution, methods, purpose, and outcomes.
- Read career sources through tools already available in your Codex environment, preserving attribution and conflicting facts.
- Reuse a local career evidence bank for different target jobs.
- Check readability, truthful keyword use, and evidence references before delivery.

LinkedIn may require an export or pasted text. Private GitHub repositories require authorized access. No connectors or document renderers are bundled, and installing this skill does not grant account access. Editable Markdown is the baseline; DOCX/PDF output requires suitable tools in your Codex environment.

The skill does not submit applications, send messages, publish profiles, or guarantee interview results. Python checks validate structure and references; they cannot prove that a statement is true. Review the final resume yourself.

## Your data

The included Python helpers have no network calls or telemetry. Codex may use its available tools and connected services when you request source research; your normal provider settings still apply.

The default saved-work folders, `career-data/` and `output/`, are ignored by this repository. Keep personal resumes and inventories out of GitHub issues and pull requests. Other projects need their own ignore rules. Local storage is not encryption and may be on a synced drive. You can ask the skill to keep the work in the conversation without creating files.

## Sources and transparency

The writing approach was informed by the supplied Headless Headhunter guide and reviewed caption segments from **two videos**, not the entire channel. The guided interview, evidence bank, and Python helpers are original project additions developed with Codex assistance.

Source attribution, timestamps, and explicit adaptations are documented in [research notes](.agents/skills/headhunter-resume/references/research.md) and [methodology](.agents/skills/headhunter-resume/references/methodology.md). Original guides, transcripts, and copied source catalogs are not distributed. Optional local catalog import is described in [maintenance](docs/MAINTENANCE.md); it is not required to use the skill.

## Updates and troubleshooting

- Skill missing: start a new turn or restart Codex; confirm the installed folder contains `SKILL.md` directly, not inside another nested folder.
- Duplicate entries: keep one active installation. The built-in installer, standalone installer, and repository scope may use different locations.
- Existing installation: compare your installed copy with the new source, move any customized copy outside the skills directory as a backup, then install again. The script never overwrites it automatically.
- Uninstall: remove only the installed `headhunter-resume` folder at the path reported during installation. Saved candidate data is stored separately.

## Contribute and test

Bug reports, clearer interview questions, and synthetic test cases are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before sharing examples.

```sh
python -m unittest discover -s tests -v
python scripts/validate_package.py
```

Use `python3` or `py -3` if that is your Python command. CI runs on Windows and Linux with Python 3.10 and 3.13. See [validation notes](docs/VALIDATION.md) for observed behavior and limits.

## License

Original code, instructions, documentation, and synthetic examples are available under the [MIT License](LICENSE). Third-party source materials are not covered by that license. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
