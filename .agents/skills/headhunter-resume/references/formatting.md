# Formatting, page fit, and export checks

Read before producing a formatted resume or reviewing its layout. Preserve an existing source and template for follow-up edits. For a new technical LaTeX resume, use [the Jake-based template](../assets/jakes-resume.tex); for other formats, carry over its simple section structure rather than requiring LaTeX.

## One full page without losing useful evidence

Default standard application resumes to one full, balanced page. A full page has meaningful content across the usable area with consistent whitespace; it is not text touching the bottom edge. The user or a specialized application can require another length. A bank or academic CV is a different deliverable.

1. Establish required roles, strongest projects, education/credentials, and supported skills before adjusting layout. Propose relevance-based section ordering and obtain approval using [methodology.md](methodology.md#section-order-by-relevance-with-user-approval); never Skills first, and keep Experience and Projects consecutive when both are present.
2. Allocate more room to recent relevant work and substantial new-grad projects. Choose bullet counts by evidence; do not impose the same count on every role.
3. If underfilled, add the strongest unused supported detail: contribution, outcome, delivery, reliability, testing, or relevant project work. If there is insufficient evidence, explain that limitation; do not invent content or pad with irrelevant employment.
4. If overfilled, remove repetition, generic claims, oversized stack lists, and less relevant details first. Shorten phrasing while retaining method and value. Perform the omission check in [methodology.md](methodology.md) before removing whole entries.
5. Adjust spacing modestly and consistently only when needed. Do not silently compress an established layout, remove a required role, or use unreadably small text to force the page count. If evidence and readability cannot both fit, describe the concrete tradeoff rather than claiming the constraint was met.

Use a single column, standard headings, selectable text, and clear dates. Start around 10.5-11 pt body text; choose a readable professional font rather than enforcing Arial or an allegedly ATS-approved font. Keep margins and section spacing consistent. No portraits, skill bars, or decorative charts by default. Education may lead when it provides the strongest relevant screening evidence, subject to approval of the sequence; a generic summary need not displace stronger evidence. The template's example order is a starting point, not a mandatory education-first layout.

Optional selective bolding can highlight an outcome, significant method, or responsibility for human scanning. Do not bold whole bullets or every technology, and do not claim bolding improves ATS ranking.

## LaTeX template use

Copy the asset into the candidate's output directory; never replace template placeholders inside the installed skill. Placeholder prompts and example domains are not candidate facts. Remove unused placeholder sections and replace all displayed fields before delivery. Preserve the template's copyright and license notice.

The asset provides grouped company/role headings, project links, and skills categories. It adapts Jake's original macros and Unicode mapping, uses Latin Modern fonts to preserve readable glyph extraction, and specifies list paragraph spacing to avoid unintended page overflow. The full upstream MIT notice is embedded in source comments and in [JAKES_TEMPLATE_LICENSE](../assets/JAKES_TEMPLATE_LICENSE). Escape candidate text and URLs for LaTeX, including `%`, `&`, `_`, `#`, and braces. Use `\textbar{}` or a tested separator rather than assuming a literal `|` renders correctly in every font encoding. Check symbols and ligatures in extracted text as well as visually.

Use the host's built-in LaTeX editor/compiler when available, otherwise an available compiler; do not claim an unavailable capability. Follow-up edits stay in the existing file. Compilation success confirms compilation, not page fit or ATS behavior. Diagnose errors and preserve source if compilation is unavailable or fails. Do not substitute an old PDF for a changed source.

## Final export checks

When tools permit, check the actual deliverable:

- **Page count:** count PDF pages or rendered DOCX pages; source length and successful compilation are insufficient.
- **Visual layout:** render and inspect every page at readable size. Look for clipping, dense paragraphs, stranded headings, overlap, extra pages, and unbalanced spacing.
- **Extracted text:** verify contact information, the approved section order, employer/role association, dates, bullets, skills, and symbols. Confirm Skills is not first and Experience/Projects are consecutive whenever both are included. This is a parser proxy, not a test of every ATS.
- **Links:** inspect embedded destinations; check accessible public pages. Record inaccessible or login-protected links without pretending they were verified.
- **Content:** compare the export with the saved source and final approved wording, including an omission audit and evidence audit. For requested website alignment, compare the current downloadable PDF with this version; account for cached pages before asserting it is stale.

Respect the application's requested file format. Otherwise a selectable PDF plus the editable source is useful when export tools are available. Use a clear filename. Do not deliver placeholders or compiler diagnostics as resume content.

If export, rendering, page counting, or text extraction is unavailable, provide editable content and identify which checks remain unverified. Keep the one-page target, but do not claim a verified one-page file based solely on text. After a narrow edit, report exactly what changed and the checks performed; preserve unrelated wording and layout.
