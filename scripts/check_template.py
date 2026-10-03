"""Compile a synthetic template sample and check page count/text/links with local TeX and Poppler.

Optional developer check, not part of the dependency-free package gate. No candidate
data or network access is used. Inspect the generated PNG manually for visual quality.
"""

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / ".agents/skills/headhunter-resume/assets/jakes-resume.tex"

# Fictional contributions exercise grouped roles, substantive bullets, special
# characters, both project destinations, and a private project's product link.
SAMPLE = r"""\begin{document}
\begin{center}
  \textbf{\LARGE Fictional Candidate}\\[3pt]
  Toronto, ON \textbar{} 555-010-0100 \textbar{} \href{mailto:sample@example.com}{sample@example.com}\\[2pt]
  \href{https://example.com/linkedin}{LinkedIn} \textbar{} \href{https://example.com/github}{GitHub} \textbar{} \href{https://example.com/portfolio}{Portfolio}
\end{center}
\section{Education}
\resumeHeadingListStart
  \resumeEducationHeading{Example University}{Toronto, ON}{Bachelor of Computer Science}{May 2026}
\resumeHeadingListEnd
\section{Experience}
\resumeHeadingListStart
  \resumeCompanyHeading{Example Agency \textbar{} Example Government}{Ottawa, ON}
  \resumeRoleHeading{Software Developer}{Aug 2024 -- Dec 2025}
  \resumeItemListStart
    \resumeItem{Developed a bilingual Python validation application that replaced manual entry checks with automated review and reports for regional clients.}
    \resumeItem{Expanded the application with comparison and geospatial workflows; a client reported that one review process fell from several days to a few hours.}
    \resumeItem{Led a three-person team and worked directly with clients to gather requirements, design workflows, present demos, and test staged releases.}
    \resumeItem{Deployed releases, trained staff, and supported production use, resolving reported issues and documenting application behavior for new team members.}
  \resumeItemListEnd
  \resumeRoleHeading{Programmer}{Sep 2023 -- Jul 2024}
  \resumeItemListStart
    \resumeItem{Engineered a multithreaded Python metadata explorer with Azure Blob Inventory, MongoDB, and SQLite so staff could locate files without manual browsing.}
    \resumeItem{Kept searches responsive during refreshes and preserved the last valid database after failed updates, allowing staff to continue using the application.}
  \resumeItemListEnd
  \resumeCompanyHeading{Example Studio}{Remote}
  \resumeRoleHeading{Frontend Developer}{Jan 2025 -- Mar 2025}
  \resumeItemListStart
    \resumeItem{Developed a responsive product website with React and TypeScript, integrating documentation and accessible navigation for prospective customers.}
    \resumeItem{Organized reusable components and centralized content models to keep product pages and language-specific API examples consistent and easy to update.}
  \resumeItemListEnd
\resumeHeadingListEnd
\section{Projects}
\resumeHeadingListStart
  \resumeProjectHeading{\textbf{Diagnostics Prototype} \textbar{} TypeScript, React, Electron, SQLite}{\href{https://example.com/product}{Product Site}}
  \resumeItemListStart
    \resumeItem{Built a desktop diagnostics prototype combining simulated serial telemetry, guarded fault-code workflows, and SQLite session recording.}
    \resumeItem{Integrated validated, user-approved AI tools and prototyped retrieval-augmented generation (RAG) with hybrid search and page citations; physical testing remains pending.}
  \resumeItemListEnd
  \resumeProjectHeading{\textbf{Device Simulator} \textbar{} C++, Qt, Qt Charts}{\href{https://example.com/simulator-code}{GitHub} \textbar{} \href{https://example.com/simulator-demo}{Live Demo}}
  \resumeItemListStart
    \resumeItem{Implemented state transitions and tests in a team-built Qt device simulator, checking malformed inputs and recovery behavior with a simulated test harness.}
  \resumeItemListEnd
  \resumeProjectHeading{\textbf{Gesture Classifier} \textbar{} Python, TensorFlow, MediaPipe}{\href{https://example.com/classifier-code}{GitHub}}
  \resumeItemListStart
    \resumeItem{Developed a machine learning (ML) gesture-classification prototype using hand landmarks and TensorFlow; evaluated held-out examples and documented model limitations.}
  \resumeItemListEnd
\resumeHeadingListEnd
\section{Technical Skills}
\begin{itemize}[leftmargin=0.05in,label={},topsep=2pt]
  \item {\fontsize{10.5}{12.4}\selectfont
    \textbf{Languages:} Python, TypeScript, JavaScript, C++, SQL, HTML/CSS\\
    \textbf{Frameworks and Tools:} React, Electron, Qt, Qt Charts, TensorFlow, MediaPipe, Git, Linux\\
    \textbf{Databases and Cloud:} SQLite, MongoDB, PostgreSQL, Azure Blob Storage\\
    \textbf{Domains and Methods:} RAG, multithreading, testing, geospatial data, client collaboration
  }
\end{itemize}
\end{document}
"""


