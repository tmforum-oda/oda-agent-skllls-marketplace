"""tools/extract_usecase_matrix.py -- IG1228 chapter 2 ("Components identified
per use-case") -> knowledge/index/usecase-component-matrix.json (spec/spec.md
5.4). Re-implements, as a real script, the pdfplumber extraction of this table
done by hand once during the research phase.

The table is split across three "Parts" (TM Forum's own print-width split,
one PDF page range each), and -- found while writing this, not assumed --
**the three parts do not share one column layout**. Part 1 has the component
identifier at column 6; Part 2, visually similar, has it at column 4; Part 3
uses a different header structure again (2 header rows, not 3). Hardcoding
one set of column positions for the whole table would have silently
misparsed two of the three parts. Each part's layout is declared explicitly
below, derived by inspecting real extracted rows, not guessed -- and
validated with assertions at parse time (the identifier column's header
must contain "identifier", the status column's must contain "status", every
use-case column header must match TMFSxxx) specifically so that if TM Forum
reformats this table in a future release, this script fails loudly at the
assertion instead of silently writing wrong data into the matrix. That is
the whole point of hardcoding per-part configs instead of trying to be
clever about detecting them -- a wrong guess here is worse than a crash.

Usage:
    python extract_usecase_matrix.py [path/to/IG1228.pdf]
"""
import json
import os
import re
import sys

import pdfplumber

DEFAULT_PDF = os.path.join(
    os.path.dirname(__file__), "..", "references", "ig1228", "IG1228_How_to_use_ODA_Using_Open_APIs_to_Realize_UseCases_v31.0.0.pdf"
)
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "knowledge", "index", "usecase-component-matrix.json")

# page_start/page_end are 1-indexed, inclusive, matching the printed page numbers.
PART_CONFIGS = [
    {
        "name": "Part 1",
        "page_start": 9,
        "page_end": 16,
        "header_rows": 3,
        "col_functional_block": 0,
        "col_component_name": 3,
        "col_component_id": 6,
        "col_status": 9,
        "usecase_start_col": 10,
    },
    {
        "name": "Part 2",
        "page_start": 17,
        "page_end": 22,
        "header_rows": 3,
        "col_functional_block": 0,
        "col_component_name": 3,
        "col_component_id": 4,
        "col_status": 7,
        "usecase_start_col": 8,
    },
    {
        "name": "Part 3",
        "page_start": 23,
        "page_end": 26,
        "header_rows": 2,
        "col_functional_block": 0,
        "col_component_name": 1,
        "col_component_id": 2,
        "col_status": 5,
        "usecase_start_col": 6,
    },
]

COMPONENT_ID_RE = re.compile(r"^TMFC\d+$")
USECASE_ID_RE = re.compile(r"^TMFS\d+$")


def clean(cell):
    return re.sub(r"\s+", " ", (cell or "").strip())


def joined_no_space(cell):
    """For header cells split across lines mid-word ('TMF\\nS002') -- strip all
    whitespace rather than collapsing it, so the id reads back as one token."""
    return re.sub(r"\s+", "", cell or "")


def main_table(page):
    tables = page.extract_tables()
    if not tables:
        return None
    return max(tables, key=lambda t: len(t[0]) if t else 0)


def header_column_text(rows, header_rows, col):
    return " ".join(clean(rows[r][col]) for r in range(header_rows) if col < len(rows[r]))


