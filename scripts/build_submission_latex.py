#!/usr/bin/env python3
"""Build BUET thesis LaTeX files from the Script Matters Markdown draft."""

from __future__ import annotations

import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "reports" / "script_matters_paper_draft.md"
THESIS_DIR = ROOT / "Thesis Template UG"
CHAPTER_DIR = THESIS_DIR / "chapters"
SEED_BIB = ROOT / "literature" / "references_seed.bib"

TITLE = "Script Matters: Measuring Latin-Script Banglish Robustness in Bangla LLMs"
STUDENT_NAME = "Munim Thahmid"
STUDENT_ID = "2005097"
SUPERVISOR_NAME = "Dr. Sadia Sharmin"
SUPERVISOR_DESIGNATION = "Associate Professor"
THESIS_DATE = "June 2026"


GROUPS = {
    1: ("01_introduction.tex", "Introduction", {1: None, 2: "Contributions"}),
    3: ("02_related_work.tex", "Related Work", {3: None}),
    4: (
        "03_benchmark_and_protocol.tex",
        "Benchmark Construction and Evaluation Protocol",
        {4: "Benchmark Construction", 5: "Evaluation Protocol"},
    ),
    6: (
        "04_main_results_and_robustness.tex",
        "Main Results and Robustness Checks",
        {
            6: "Main Result: Reviewed Banglish Remains Harder",
            7: "Review Sensitivity",
            8: "Tokenization Sensitivity",
        },
    ),
    9: ("05_failure_analysis.tex", "Failure Analysis", {9: None}),
    10: (
        "06_frontier_and_scale_boundary.tex",
        "Frontier and Scale Boundary",
        {
            10: "Frontier API Boundary",
            11: "BEnQA Scale Extension",
            12: "Natural Code-Mixed External Layer",
        },
    ),
    13: ("07_mitigation_attempts.tex", "Mitigation Attempts", {13: None}),
    14: (
        "08_discussion_limitations_artifacts.tex",
        "Discussion, Limitations, and Artifacts",
        {14: "Discussion", 15: "Limitations", 16: "Reproducibility and Artifacts"},
    ),
    17: ("09_conclusion.tex", "Conclusion", {17: None}),
}


def section_group(number: int) -> tuple[int, str, dict[int, str | None]]:
    starts = sorted(GROUPS)
    start = max(s for s in starts if s <= number)
    filename, chapter, section_titles = GROUPS[start]
    return start, chapter, section_titles


def strip_numbered_title(title: str) -> tuple[int | None, str]:
    match = re.match(r"^(\d+)\.\s+(.*)$", title)
    if not match:
        return None, title.strip()
    return int(match.group(1)), match.group(2).strip()


def strip_subsection_number(title: str) -> str:
    return re.sub(r"^\d+(?:\.\d+)+\s+", "", title).strip()