def run(argv):
    result = subprocess.run(argv, capture_output=True, text=True, errors="replace", timeout=60)
    if result.returncode:
        raise RuntimeError(f"{Path(argv[0]).name} failed: {(result.stdout + result.stderr)[-4000:]}")
    return result.stdout


def check(output_dir):
    names = ("pdflatex", "pdfinfo", "pdftotext", "pdftoppm")
    binaries = {name: shutil.which(name) for name in names}
    missing = [name for name, path in binaries.items() if path is None]
    if missing:
        raise RuntimeError("Optional template check requires: " + ", ".join(missing))
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    source = output_dir / "template-sample.tex"
    preamble = TEMPLATE.read_text(encoding="utf-8").split(r"\begin{document}", 1)[0]
    source.write_text(preamble + SAMPLE, encoding="utf-8")
    run([binaries["pdflatex"], "-interaction=nonstopmode", "-halt-on-error", "-no-shell-escape",
         "-output-directory=" + str(output_dir), str(source)])
    pdf = source.with_suffix(".pdf")
    info = run([binaries["pdfinfo"], str(pdf)])
    pages = re.search(r"^Pages:\s+(\d+)", info, re.MULTILINE)
    if not pages or int(pages[1]) != 1:
        raise RuntimeError("Synthetic sample did not render to exactly one page")
    log = source.with_suffix(".log").read_text(encoding="utf-8", errors="replace")
    if "Overfull" in log:
        raise RuntimeError("Template sample has an overfull box; inspect the log")
    text = run([binaries["pdftotext"], str(pdf), "-"])
    expected = ("Fictional Candidate", "Education", "Experience", "Software Developer", "Programmer",
                "Frontend Developer", "Projects", "Diagnostics Prototype", "Device Simulator",
                "Gesture Classifier", "Technical Skills")
    positions = [text.find(term) for term in expected]
    if -1 in positions or positions != sorted(positions):
        raise RuntimeError("Extracted section/role/project reading order was not preserved")
    if "Example Agency | Example Government" not in text or "sample@example.com" not in text:
        raise RuntimeError("Contact or separator extraction failed")
    if any(ord(char) < 32 and char not in "\n\r\t\f" for char in text):
        raise RuntimeError("Extracted text contains unexpected control characters")
    if not all(term in text.casefold() for term in ("workflows", "staff", "files", "classifier")):
        raise RuntimeError("Common words or ligatures did not extract correctly")
    source.with_suffix(".txt").write_text(text, encoding="utf-8")
    urls = run([binaries["pdfinfo"], "-url", str(pdf)])
    for url in re.findall(r"\\href\{([^}]+)\}", SAMPLE):
        if url not in urls:
            raise RuntimeError("Missing embedded destination: " + url)
    run([binaries["pdftoppm"], "-f", "1", "-singlefile", "-scale-to", "1600", "-png", str(pdf), str(output_dir / "template-sample")])
    return {"ok": True, "pages": 1, "overfull_boxes": False, "reading_order_checked": True,
            "embedded_links_checked": True, "visual_review_required": str(output_dir / "template-sample.png"),
            "scope": "Synthetic local check, not ATS certification or verification of candidate facts."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "tmp/template-check")
    args = parser.parse_args()
    try:
        result = check(args.output_dir)
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
