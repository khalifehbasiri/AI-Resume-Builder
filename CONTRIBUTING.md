# Contributing

Contributions that make the skill more useful, accurate, and accessible are welcome.

## Report a problem

Open a GitHub issue with your operating system, Python version if relevant, installation method, expected behavior, and what happened. Use fictional or carefully anonymized examples. Do not post resumes, contact details, private repository content, employer-confidential information, credentials, or raw conversation logs containing personal data.

For interview or writing problems, include a short synthetic candidate prompt that reproduces the issue. Explain the unsupported claim, missed question, or confusing output. Distinguish an instruction problem from a tool access failure.

## Make a change

1. Fork the repository and work on a branch.
2. Keep changes focused. Preserve user intent, truthful attribution, and the ability to say "unknown".
3. Add a regression test when changing helper behavior. For instruction changes, include a realistic synthetic scenario and the observed result.
4. Run `python -m unittest discover -s tests -v` and `python scripts/validate_package.py`.
5. Open a pull request explaining the problem, resulting behavior, and verification.

Do not include copied guides, transcripts, qualification tables, or other third-party datasets without established redistribution rights. Keep optional imports under ignored local folders. New original contributions are submitted under this project's MIT License.

AI-assisted contributions are welcome. Review generated changes, test them, and accurately describe what was verified. Avoid claims of universal ATS compatibility, guaranteed interviews, or perfect factual validation.