def extract_part(pdf, config):
    usecase_columns = None  # {col_index: usecase_id}, fixed once from the first page's header
    rows_out = []

    for page_num in range(config["page_start"], config["page_end"] + 1):
        page = pdf.pages[page_num - 1]
        table = main_table(page)
        if table is None:
            continue

        if usecase_columns is None:
            # Found while building this: pdfplumber's merged-cell reconstruction shifts the
            # *header's* column boundary by one relative to the *data* rows for some of these
            # multi-row-spanning header cells (confirmed directly: "Identifier"'s header text
            # sits one column to the right of where TMFCxxx values actually land in data rows;
            # "Status" doesn't drift the same way). A window rather than an exact index absorbs
            # that real, observed off-by-one without giving up the "fail loudly on real drift"
            # guarantee -- a genuine format change won't land the right keyword anywhere nearby.
            id_header = " ".join(
                header_column_text(table, config["header_rows"], c)
                for c in range(max(0, config["col_component_id"] - 1), config["col_component_id"] + 2)
            )
            status_header = " ".join(
                header_column_text(table, config["header_rows"], c)
                for c in range(max(0, config["col_status"] - 1), config["col_status"] + 2)
            )
            assert "identifier" in id_header.lower(), (
                f"{config['name']} p{page_num}: expected 'Identifier' near column {config['col_component_id']}'s "
                f"header, got {id_header!r} -- table layout has changed, column mapping needs re-deriving"
            )
            assert "status" in status_header.lower(), (
                f"{config['name']} p{page_num}: expected 'Status' near column {config['col_status']}'s "
                f"header, got {status_header!r} -- table layout has changed, column mapping needs re-deriving"
            )
            usecase_columns = {}
            header_row0 = table[0]
            for col in range(config["usecase_start_col"], len(header_row0)):
                uc_id = joined_no_space(header_row0[col])
                assert USECASE_ID_RE.match(uc_id), (
                    f"{config['name']} p{page_num}: column {col} header {uc_id!r} doesn't look like a "
                    f"TMFSxxx use-case id -- table layout has changed"
                )
                usecase_columns[col] = uc_id

        current_functional_block = None
        for row in table[config["header_rows"] :]:
            fb = clean(row[config["col_functional_block"]]) if config["col_functional_block"] < len(row) else ""
            if fb:
                current_functional_block = fb
            comp_id = joined_no_space(row[config["col_component_id"]]) if config["col_component_id"] < len(row) else ""
            if not COMPONENT_ID_RE.match(comp_id):
                continue  # functional-block-only summary row, or a "new component to validate" placeholder ('-')
            comp_name = clean(row[config["col_component_name"]]) if config["col_component_name"] < len(row) else ""
            status = clean(row[config["col_status"]]) if config["col_status"] < len(row) else ""
            used_by = [usecase_columns[col] for col in usecase_columns if clean(row[col] if col < len(row) else "") == "Y"]
            rows_out.append(
                {
                    "component_id": comp_id,
                    "component_name": comp_name,
                    "functional_block": current_functional_block,
                    "status": status,
                    "used_by": used_by,
                }
            )

    return rows_out


def build_matrix(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_rows = []
        for config in PART_CONFIGS:
            part_rows = extract_part(pdf, config)
            print(f"{config['name']}: {len(part_rows)} component rows")
            all_rows.extend(part_rows)

    components = {}
    use_cases = {}
    for row in all_rows:
        comp_id = row["component_id"]
        # the same component can legitimately reappear across Parts (its row is
        # printed once per Part, with only that Part's use-case columns) --
        # merge used_by across occurrences rather than letting a later Part overwrite an earlier one
        if comp_id in components:
            components[comp_id]["used_by"] = sorted(set(components[comp_id]["used_by"]) | set(row["used_by"]))
        else:
            components[comp_id] = {
                "name": row["component_name"],
                "functional_block": row["functional_block"],
                "status": row["status"],
                "used_by": sorted(row["used_by"]),
            }
        for uc in row["used_by"]:
            use_cases.setdefault(uc, [])
            if comp_id not in use_cases[uc]:
                use_cases[uc].append(comp_id)

    for uc in use_cases:
        use_cases[uc].sort()

    return {
        "generated_from": "IG1228 v31.0.0, chapter 2 (\"Components identified per use-case\")",
        "source_pdf": os.path.relpath(pdf_path, os.path.join(os.path.dirname(__file__), "..")).replace("\\", "/"),
        "use_cases": dict(sorted(use_cases.items())),
        "components": dict(sorted(components.items())),
    }


def main():
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PDF
    matrix = build_matrix(pdf_path)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(matrix, f, indent=2)
    print(f"\n{len(matrix['use_cases'])} use cases, {len(matrix['components'])} components -> {OUT_PATH}")


if __name__ == "__main__":
    main()
