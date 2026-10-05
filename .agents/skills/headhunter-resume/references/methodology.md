# Writing decisions and their reasons

## How the sources are combined

Use the candidate's request, truthful evidence, and the actual application requirements to resolve choices. Source guides inform the workflow; their preferences are not universal hiring facts. The inspected sources and limits are recorded in [research.md](research.md).

| Source or lesson | What we retain | Why and where we adapt |
| --- | --- | --- |
| Headless Headhunter guide and reviewed videos | Qualification-first selection; understandable work context; action, method, purpose/result | A nonspecialist should understand what the candidate did and why it mattered. Retain technical methods that establish engineering depth. |
| Jake's LaTeX template | Consistent single-column sections, compact headings, projects, categorized skills, Unicode text mapping | Provides a reusable starting layout. A template or Unicode setting alone cannot prove ATS compatibility; inspect the actual PDF. |
| Supplied Jake's Resume guide | Clear headings, action verbs, relevant keywords, readable bullets, useful outcomes, consistent presentation | Supports both human scanning and machine-readable information. Do not adopt its fixed skill counts, bullet quotas, one-line limit, unsupported hiring statistics, or claims of universally approved fonts. |
| Main-resume revisions | One substantive page; required roles; project depth; omission checks | Over-simplification can remove the candidate's strongest evidence. Fill the page with useful facts rather than unrelated work or visual padding. |
| Metrics corrections | User confirmations, attributed outcomes, explicit baselines and scope | Numbers can clarify value, but incorrect arithmetic or attribution damages credibility. Keep supported numbers even though sampled Headless videos discourage many software metrics. |
| ATS and skills revisions | Categorized supported skills plus examples of actual use | Qualification-first prose can still omit literal searchable terms. Check terminology and text extraction alongside human readability; neither replaces evidence. |
| Profile revisions | Shared facts, different lengths for different surfaces | Copying dense resume bullets everywhere can overwhelm LinkedIn and small portfolio cards. Preserve explicit domain terminology while shortening the presentation. |
| Relevance-based section order | Put the strongest supported qualifications earlier, with user approval; never Skills first; keep Experience and Projects adjacent | The strongest evidence may be a project, degree, credential, or employment. A fixed education-first or experience-first layout can bury it. Approval preserves the candidate's layout choice; adjacent work/project sections keep their evidence easy to compare. |

These adaptations are independently authored design choices. They do not imply endorsement or that either source creator teaches every rule here.

## Decide the deliverable

- **Resume Experience Bank:** reusable detailed facts and alternative bullets; no page limit.
- **Primary resume (base mode):** substantive application resume for the chosen role family, retaining useful technical breadth. A job posting is optional.
- **Tailored resume:** posting-specific emphasis, skills, and project selection from the same bank.

"Master" can mean either a primary application resume or an exhaustive reference document. Clarify only when needed. Preserve the user's required roles and exclusions as candidate preferences, not rules for everyone. Default standard application resumes to one full, balanced page, with user-selected length and specialized CV/application formats taking precedence. Read [formatting.md](formatting.md) for fitting and verification.

## Section order by relevance, with user approval

Evaluate every included section against the actual posting or chosen role family, using confirmed evidence and important screening requirements. Education, credentials, publications, and other substantive sections may lead when they provide the strongest relevant proof; neither Education nor Experience automatically belongs first. A generic summary should not displace stronger evidence. Do not rank a section first merely because its title or skills list repeats keywords.

Keep the name/contact header at the top. **Skills or Technical Skills must never be the first resume-body section.** Treat Experience and Projects as one consecutive block whenever both are included. Choose their internal order by which demonstrates the target qualifications better, then place that block among the other sections by relevance. Adjacency means consecutive vertical sections in the single-column document, not side-by-side columns. Do not put Education, Skills, a summary, or any other section between Experience and Projects. Do not invent an empty section when one is absent.

Before applying this ordering to a new or existing resume, show the complete proposed sequence and a brief evidence-based reason, then explicitly ask for approval. For example: "For this AI engineering role, your RAG project demonstrates the required AI work more directly than your employment. I recommend Projects → Experience → Education → Technical Skills. May I use this order?" This is a reviewable proposal; a general request to improve or tailor the resume is not approval for the sequence.

Apply only after the user approves. An explicit user request for that exact sequence, or an earlier approval for the same target and sequence, already provides authorization; do not ask again. A materially different sequence or target requires a fresh proposal and approval. Record the approved order, target, and approval locator in the candidate's bank notes so reuse remains scoped.

If approval is pending, continue evidence gathering and bullet work without applying the proposed reorder. If the user declines, retain the existing valid order or agreed template default and offer another compliant sequence if useful. If the existing order starts with Skills or separates Experience and Projects, explain the conflict and seek approval for a compliant order rather than silently moving sections. Do not interpret silence as approval. Narrow bullet edits do not trigger an unsolicited reorder.

Illustrative approved orders, excluding the contact header:

- AI projects provide stronger relevant evidence: **Projects → Experience → Education → Technical Skills**.
- Employment provides stronger relevant evidence: **Experience → Projects → Education → Technical Skills**.
- Education is the strongest relevant credential: **Education → Experience → Projects → Technical Skills**.
- A required professional credential is strongest: **Certifications → Education → Projects → Experience → Skills**.

