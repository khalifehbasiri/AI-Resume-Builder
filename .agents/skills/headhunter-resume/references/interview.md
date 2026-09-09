# Guided candidate interview

## Intake by mode

| Mode | Minimum useful inputs | First useful action |
| --- | --- | --- |
| Scratch | Target role; any career history | Collect recent work, education, and strongest project |
| Improve | Existing resume; target role or inferred role to confirm | Extract facts and identify buried evidence |
| Tailor | Posting and existing resume or career inventory | Map posting requirements before writing |
| Base | Role family, level, market; career history | Identify recurring qualifications for that role |
| Review | Existing resume; target if available | Explain prioritized issues and evidence gaps |

Ask for missing inputs conversationally. Do not dump this table or a full intake form into the conversation. If the user supplied a complete brief, begin the analysis. Accept an accessible link, local file, export, or pasted text. If a posting is unavailable, request its qualification text while continuing resume extraction.

Gather name/contact and public links when needed for the final document; drafting does not require phone or email immediately. Ask about education, internships, employment, projects, volunteer work, certifications, languages, and relevant accomplishments conditionally. Include volunteer and unpaid professional work accurately under an appropriate label; do not relabel an actual unpaid internship as a personal project.

## Qualification map

Keep the posting's exact requirement, priority, evidence IDs, assessment, and question. "Supported" means evidence meets the complete requirement. "Partial" means some part is established. "Unknown" means not established. "Absent" means the user has explicitly confirmed they lack it. No mention on a profile is unknown, not absent.

For a general role, consult a small set of comparable current postings in the chosen market when browsing is available. A user-supplied role catalog can provide additional context but is optional. Record the actual sample and dates; never pretend to have surveyed 10-15 jobs. The guide suggests a larger sample to identify recurring qualifications; expand when the role is ambiguous or the user requests market research. A specific posting overrides general frequency.

## Choose the next question

Prioritize a must-have with ambiguous evidence, then unclear ownership or outcomes in the strongest experience, then a missing fact that blocks the document. Ask concrete questions using the user's own project context, without suggesting an answer to adopt.

- Context: What problem did this solve, and for whom?
- Ownership: Which parts did you personally build, operate, or decide? What did teammates do?
- Method: What tools, techniques, protocols, or processes did you use, and for what?
- Outcome: What became possible or easier? Is this an observed outcome or the intended purpose?
- Scale: Is the number known, estimated, or unknown? What supports it? A number is optional.
- Status: Was it a prototype, coursework, production system, maintained service, or unfinished project?

Do not ask every question for every experience. Reuse established answers and stop repeating skipped questions unless a changed requirement makes them essential. When users cannot recall a metric, write an accurate qualitative purpose. Preserve "approximately" for estimates and the difference between intended and measured results.

## Conditional probes

Software: built versus consumed HTTP APIs; endpoint behavior; databases and actual queries; provider-specific cloud work; tests authored; CI checks versus deployment automation; pull requests; authentication; real production incidents; documentation and stakeholders.

Embedded/desktop: device and protocol; command/response behavior; parsing; concurrency; GUI; storage; test setup; simulation versus physical hardware. Ask about baud rate or channel count only when relevant and known.

Data: question answered; data source; SQL transformations; quality checks; analysis versus model training; evaluation methodology; dashboard audience; decisions informed. A notebook importing a library does not prove a deployed model.

Nontechnical roles: customers or stakeholders; operational process; tools and credentials required in the posting; work personally performed; responsibilities and useful outcome. Use the same evidence standard for accounting, customer service, operations, trades, and management.

## Example interaction (fictional)

Candidate: "I built a Python search tool during an internship. Our team used cloud storage."

Ask: "What storage service did your part connect to, and did you write that connection yourself or use an existing component?"

Candidate: "I wrote the Azure Blob Storage integration and the SQLite filters. Staff could find files without opening each container. I don't know the time savings."

A defensible bullet: "Built a Python search tool with Azure Blob Storage integration and SQLite filters so staff could locate files without browsing individual storage containers."

Do not add AWS, REST API development, millions of records, production adoption, or a percentage improvement. Ask separately when those would matter to the target.

## Resume an interrupted interview

Read the candidate's saved inventory and open questions. Briefly confirm the target if it has changed, reuse verified claims, and ask the highest-priority remaining question. Rank projects anew for each target; do not overwrite the broader career inventory with a single tailored subset.
