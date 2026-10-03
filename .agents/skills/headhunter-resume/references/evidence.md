# Career evidence bank

Copy `assets/inventory.json` to `career-data/<candidate-id>/inventory.json` in the user's working project when persistence is appropriate. Use a neutral candidate ID, not an email address. Never write candidate facts into the installed skill. Reopen that file on later tasks; the skill provides no hidden cross-session memory.

## Build a readable Resume Experience Bank

Suggest an AI-assisted interview to build the bank from existing resumes, candidate answers, and accessible career sources. Copy [experience-bank.md](../assets/experience-bank.md) alongside the inventory and complete entries incrementally. Markdown is the portable default; DOCX is optional when requested and supported. The bank has no page limit. It should preserve useful details that do not fit a primary or tailored resume, including alternative bullets and deeper project explanations.

For each role/project capture the problem and audience, personal and team contributions, actual tools and methods, client collaboration, design decisions, testing, delivery/training/support, outcomes, scope, status, and public links. Tie usable facts and bullet alternatives to claim IDs. The readable bank and JSON inventory represent the same facts; update both after a correction. Do not create a second conflicting source of truth or require a complete bank before drafting.

## Inventory schema

The version-1 inventory contains:

- `candidate_id`: one candidate per bank.
- `target`: mode, role, seniority, market, optional posting URL.
- `sources`: unique ID, kind, locator, accessed date, short note. A conversation answer can be a source with a turn/date locator.
- `experiences`: unique ID, kind, title, organization, start/end (YYYY-MM, `present`, or null), description. Title, organization, and description may be null during intake when unknown; never invent an employer for a personal project. Do not guess missing months. Resolve required display fields before calling a resume complete, or omit the affected entry and explain the limitation.
- `claims`: unique ID, experience ID (or null for education/contact), text, status, ownership, source IDs, keywords, confirmation note.
- `requirements`: unique ID, exact text, required/preferred priority, supported/partial/unknown/absent assessment, supporting claim IDs.
- `open_questions`: remaining questions as strings. Record skipped questions in `notes` to avoid repetition.
- `notes`: candidate context, unresolved source conflicts, and revisions.

Claim status is `confirmed`, `unconfirmed`, `conflict`, or `rejected`. Ownership is `personal`, `team`, or `unknown`. `confirmed` means explicitly attested by the candidate or directly established with appropriate attribution; it does not mean independently background-checked. Team ownership may support a scoped team claim, never "I built everything". Unknown ownership cannot support a final resume claim until clarified. Never delete conflicting history just to pass validation.

Version 1 also accepts these optional extensions; older inventories remain valid:

- `preferences`: `page_target` (positive integer, default 1), `template` (nonempty label), `required_experience_ids` (existing experience IDs), and `excluded_keywords` (terms the user excludes). Requirements and format instructions still take precedence over defaults. An empty inventory omits the required-ID list until experiences exist.
- Experience `employer_group`: a shared nonempty grouping ID, or null. It enables one employer heading without collapsing distinct role titles or dates; confirm the relationship manually.
- Experience `public_links`: objects with `kind` (`github`, `demo`, `product`, or `other`), `label`, and HTTP(S) `url`. Record every available public destination; a private repo is not a public link.
- Claim `delivery_status`: `planned`, `prototype`, `implemented`, `released`, or `production`, when useful. This describes stage; claim `status` describes certainty. A confirmed plan is still a plan. Record simulation/physical testing and evaluation limitations as separate claims.
- Claim `metric`: `kind` (`scope`, `outcome`, or `adoption`), `value` (text preserving the confirmed number/range), `qualifier` (`exact`, `approximate`, `minimum`, or `range`), `population`, `attribution`, and nullable `baseline`, `outcome`, and `window`. Do not guess a missing window or baseline. Split unrelated numbers into separate claims.
- Claim `supersedes`: prior claim IDs corrected by this claim. Keep the original record and revision reason, usually mark an invalidated original `rejected`, and update questions/requirements/draft references. A confirmed correction makes the prior IDs unusable in a new draft even if their old status was not updated. The validator rejects self-references, cycles, and unknown IDs.

Record a candidate's explicit confirmation as an interview source and its date/locator. Do not reopen an analytics-source question that the candidate already answered unless new evidence creates a concrete conflict. Supersession is for a correction of the same assertion, not for replacing a weak bullet with an unrelated stronger one.

## Metrics and attribution

Preserve the measured or user-confirmed assertion without silently expanding it. A before/after timeline for one workflow does not establish a percentage for another workflow. If a prior percentage depended on a corrected baseline, reject it; do not recompute from vague units such as "weeks" and "a few hours". With no established baseline, a truthful statement such as replacing manual entry checks with validation completed in minutes may be sufficient.

Distinguish an employer's customer base from customers gained through the candidate's site, and visits from unique visitors. Distinguish a storage estate searchable through metadata from bytes personally copied or processed. Use approximate wording for estimates; `+` requires a confirmed minimum, not merely a rounded estimate. Keep reported improvements attributed when appropriate. There is no requirement to invent a number for every accomplishment.

An evidence claim records one factual assertion, not a paragraph mixing several certainty levels. Avoid bundling confirmed Python experience with unconfirmed AWS experience. Use separate IDs and cite the precise ones needed for each final claim.

Example claim:

```json
{
  "id": "claim-search",
  "experience_id": "exp-intern",
  "text": "Personally implemented SQLite filters in a Python file-search tool for staff.",
  "status": "confirmed",
  "ownership": "personal",
  "source_ids": ["source-interview"],
  "keywords": ["Python", "SQLite", "SQL"],
  "confirmation": "Candidate described writing SELECT queries and filters during intake."
}
```

Before delivering a file-based draft, create `draft-claims.json` containing every factual resume statement (including contact, education, dates, skills, and each bullet), not only selected bullets:

```json
{
  "claims": [
    {
      "text": "Built SQLite filters in a Python file-search tool for staff.",
      "evidence_ids": ["claim-search"]
    }
  ]
}
```

Run the inventory validator, then the draft audit. The audit requires known confirmed evidence with known ownership for each draft claim. It does not read the resume file, detect omitted claims, understand entailment, or verify external facts: the agent must compare the manifest with the entire resume and inspect whether the evidence really supports each assertion. Changing "staff" to "10,000 customers" can pass a structural audit and must fail the manual semantic review.

The extended validator checks optional field shapes and correction references; the audit blocks confirmed-superseded evidence. Neither verifies that a metric's meaning, grouping, public visibility, delivery status, or attribution is true. Manually check required roles, skill exclusions, and omissions against the actual resume, because a claims manifest alone cannot prove those layout/content decisions.

Qualification assessments also require judgment. `supported` needs at least one confirmed claim, but the validator cannot decide whether a claim fully proves a compound requirement or a numerical threshold. Resolve each part explicitly before classifying it.