These are examples, not fixed templates. Preserve accurate chronology inside Experience and relevant project ranking inside Projects. After an approved reorder, recheck page fit, reading order, and that the rendered section sequence matches the approved one.

## Write bullets that explain value

Use action + relevant method/qualification + context + useful purpose or observed outcome. Do not force every element into every bullet. The opening bullet should explain the application, service, or work to someone outside the specialty. A qualification can also be proven by another bullet; never force a separate bland summary that wastes space.

Choose the strongest combination of product breadth, impact, technical depth, reliability, testing, teamwork, and delivery. A list of tiny features is usually weaker than a coherent account of the problem solved. Keep a small feature when it demonstrates a relevant skill or consequential design decision.

Fictional example:

- Thin: "Implemented wildcard search."
- More useful, if confirmed: "Developed a Python metadata search tool that reduced manual file lookup from hours to seconds or minutes, using SQLite filters and Azure Blob Inventory."
- Without timing evidence: "Developed a Python metadata search tool with SQLite filters so staff could locate files without inspecting storage containers individually."

Do not transplant example facts into a candidate's resume. Use supported scope as scope, not an invented outcome. Reliability and data integrity can establish value even without a measured percentage.

Check for buried delivery ownership: client requirements, application design, demonstrations, development, testing, deployment, training, and support. Name the stages the candidate actually performed. Do not infer delivery from code or Agile participation alone. Use the audience's accurate label (clients, staff, customers, or users).

Use precise, varied verbs: **Developed/Built** for implementation, **Engineered** for substantial system work, **Designed** for design ownership, **Integrated** for connecting systems, **Implemented** for a concrete behavior, **Expanded** for extending an existing system, **Led** for actual leadership. Repetition is preferable to an inaccurate synonym; "architected," "spearheaded," and "optimized" require corresponding evidence. Use past tense for completed accomplishments, including completed work in a current role; present tense for ongoing duties. Bullet counts and line lengths follow evidence and page space, not fixed quotas.

## Preserve technical breadth and ATS terminology

For technical resumes, include a concise categorized skills section, unless the user chooses otherwise: languages; frameworks/tools; databases/cloud; relevant domains or methods. Adapt the categories to the candidate. Other professions may need licenses, equipment, systems, or professional methods instead.

Audit against both the posting and the bank. Skills need confirmed evidence of use and a level the candidate can discuss; they need not all be repeated in bullets. Exclude skills the candidate declines or cannot substantiate. Do not turn a dependency, team stack, or employer technology into personal proficiency. Do not include every minor library or generic soft skill merely to increase keyword counts.

Keep recognizable technology names and explicit domain terms when useful. For example, TensorFlow alone need not communicate **machine learning (ML)** to every reader. Actual retrieval work may support **retrieval-augmented generation (RAG)**, hybrid search, citations, or evaluation; an API call alone does not. Expand a relevant acronym once when space permits, then use the short form. Exact posting terminology is useful only when its meaning matches the work.

Perform a literal terminology check separately from the evidence audit. Report supported terms present and relevant omissions. Do not describe a keyword count, PDF extraction result, or font choice as an ATS pass score. Treat degree, license, authorization, and experience thresholds separately from keyword coverage. Source guides' suggested coverage percentages are not application gates or interview probabilities.

## Select experiences and projects

Keep required core roles. Group consecutive positions at the same employer under one company heading, with distinct accurate role titles and month/year dates. Sort employers by latest relevant role, and roles within a group newest first; an overlapping short role at another employer can follow the continuous employer group. Do not double-count overlapping time, claim a promotion without confirmation, merge titles to inflate seniority, or switch to year-only dates to conceal a short contract. Unknown months remain unknown.

Add a recognizable parent organization or a short domain descriptor when accurate and useful, without replacing the official employer or inventing an affiliation. Include unrelated work only when its contribution is useful for the target or the user explicitly requires it. Prefer relevant project detail to unrelated filler.

Give new-grad projects meaningful space. Rank them by relevance, personal contribution, engineering depth, teamwork, validation, and demonstrated outcomes. Publication is one signal; a published shallow app need not outrank a substantial team simulation. Keep simulation, prototype, deployment, and validation status accurate. Choose a few major technologies for each header; use bullets to explain distinctive work.

For each listed project include every available public destination: GitHub and live demo when both exist; product/site when the repository is private or unavailable; GitHub when no demo exists. Label links clearly (GitHub, Live Demo, Product Site), verify their destinations when accessible, and do not expose a private repository. Header contact links do not replace project-specific links.

## Omission check and review

Before approving a shortened draft, compare it with the prior resume and the bank. Check for lost outcomes, technical depth (such as concurrency, database work, reliability, security, or geospatial tooling), team contributions, client collaboration, and delivery/support. Restore relevant material or explain the tradeoff. Do not restore every fact indiscriminately; preserve the remainder in the bank.

Use a simulated 10-20 second scan as a readability heuristic, not a claim about all recruiters. Verify titles, dates, ownership, metrics, stage, and links; then follow the export checks in [formatting.md](formatting.md). Keep unresolved questions outside the resume. If asked to rate the document, explain strengths and deductions for content, clarity, relevance, and formatting; label any score subjective. Do not predict interviews, rank a candidate's worth, or repeat source statistics and legal advice as current facts.
