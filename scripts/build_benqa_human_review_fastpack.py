#!/usr/bin/env python3
"""Build a fast human-review dashboard for the BEnQA 1,000-row extension.

The dashboard is a static HTML file. It does not modify the source data.
Reviewer decisions are stored in browser localStorage and exported as JSONL/CSV.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data/slices/benqa_extended_1000_v1_ai_reviewed.jsonl"
DEFAULT_OUT_DIR = ROOT / "reports/benqa_ext_human_review_fast"
DEFAULT_QUEUE = ROOT / "results/analysis/benqa_extended_1000_v1_human_review_queue.csv"
DEFAULT_TEMPLATE = ROOT / "results/analysis/benqa_extended_1000_v1_human_review_template.csv"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def repo_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def metadata(row: dict[str, Any]) -> dict[str, Any]:
    value = row.get("metadata")
    return value if isinstance(value, dict) else {}


def ai_review(row: dict[str, Any]) -> dict[str, Any]:
    value = metadata(row).get("ai_assisted_review")
    return value if isinstance(value, dict) else {}


def subject(row: dict[str, Any]) -> str:
    return str(metadata(row).get("subject") or row.get("domain") or "unknown")


def row_priority(row: dict[str, Any]) -> tuple[int, int, str, str]:
    review = ai_review(row)
    warnings = review.get("warnings") if isinstance(review.get("warnings"), list) else []
    issues = review.get("issues") if isinstance(review.get("issues"), list) else []
    status = str(row.get("quality_status") or "")
    if issues or "fail" in status:
        tier = 0
    elif warnings or "warn" in status:
        tier = 1
    else:
        tier = 2
    return (tier, -len(warnings), subject(row), str(row.get("id") or ""))


def review_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sorted_rows = sorted(rows, key=row_priority)
    prepared: list[dict[str, Any]] = []
    for index, row in enumerate(sorted_rows, start=1):
        review = ai_review(row)
        warnings = review.get("warnings") if isinstance(review.get("warnings"), list) else []
        issues = review.get("issues") if isinstance(review.get("issues"), list) else []
        prepared.append(
            {
                "queue_index": index,
                "id": row.get("id", ""),
                "source_file": row.get("source_file", ""),
                "source_row": row.get("source_row", ""),
                "grade": metadata(row).get("grade", ""),
                "subject": subject(row),
                "answer": row.get("answer", ""),
                "quality_status": row.get("quality_status", ""),
                "warnings": warnings,
                "issues": issues,
                "bangla": row.get("bangla", ""),
                "banglish": row.get("banglish_clean", ""),
                "english": row.get("english", ""),
                "priority": "warning" if warnings else "pass",
            }
        )
    return prepared


def write_csvs(queue_path: Path, template_path: Path, rows: list[dict[str, Any]]) -> None:
    queue_path.parent.mkdir(parents=True, exist_ok=True)
    template_path.parent.mkdir(parents=True, exist_ok=True)
    queue_fields = [
        "queue_index",
        "id",
        "subject",
        "grade",
        "answer",
        "priority",
        "quality_status",
        "warnings",
        "source_file",
        "source_row",
    ]
    with queue_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=queue_fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    field: (";".join(row[field]) if isinstance(row.get(field), list) else row.get(field, ""))
                    for field in queue_fields
                }
            )

    template_fields = [
        "queue_index",
        "id",
        "decision",
        "reviewed_banglish",
        "notes",
        "subject",
        "answer",
        "quality_status",
        "warnings",
    ]
    with template_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=template_fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "queue_index": row["queue_index"],
                    "id": row["id"],
                    "decision": "",
                    "reviewed_banglish": row["banglish"],
                    "notes": "",
                    "subject": row["subject"],
                    "answer": row["answer"],
                    "quality_status": row["quality_status"],
                    "warnings": ";".join(row["warnings"]),
                }
            )


def dashboard_html(rows: list[dict[str, Any]]) -> str:
    payload = json.dumps(rows, ensure_ascii=False).replace("</", "<\\/")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BEnQA 1000 Human Review</title>
<style>
:root {{
  --bg: #f7f7f4;
  --panel: #ffffff;
  --ink: #171717;
  --muted: #666666;
  --line: #d9d9d2;
  --warn: #8a4b00;
  --warn-bg: #fff4db;
  --ok: #0f6b3d;
  --bad: #9a1f1f;
  --focus: #1455d9;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: Arial, Helvetica, sans-serif;
  font-size: 14px;
}}
header {{
  position: sticky;
  top: 0;
  z-index: 5;
  background: var(--panel);
  border-bottom: 1px solid var(--line);
  padding: 10px 14px;
}}
.topline {{
  display: grid;
  grid-template-columns: minmax(240px, 1fr) auto;
  gap: 12px;
  align-items: center;
}}
h1 {{
  margin: 0;
  font-size: 18px;
  letter-spacing: 0;
}}
.stats {{
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  justify-content: flex-end;
}}
.pill {{
  border: 1px solid var(--line);
  border-radius: 4px;
  padding: 4px 7px;
  background: #fafafa;
  white-space: nowrap;
}}
.toolbar {{
  display: grid;
  grid-template-columns: 1fr auto auto auto;
  gap: 8px;
  margin-top: 10px;
  align-items: center;
}}
input, select, textarea, button {{
  font: inherit;
}}
input, select, textarea {{
  border: 1px solid var(--line);
  border-radius: 4px;
  padding: 7px 8px;
  background: #fff;
}}
button {{
  border: 1px solid var(--line);
  border-radius: 4px;
  padding: 7px 10px;
  background: #fff;
  cursor: pointer;
}}
button:hover {{ border-color: #999; }}
button.primary {{ background: #111; color: white; border-color: #111; }}
button.ok {{ background: #eaf7ef; border-color: #abd6bd; color: var(--ok); }}
button.edit {{ background: #edf3ff; border-color: #b7caff; color: var(--focus); }}
button.reject {{ background: #fff0f0; border-color: #e3b1b1; color: var(--bad); }}
main {{
  max-width: 1280px;
  margin: 0 auto;
  padding: 14px;
}}
.guide {{
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 10px 12px;
  margin-bottom: 12px;
  line-height: 1.45;
}}
.guide b {{ color: #000; }}
.card {{
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 6px;
  margin-bottom: 12px;
  overflow: hidden;
}}
.cardHead {{
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 10px;
  padding: 10px 12px;
  border-bottom: 1px solid var(--line);
  background: #fbfbfa;
}}
.title {{
  font-weight: 700;
}}
.meta {{
  color: var(--muted);
  margin-top: 4px;
  font-size: 13px;
}}
.badges {{
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  justify-content: flex-end;
}}
.badge {{
  border-radius: 4px;
  padding: 3px 6px;
  font-size: 12px;
  border: 1px solid var(--line);
  background: #f7f7f7;
}}
.badge.warn {{ color: var(--warn); background: var(--warn-bg); border-color: #e2c06d; }}
.badge.done {{ color: var(--ok); background: #eef8f1; border-color: #b8dac4; }}
.badge.reject {{ color: var(--bad); background: #fff0f0; border-color: #e3b1b1; }}
.body {{
  padding: 12px;
}}
.columns {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}}
.panel {{
  min-width: 0;
}}
.label {{
  display: flex;
  justify-content: space-between;
  gap: 8px;
  color: var(--muted);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0;
  margin-bottom: 5px;
}}
pre {{
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  margin: 0;
  border: 1px solid var(--line);
  border-radius: 4px;
  padding: 8px;
  background: #fff;
  min-height: 130px;
  line-height: 1.35;
}}
textarea.banglish {{
  width: 100%;
  min-height: 180px;
  resize: vertical;
  line-height: 1.35;
}}
details {{
  margin-top: 10px;
}}
summary {{
  cursor: pointer;
  color: var(--muted);
}}
.actions {{
  display: grid;
  grid-template-columns: repeat(5, auto) 1fr;
  gap: 8px;
  margin-top: 12px;
  align-items: center;
}}
.notes {{
  width: 100%;
}}
.hidden {{ display: none; }}
@media (max-width: 820px) {{
  .topline, .toolbar, .columns, .actions {{
    grid-template-columns: 1fr;
  }}
  .stats {{ justify-content: flex-start; }}
}}
</style>
</head>
<body>
<header>
  <div class="topline">
    <h1>BEnQA 1,000 Human Review</h1>
    <div class="stats" id="stats"></div>
  </div>
  <div class="toolbar">
    <input id="search" type="search" placeholder="Search id, subject, warning, text">
    <select id="filter">
      <option value="todo">Todo first</option>
      <option value="warning">Warnings only</option>
      <option value="pass">Pass rows only</option>
      <option value="all">All rows</option>
      <option value="accepted">Accepted</option>
      <option value="edited">Edited</option>
      <option value="rejected">Rejected</option>
      <option value="unsure">Unsure</option>
    </select>
    <button id="exportJson" class="primary">Export JSONL</button>
    <button id="exportCsv">Export CSV</button>
  </div>
</header>
<main>
  <section class="guide">
    <b>Blitz rule:</b> accept if Banglish preserves the question, A-D options, digits/formulas, answer label, and answer instruction.
    Edit only the Banglish text when the fix is obvious. Reject if the meaning, option mapping, or formula/digit content is uncertain.
    Shortcuts: <b>A</b> accept, <b>E</b> edited, <b>R</b> reject, <b>U</b> unsure, <b>N</b> next, <b>P</b> previous.
  </section>
  <section id="cards"></section>
</main>
<script id="rows-data" type="application/json">{payload}</script>
<script>
const rows = JSON.parse(document.getElementById('rows-data').textContent);
const storageKey = 'benqa_ext_1000_human_review_v1';
let decisions = loadDecisions();
let visibleRows = [];

function loadDecisions() {{
  try {{
    return JSON.parse(localStorage.getItem(storageKey) || '{{}}');
  }} catch {{
    return {{}};
  }}
}}

function saveDecisions() {{
  localStorage.setItem(storageKey, JSON.stringify(decisions));
  renderStats();
}}

function defaultDecision(row) {{
  return {{
    id: row.id,
    queue_index: row.queue_index,
    decision: '',
    reviewed_banglish: row.banglish,
    notes: '',
    reviewed_at_local: ''
  }};
}}

function getDecision(row) {{
  if (!decisions[row.id]) decisions[row.id] = defaultDecision(row);
  return decisions[row.id];
}}

function setDecision(row, value) {{
  const d = getDecision(row);
  d.decision = value;
  d.reviewed_at_local = new Date().toISOString();
  const text = document.getElementById('banglish-' + row.queue_index);
  const notes = document.getElementById('notes-' + row.queue_index);
  if (text) d.reviewed_banglish = text.value;
  if (notes) d.notes = notes.value;
  decisions[row.id] = d;
  saveDecisions();
  renderOne(row);
}}

function escapeHtml(text) {{
  return String(text ?? '').replace(/[&<>"']/g, c => ({{
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }}[c]));
}}

function decisionBadge(decision) {{
  if (!decision) return '<span class="badge">todo</span>';
  const cls = decision === 'reject' ? 'reject' : 'done';
  return '<span class="badge ' + cls + '">' + escapeHtml(decision) + '</span>';
}}

function rowMatches(row, filter, query) {{
  const d = getDecision(row);
  if (filter === 'warning' && row.priority !== 'warning') return false;
  if (filter === 'pass' && row.priority !== 'pass') return false;
  if (filter === 'accepted' && d.decision !== 'accept') return false;
  if (filter === 'edited' && d.decision !== 'edited') return false;
  if (filter === 'rejected' && d.decision !== 'reject') return false;
  if (filter === 'unsure' && d.decision !== 'unsure') return false;
  if (filter === 'todo' && d.decision) return false;
  if (!query) return true;
  const haystack = [
    row.id, row.subject, row.grade, row.answer, row.quality_status,
    row.warnings.join(' '), row.issues.join(' '), row.bangla, row.banglish, row.english
  ].join(' ').toLowerCase();
  return haystack.includes(query.toLowerCase());
}}

function filteredRows() {{
  const filter = document.getElementById('filter').value;
  const query = document.getElementById('search').value.trim();
  return rows.filter(row => rowMatches(row, filter, query));
}}

function renderStats() {{
  const counts = {{ accept: 0, edited: 0, reject: 0, unsure: 0, todo: 0 }};
  for (const row of rows) {{
    const decision = getDecision(row).decision;
    if (decision && counts[decision] !== undefined) counts[decision] += 1;
    else counts.todo += 1;
  }}
  const warningTotal = rows.filter(r => r.priority === 'warning').length;
  document.getElementById('stats').innerHTML = [
    ['Rows', rows.length],
    ['Warnings', warningTotal],
    ['Todo', counts.todo],
    ['Accept', counts.accept],
    ['Edited', counts.edited],
    ['Reject', counts.reject],
    ['Unsure', counts.unsure]
  ].map(([k, v]) => '<span class="pill">' + k + ': <b>' + v + '</b></span>').join('');
}}

function cardHtml(row) {{
  const d = getDecision(row);
  const warningBadges = row.warnings.map(w => '<span class="badge warn">' + escapeHtml(w) + '</span>').join('');
  const issueBadges = row.issues.map(w => '<span class="badge reject">' + escapeHtml(w) + '</span>').join('');
  return `
  <article class="card" id="card-${{row.queue_index}}">
    <div class="cardHead">
      <div>
        <div class="title">${{row.queue_index}}. ${{escapeHtml(row.id)}} ${{decisionBadge(d.decision)}}</div>
        <div class="meta">${{escapeHtml(row.subject)}} | grade ${{escapeHtml(row.grade)}} | answer ${{escapeHtml(row.answer)}} | ${{escapeHtml(row.quality_status)}}</div>
      </div>
      <div class="badges">${{warningBadges || '<span class="badge">ai-pass</span>'}}${{issueBadges}}</div>
    </div>
    <div class="body">
      <div class="columns">
        <div class="panel">
          <div class="label"><span>Bangla source</span><span>do not edit</span></div>
          <pre>${{escapeHtml(row.bangla)}}</pre>
        </div>
        <div class="panel">
          <div class="label"><span>Reviewed Banglish</span><span>edit only if needed</span></div>
          <textarea class="banglish" id="banglish-${{row.queue_index}}">${{escapeHtml(d.reviewed_banglish || row.banglish)}}</textarea>
        </div>
      </div>
      <details>
        <summary>English reference and source metadata</summary>
        <pre>${{escapeHtml(row.english)}}</pre>
        <div class="meta">Source: ${{escapeHtml(row.source_file)}}:${{escapeHtml(row.source_row)}}</div>
      </details>
      <div class="actions">
        <button class="ok" onclick="setDecisionByIndex(${{row.queue_index}}, 'accept')">A Accept</button>
        <button class="edit" onclick="setDecisionByIndex(${{row.queue_index}}, 'edited')">E Edited</button>
        <button class="reject" onclick="setDecisionByIndex(${{row.queue_index}}, 'reject')">R Reject</button>
        <button onclick="setDecisionByIndex(${{row.queue_index}}, 'unsure')">U Unsure</button>
        <button onclick="clearDecisionByIndex(${{row.queue_index}})">Clear</button>
        <input class="notes" id="notes-${{row.queue_index}}" value="${{escapeHtml(d.notes || '')}}" placeholder="Optional note">
      </div>
    </div>
  </article>`;
}}

function renderOne(row) {{
  const old = document.getElementById('card-' + row.queue_index);
  if (!old) return;
  old.outerHTML = cardHtml(row);
}}

function render() {{
  visibleRows = filteredRows();
  document.getElementById('cards').innerHTML = visibleRows.map(cardHtml).join('');
  renderStats();
}}

function setDecisionByIndex(index, decision) {{
  const row = rows.find(r => r.queue_index === index);
  if (row) setDecision(row, decision);
}}

function clearDecisionByIndex(index) {{
  const row = rows.find(r => r.queue_index === index);
  if (!row) return;
  decisions[row.id] = defaultDecision(row);
  saveDecisions();
  renderOne(row);
}}

function focusRelative(delta) {{
  const cards = Array.from(document.querySelectorAll('.card'));
  if (!cards.length) return;
  const top = window.scrollY + 80;
  let idx = cards.findIndex(card => card.offsetTop >= top);
  if (idx < 0) idx = cards.length - 1;
  idx = Math.max(0, Math.min(cards.length - 1, idx + delta));
  cards[idx].scrollIntoView({{ behavior: 'smooth', block: 'start' }});
}}

function activeRow() {{
  const cards = Array.from(document.querySelectorAll('.card'));
  const top = window.scrollY + 90;
  let active = cards[0];
  for (const card of cards) {{
    if (card.offsetTop <= top) active = card;
  }}
  if (!active) return null;
  const index = Number(active.id.replace('card-', ''));
  return rows.find(r => r.queue_index === index);
}}

function updateActiveText() {{
  const row = activeRow();
  if (!row) return;
  const d = getDecision(row);
  const text = document.getElementById('banglish-' + row.queue_index);
  const notes = document.getElementById('notes-' + row.queue_index);
  if (text) d.reviewed_banglish = text.value;
  if (notes) d.notes = notes.value;
  decisions[row.id] = d;
  saveDecisions();
}}

function reviewedRecords() {{
  return rows.map(row => {{
    const d = getDecision(row);
    return {{
      queue_index: row.queue_index,
      id: row.id,
      decision: d.decision || '',
      reviewed_banglish: d.reviewed_banglish || row.banglish,
      notes: d.notes || '',
      subject: row.subject,
      answer: row.answer,
      quality_status: row.quality_status,
      warnings: row.warnings,
      reviewed_at_local: d.reviewed_at_local || ''
    }};
  }});
}}

function download(filename, text, type) {{
  const blob = new Blob([text], {{ type }});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}}

function exportJsonl() {{
  updateActiveText();
  const text = reviewedRecords().map(r => JSON.stringify(r)).join('\\n') + '\\n';
  download('benqa_extended_1000_v1_human_review_decisions.jsonl', text, 'application/jsonl');
}}

function csvEscape(value) {{
  const text = Array.isArray(value) ? value.join(';') : String(value ?? '');
  return '"' + text.replace(/"/g, '""') + '"';
}}

function exportCsv() {{
  updateActiveText();
  const fields = ['queue_index','id','decision','reviewed_banglish','notes','subject','answer','quality_status','warnings','reviewed_at_local'];
  const lines = [fields.join(',')];
  for (const record of reviewedRecords()) {{
    lines.push(fields.map(f => csvEscape(record[f])).join(','));
  }}
  download('benqa_extended_1000_v1_human_review_decisions.csv', lines.join('\\n') + '\\n', 'text/csv');
}}

document.getElementById('search').addEventListener('input', render);
document.getElementById('filter').addEventListener('change', render);
document.getElementById('exportJson').addEventListener('click', exportJsonl);
document.getElementById('exportCsv').addEventListener('click', exportCsv);
document.addEventListener('keydown', event => {{
  const tag = document.activeElement.tagName.toLowerCase();
  if ((tag === 'textarea' || tag === 'input') && !event.altKey) return;
  const row = activeRow();
  if (!row) return;
  const key = event.key.toLowerCase();
  if (key === 'a') {{ setDecision(row, 'accept'); event.preventDefault(); }}
  if (key === 'e') {{ setDecision(row, 'edited'); event.preventDefault(); }}
  if (key === 'r') {{ setDecision(row, 'reject'); event.preventDefault(); }}
  if (key === 'u') {{ setDecision(row, 'unsure'); event.preventDefault(); }}
  if (key === 'n') {{ updateActiveText(); focusRelative(1); event.preventDefault(); }}
  if (key === 'p') {{ updateActiveText(); focusRelative(-1); event.preventDefault(); }}
}});
window.addEventListener('beforeunload', updateActiveText);
render();
</script>
</body>
</html>
"""