def latex_escape(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "<": r"\textless{}",
        ">": r"\textgreater{}",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


def convert_citation(match: re.Match[str]) -> str:
    body = match.group(1)
    keys = re.findall(r"@([A-Za-z0-9:_./-]+)", body)
    if not keys:
        return latex_escape(match.group(0))
    return r"\cite{" + ",".join(keys) + "}"


def inline_latex(text: str) -> str:
    placeholders: list[str] = []

    def hold(value: str) -> str:
        placeholders.append(value)
        return f"@@PLACEHOLDER{len(placeholders) - 1}@@"

    text = re.sub(r"\[([^\]]*@[^]]*)\]", lambda m: hold(convert_citation(m)), text)
    text = re.sub(
        r"`([^`]+)`",
        lambda m: hold(
            (r"\path{" + m.group(1).replace("\\", "/") + "}")
            if "/" in m.group(1)
            else (r"\texttt{" + latex_escape(m.group(1)) + "}")
        ),
        text,
    )
    text = re.sub(
        r"\*\*([^*]+)\*\*",
        lambda m: hold(r"\textbf{" + inline_latex(m.group(1)) + "}"),
        text,
    )
    escaped = latex_escape(text)
    for idx, value in enumerate(placeholders):
        escaped = escaped.replace(latex_escape(f"@@PLACEHOLDER{idx}@@"), value)
    return escaped


def split_table_row(row: str) -> list[str]:
    return [cell.strip() for cell in row.strip().strip("|").split("|")]


def render_table(lines: list[str], caption: str | None, index: int) -> list[str]:
    header = split_table_row(lines[0])
    rows = [split_table_row(line) for line in lines[2:]]
    if caption is None:
        joined_header = " | ".join(header)
        if "v4 Banglish" in joined_header:
            caption = "Review sensitivity from v4 Banglish to reviewed-v5 Banglish."
        elif "Strict policy" in joined_header:
            caption = "Strict-197 denominator sensitivity."
        elif "Correct script views" in joined_header:
            caption = "Example recoverable reviewed-Banglish misses from the BEnQA extension."
        else:
            caption = "Tabular result " + str(index)
    colspec = "l" * len(header)
    should_resize = len(header) >= 5
    out = [
        r"\begin{table}[H]",
        r"\centering",
    ]
    out.append(r"\caption{" + inline_latex(caption) + "}")
    out.append(r"\small")
    if should_resize:
        out.append(r"\resizebox{\textwidth}{!}{%")
    out.extend(
        [
            r"\begin{tabular}{" + colspec + r"}",
            r"\hline",
            " & ".join(inline_latex(cell) for cell in header) + r" \\",
            r"\hline",
        ]
    )
    for row in rows:
        padded = row + [""] * (len(header) - len(row))
        out.append(" & ".join(inline_latex(cell) for cell in padded[: len(header)]) + r" \\")
    out.extend([r"\hline", r"\end{tabular}%"])
    if should_resize:
        out.append(r"}")
    out.append(r"\end{table}")
    return out


def flush_paragraph(lines: list[str], out: list[str]) -> None:
    if not lines:
        return
    text = " ".join(line.strip() for line in lines).strip()
    if text:
        out.append(inline_latex(text))
        out.append("")
    lines.clear()


def convert_markdown(md: str) -> dict[str, list[str]]:
    content_by_file: dict[str, list[str]] = {}
    current_file: str | None = None
    current_section_number: int | None = None
    paragraph: list[str] = []
    pending_caption: str | None = None
    table_count = 0
    in_code = False
    in_itemize = False
    in_enumerate = False
    section_started_by_file: dict[str, bool] = {}

    def out() -> list[str]:
        if current_file is None:
            raise RuntimeError("No current chapter")
        return content_by_file[current_file]

    def close_lists() -> None:
        nonlocal in_itemize, in_enumerate
        if in_itemize:
            out().append(r"\end{itemize}")
            out().append("")
            in_itemize = False
        if in_enumerate:
            out().append(r"\end{enumerate}")
            out().append("")
            in_enumerate = False

    lines = md.splitlines()
    idx = 0
    while idx < len(lines):
        raw = lines[idx].rstrip()

        if raw.startswith("```"):
            flush_paragraph(paragraph, out() if current_file else [])
            if current_file:
                close_lists()
                out().append(r"\begin{verbatim}" if not in_code else r"\end{verbatim}")
                out().append("")
            in_code = not in_code
            idx += 1
            continue

        if in_code:
            if current_file:
                out().append(raw)
            idx += 1
            continue

        if raw.startswith("# ") or raw.startswith("Updated:") or raw.startswith("Draft status:"):
            idx += 1
            continue

        if raw.startswith("## Appendix"):
            break

        heading = re.match(r"^(#{2,4})\s+(.*)$", raw)
        if heading:
            if current_file:
                flush_paragraph(paragraph, out())
                close_lists()
            level = len(heading.group(1))
            number, title = strip_numbered_title(heading.group(2))
            title = strip_subsection_number(title)
            if level == 2 and number is not None:
                current_section_number = number
                start, chapter, section_titles = section_group(number)
                filename = GROUPS[start][0]
                if current_file != filename:
                    current_file = filename
                    content_by_file.setdefault(filename, [r"\chapter{" + inline_latex(chapter) + "}", ""])
                    section_started_by_file.setdefault(filename, False)
                section_title = section_titles.get(number, title)
                if section_title:
                    out().append(r"\section{" + inline_latex(section_title) + "}")
                    out().append("")
                    section_started_by_file[current_file] = True
            elif current_file:
                if level == 3 and not section_started_by_file.get(current_file, False):
                    cmd = r"\section"
                    section_started_by_file[current_file] = True
                else:
                    cmd = r"\subsection" if level == 3 else r"\subsubsection"
                out().append(cmd + "{" + inline_latex(title) + "}")
                out().append("")
            idx += 1
            continue

        if current_file is None:
            idx += 1
            continue

        if raw.strip() == "":
            flush_paragraph(paragraph, out())
            next_nonempty = ""
            for future in lines[idx + 1 :]:
                if future.strip():
                    next_nonempty = future
                    break
            if in_itemize and not re.match(r"^-\s+", next_nonempty):
                close_lists()
            elif in_enumerate and not re.match(r"^\d+\.\s+", next_nonempty):
                close_lists()
            elif not in_itemize and not in_enumerate:
                close_lists()
            idx += 1
            continue

        if raw.startswith("|") and idx + 1 < len(lines) and lines[idx + 1].lstrip().startswith("| ---"):
            flush_paragraph(paragraph, out())
            close_lists()
            table_lines = [raw, lines[idx + 1].rstrip()]
            idx += 2
            while idx < len(lines) and lines[idx].lstrip().startswith("|"):
                table_lines.append(lines[idx].rstrip())
                idx += 1
            table_count += 1
            out().extend(render_table(table_lines, pending_caption, table_count))
            out().append("")
            pending_caption = None
            continue

        if raw.startswith("**Table"):
            flush_paragraph(paragraph, out())
            caption_text = raw
            while "**" not in caption_text[2:] and idx + 1 < len(lines):
                idx += 1
                caption_text += " " + lines[idx].strip()
            caption_match = re.match(r"^\*\*Table\s+\d+\.\s*(.*?)\*\*(.*)$", caption_text)
            if caption_match:
                pending_caption = caption_match.group(1).strip().rstrip(".")
                trailing = caption_match.group(2).strip()
                if trailing:
                    paragraph.append(trailing)
            idx += 1
            continue

        bullet = re.match(r"^-\s+(.*)$", raw)
        if bullet:
            flush_paragraph(paragraph, out())
            if not in_itemize:
                close_lists()
                out().append(r"\begin{itemize}")
                in_itemize = True
            out().append(r"\item " + inline_latex(bullet.group(1)))
            idx += 1
            continue

        numbered = re.match(r"^\d+\.\s+(.*)$", raw)
        if numbered and current_section_number == 2:
            flush_paragraph(paragraph, out())
            if not in_enumerate:
                close_lists()
                out().append(r"\begin{enumerate}")
                in_enumerate = True
            out().append(r"\item " + inline_latex(numbered.group(1)))
            idx += 1
            continue

        paragraph.append(raw)
        idx += 1

    if current_file:
        flush_paragraph(paragraph, out())
        close_lists()
    return content_by_file


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    source = SOURCE.read_text(encoding="utf-8")
    source = re.sub(r"\bThis\s+paper\b", "This thesis", source)
    source = re.sub(r"\bthis\s+paper\b", "this thesis", source)
    source = re.sub(r"\bThe\s+paper\b", "The thesis", source)
    source = re.sub(r"\bthe\s+paper\b", "the thesis", source)
    chapters = convert_markdown(source)
    CHAPTER_DIR.mkdir(exist_ok=True)

    for filename, lines in chapters.items():
        write_text(CHAPTER_DIR / filename, "\n".join(lines) + "\n\\endinput")

    write_text(THESIS_DIR / "parameters" / "students.txt", f"{STUDENT_NAME}, {STUDENT_ID}")
    write_text(
        THESIS_DIR / "parameters" / "supervisor.txt",
        f"{SUPERVISOR_NAME}, {SUPERVISOR_DESIGNATION}",
    )
    write_text(THESIS_DIR / "parameters" / "thesistitle.txt", TITLE)
    write_text(THESIS_DIR / "parameters" / "thesisdate.txt", THESIS_DATE)

    abstract = r"""
% Do not change these lines
\renewcommand{\abstractname}{\textbf{{\Large ABSTRACT}}}
\addcontentsline{toc}{chapter}{\textbf{\normalsize{\emph{ABSTRACT}}}}

\begin{abstract}\thispagestyle{plain}
Bangla users do not always meet language models through the script assumed by
standard benchmarks. The same Bengali question may be typed in native Bengali
script, in English, or in Latin-script Banglish. Recent Bengali benchmarks
increasingly cover knowledge, education, culture, inference, and social
interaction, but they rarely isolate this script choice while holding the
underlying task and answer fixed. This thesis studies whether orthography
itself changes large language model behavior. We construct controlled Bangla,
reviewed Banglish, and English variants of curriculum-style QA and math items
drawn from BEnQA and BanglaMATH, and evaluate models under a paired item-level
protocol.

On a 200-item validation slice, compact Qwen models show a consistent
reviewed-Banglish deficit. Qwen2.5-3B scores 54/200 in Bangla but 41/200 in
reviewed Banglish, Qwen2.5-7B 8-bit scores 65/200 versus 47/200, and Qwen3-4B
scores 80/200 versus 49/200. The gap is not explained by token count alone,
since reviewed Banglish is token-cheaper than native Bangla for the audited
Qwen tokenizers. A frozen v5 review of high-impact Banglish rows changes scores
by at most two items, improving benchmark quality without removing the
script-conditioned weakness.

Hosted-model and scale checks clarify the boundary. GPT-5.5 low nearly closes
the validation-200 gap under secondary scoring, while Claude Sonnet 4.6,
DeepSeek V4 Flash, and Groq-hosted Llama 3.3 70B preserve reviewed-Banglish
deficits under the same protocol. An 851-row BEnQA silver extension reproduces
the English greater-than Bangla greater-than reviewed Banglish ordering for
Qwen2.5-3B and DeepSeek V4 Flash. Mitigation remains model-dependent:
self-normalization helps one Qwen model and hurts another, and generated
alternate-script views require preservation gates before they can support a
deployable routing claim. Overall, the thesis shows that Latin-script Banglish
is an undermeasured orthographic robustness challenge for Bangla LLM use. It is
a real access path for Bangla users, and its reliability must be measured
directly rather than assumed from native-script Bangla or English performance.
\end{abstract}

\endinput
"""
    write_text(THESIS_DIR / "buetcseugthesisabstract.tex", abstract)

    acknowledgement = r"""
% Do not chage this part
\begin{center}
  \textbf{{\Large ACKNOWLEDGEMENT}}\\[60pt]
\end{center}
\addcontentsline{toc}{chapter}{\textbf{\normalsize{\emph{ACKNOWLEDGEMENT}}}}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

I am deeply grateful to my supervisor, Dr. Sadia Sharmin, for her guidance,
feedback, and support throughout this thesis. Her advice helped shape the
problem framing, experimental discipline, and interpretation of the results.

I also thank the Department of Computer Science and Engineering, Bangladesh
University of Engineering and Technology, for providing the academic environment
in which this work was carried out.

Finally, I am thankful to my family, friends, and peers for their patience and
encouragement during the research and writing process.

\vspace*{20.0mm}

\begin{minipage}[t]{0.2\textwidth}
  Dhaka\par
  \thesisdate
\end{minipage}%
\hfill
\begin{minipage}[t]{0.45\textwidth}
  \begin{enumerate}
    \vspace{-0.75\baselineskip}
    \DTLforeach{ThesisStudents}{\StudentName=Column1}{\item[]\StudentName}
  \end{enumerate}
\end{minipage}

\endinput
"""
    write_text(THESIS_DIR / "buetcseugthesisacknowledgement.tex", acknowledgement)

    main_tex = r"""
\documentclass[12pt,notitlepage,oneside]{report}

\usepackage{buetcseugthesis}

% This thesis currently contains no figure or algorithm environments.
\suppresslistoffigures
\suppresslistofalgorithms

% Allow long artifact paths and model names to wrap without changing the template.
\makeatletter
\g@addto@macro\UrlBreaks{\do\_\do\-}
\makeatother
\def\UrlFont{\footnotesize\ttfamily}
\setlength{\emergencystretch}{3em}

\begin{document}

\input{chapters/01_introduction.tex}
\input{chapters/02_related_work.tex}
\input{chapters/03_benchmark_and_protocol.tex}
\input{chapters/04_main_results_and_robustness.tex}
\input{chapters/05_failure_analysis.tex}
\input{chapters/06_frontier_and_scale_boundary.tex}
\input{chapters/07_mitigation_attempts.tex}
\input{chapters/08_discussion_limitations_artifacts.tex}
\input{chapters/09_conclusion.tex}

\input{buetcseugthesisbibliography.tex}

\end{document}
"""
    write_text(THESIS_DIR / "buetcseugthesis.tex", main_tex)

    shutil.copyfile(SEED_BIB, THESIS_DIR / "buetcseugthesis.bib")
    print(f"wrote {len(chapters)} thesis chapters under {CHAPTER_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
