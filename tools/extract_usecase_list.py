"""Reads: references/ig1228/IG1228_*.pdf.
Writes: knowledge/index/usecase-list.json.
Track: assisted (spec.md 6.1) -- the source PDF requires a logged-in TM
Forum member session to download.

tools/extract_usecase_list.py -- IG1228 chapter 1 ("List of Use Cases") ->
knowledge/index/usecase-list.json: every TMFSxxx identifier the current
IG1228 knows about, with its title, its status *in IG1228* (not the same
as a document's own maturity/approval_status envelope field -- this is
just "Available" | "planned" | "not available", TM Forum's own roster
label), and any comment.

This is the roster chapter 2's matrix (extract_usecase_matrix.py) doesn't
have -- chapter 2 only lists use cases with component mappings already
filled in (24 of them in v31.0.0); chapter 1 lists every identifier TM
Forum has assigned at all, including ones marked "planned" or "not
available" with nothing to download yet. Phase 4 uses this to know which
identifiers are actually worth attempting the assisted download for.

A handful of rows need special handling, found while building this:
- TMFS019 is printed as a combined "TMFS019A\\nTMFS019B" identifier cell
  covering a Part I + Part II split -- normalized to the single id
  "TMFS019" (that's what's actually searchable in TM Forum's catalog;
  see tasks.md 4.2's runbook notes for how Part I/II resolve there).
- The row immediately after it, with a *blank* identifier cell describing
  "Part II: Detailed Modelling...", is that same entry's continuation,
  not a second use case -- skipped rather than creating a spurious
  blank-id row.
- TMFS015 doesn't appear in the table at all in v31.0.0 (not "not
  available" -- genuinely absent). That's expected, not a parse failure;
  don't treat a gap in the numbering as a bug to chase.

Usage:
    python extract_usecase_list.py [path/to/IG1228.pdf]
"""
import json
import os
import re
import sys

import pdfplumber

DEFAULT_PDF = os.path.join(
    os.path.dirname(__file__), "..", "references", "ig1228", "IG1228_How_to_use_ODA_Using_Open_APIs_to_Realize_UseCases_v31.0.0.pdf"
)
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "knowledge", "index", "usecase-list.json")

PAGE_START, PAGE_END = 6, 7  # 1-indexed, inclusive -- "1. List of Use Cases"
HEADER_ROWS = 2
COL_ID, COL_TITLE, COL_STATUS, COL_COMMENT = 0, 3, 4, 7
ID_RE = re.compile(r"TMFS\d+")


def clean(cell):
    return re.sub(r"\s+", " ", (cell or "").strip())


def main_table(page):
    tables = page.extract_tables()
    if not tables:
        return None
    return max(tables, key=lambda t: len(t[0]) if t else 0)


def build_list(pdf_path):
    entries = {}
    with pdfplumber.open(pdf_path) as pdf:
        for page_num in range(PAGE_START, PAGE_END + 1):
            table = main_table(pdf.pages[page_num - 1])
            if table is None:
                continue
            for row in table[HEADER_ROWS:]:
                raw_id = clean(row[COL_ID]) if COL_ID < len(row) else ""
                m = ID_RE.search(raw_id)
                if not m:
                    continue  # blank-identifier continuation row (e.g. TMFS019's Part II note) -- not a new entry
                uc_id = m.group(0)
                entries[uc_id] = {
                    "id": uc_id,
                    "title": clean(row[COL_TITLE]) if COL_TITLE < len(row) else "",
                    "status_in_ig1228": clean(row[COL_STATUS]) if COL_STATUS < len(row) else "",
                    "comment": clean(row[COL_COMMENT]) if COL_COMMENT < len(row) else "",
                }
    return dict(sorted(entries.items()))


def main():
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PDF
    entries = build_list(pdf_path)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(
            {
                "generated_from": "IG1228 v31.0.0, chapter 1 (\"List of Use Cases\")",
                "source_pdf": os.path.relpath(pdf_path, os.path.join(os.path.dirname(__file__), "..")).replace("\\", "/"),
                "use_cases": entries,
            },
            f,
            indent=2,
        )

    by_status = {}
    for e in entries.values():
        by_status.setdefault(e["status_in_ig1228"], []).append(e["id"])
    print(f"{len(entries)} identifiers -> {OUT_PATH}")
    for status, ids in sorted(by_status.items()):
        print(f"  {status}: {len(ids)} -- {', '.join(ids)}")


if __name__ == "__main__":
    main()