def write_readme(path: Path, input_path: Path, rows: list[dict[str, Any]], queue: Path, template: Path) -> None:
    counts = Counter(row["priority"] for row in rows)
    lines = [
        "# BEnQA 1,000 Human Review Fastpack",
        "",
        f"Updated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Purpose",
        "",
        "This fastpack is for converting the BEnQA 1,000-row extension from",
        "AI-assisted triage into a human-reviewed extension. It is designed for",
        "fast row-by-row review without hiding quality checks.",
        "",
        "## Files",
        "",
        f"- Dashboard: `{repo_path(path / 'index.html')}`",
        f"- Source rows: `{repo_path(input_path)}`",
        f"- Review queue CSV: `{repo_path(queue)}`",
        f"- Spreadsheet template: `{repo_path(template)}`",
        "",
        "## Counts",
        "",
        f"- Total rows: {len(rows)}",
        f"- AI-warning rows shown first: {counts.get('warning', 0)}",
        f"- AI-pass rows after warnings: {counts.get('pass', 0)}",
        "",
        "## Blitz Protocol",
        "",
        "1. Open `index.html` in a browser.",
        "2. Start with the default `Todo first` filter; rows with AI warnings are already first.",
        "3. For each row, compare Bangla source against Banglish.",
        "4. Accept if question, options, digits/formulas, answer label, and answer instruction are preserved.",
        "5. Edit only the Banglish field when the fix is obvious.",
        "6. Reject if option mapping, formula/digit content, or meaning is uncertain.",
        "7. Export JSONL when done or at every break.",
        "",
        "Keyboard shortcuts: `A` accept, `E` edited, `R` reject, `U` unsure, `N` next, `P` previous.",
        "",
        "## Freeze Rule",
        "",
        "The extension should only be called human-reviewed after every row has a",
        "human decision and the exported JSONL is used to build a frozen reviewed",
        "slice. Rows marked `reject` or `unsure` should not enter the gold extension.",
        "",
    ]
    path.mkdir(parents=True, exist_ok=True)
    (path / "README.md").write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raw_rows = load_jsonl(args.input)
    rows = review_rows(raw_rows)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    index_path = args.out_dir / "index.html"
    index_path.write_text(dashboard_html(rows), encoding="utf-8")
    write_csvs(args.queue, args.template, rows)
    write_readme(args.out_dir, args.input, rows, args.queue, args.template)
    counts = Counter(row["priority"] for row in rows)
    print(f"rows={len(rows)} warning={counts.get('warning', 0)} pass={counts.get('pass', 0)}")
    print(f"dashboard={repo_path(index_path)}")
    print(f"queue={repo_path(args.queue)}")
    print(f"template={repo_path(args.template)}")


if __name__ == "__main__":
    main()
