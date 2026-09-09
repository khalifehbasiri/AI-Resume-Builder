# Career evidence bank

Copy `assets/inventory.json` to `career-data/<candidate-id>/inventory.json` in the user's working project when persistence is appropriate. Use a neutral candidate ID, not an email address. Never write candidate facts into the installed skill. Reopen that file on later tasks; the skill provides no hidden cross-session memory.

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

Qualification assessments also require judgment. `supported` needs at least one confirmed claim, but the validator cannot decide whether a claim fully proves a compound requirement or a numerical threshold. Resolve each part explicitly before classifying it.
