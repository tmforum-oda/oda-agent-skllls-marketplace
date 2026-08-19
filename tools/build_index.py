"""Reads: every knowledge/use-cases/**/*.md frontmatter block; every
knowledge/{components,apis}/**/*.meta.json.
Writes: knowledge/index/{use-cases,components,apis}.json.
Track: shared -- run at the end of either refresh track (or both) to
regenerate the corpus-wide index; gates on validate_envelope.py.

tools/build_index.py -- regenerate knowledge/index/{use-cases,components,apis}.json
from every artefact's envelope (spec/spec.md 5.4).

Walks the envelope the same way regardless of artefact type -- frontmatter for
knowledge/use-cases/**/*.md, *.meta.json for knowledge/components/** and
knowledge/apis/** -- per the "one envelope, shared by every artefact type"
principle (spec.md 5.0/§3 principle 9). No type-specific parsing needed here
beyond which reader function opens the file.

Reverse links (links.use_cases on a component/API's index row) are computed
ONLY from each use case's own forward links.components/links.apis -- never
merged with usecase-component-matrix.json's independently-sourced data, which
stays a separate file precisely because the two sources don't always agree
(knowledge/index/matrix-discrepancies.md, task 3.3). Blending them here would
quietly erase that signal.

Must be idempotent (spec.md principle 7, success criterion in §9): run twice
with no input changes, byte-identical output. That's why every dict below is
built with explicit, sorted key order rather than relying on iteration order
of a directory listing or a set.

Runs tools/validate_envelope.py --strict as its last step -- an index built
from a corpus with an incomplete envelope is worse than no index (a lookup
would silently return partial data), so that check gates a successful run.

Usage:
    python build_index.py
"""
import glob
import json
import os
import subprocess
import sys

import _yaml_lite

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")
KNOWLEDGE_DIR = os.path.join(REPO_ROOT, "knowledge")
INDEX_DIR = os.path.join(KNOWLEDGE_DIR, "index")


def rel(path):
    return os.path.relpath(path, REPO_ROOT).replace("\\", "/")


def load_use_cases():
    rows = []
    for path in sorted(glob.glob(os.path.join(KNOWLEDGE_DIR, "use-cases", "*", "*.md"))):
        with open(path, encoding="utf-8") as f:
            data, _ = _yaml_lite.split(f.read())
        rows.append(
            {
                "id": data["id"],
                "type": data["type"],
                "name": data["name"],
                "version": data["version"],
                "status": data["status"],
                "maturity": data.get("maturity"),
                "approval_status": data.get("approval_status"),
                "release_status": data.get("release_status"),
                "components": sorted(c["id"] for c in data.get("links", {}).get("components", [])),
                "apis": sorted(a["id"] for a in data.get("links", {}).get("apis", [])),
                "path": rel(path),
            }
        )
    return sorted(rows, key=lambda r: r["id"])


def load_meta_rows(subdir):
    rows = []
    for path in sorted(glob.glob(os.path.join(KNOWLEDGE_DIR, subdir, "*", "*.meta.json"))):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        content_path = path[: -len(".meta.json")] + (".yaml" if subdir == "components" else ".json")
        rows.append(
            {
                "id": data["id"],
                "type": data["type"],
                "name": data["name"],
                "version": data["version"],
                "status": data["status"],
                "source_origin": data.get("source", {}).get("origin"),
                "path": rel(content_path) if os.path.exists(content_path) else None,
                "meta_path": rel(path),
            }
        )
    return rows


def add_reverse_links(rows, use_cases, link_key):
    """rows: components.json or apis.json rows, keyed by id. link_key: 'components' or 'apis'."""
    used_by = {}
    for uc in use_cases:
        for ref_id in uc[link_key]:
            used_by.setdefault(ref_id, set()).add(uc["id"])
    for row in rows:
        row["used_by"] = sorted(used_by.get(row["id"], []))
    return rows


def main():
    use_cases = load_use_cases()
    components = add_reverse_links(load_meta_rows("components"), use_cases, "components")
    apis = add_reverse_links(load_meta_rows("apis"), use_cases, "apis")

    os.makedirs(INDEX_DIR, exist_ok=True)
    outputs = {
        "use-cases.json": sorted(use_cases, key=lambda r: r["id"]),
        "components.json": sorted(components, key=lambda r: r["id"]),
        "apis.json": sorted(apis, key=lambda r: r["id"]),
    }
    for filename, data in outputs.items():
        with open(os.path.join(INDEX_DIR, filename), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, sort_keys=False)
            f.write("\n")

    print(f"use-cases.json: {len(use_cases)} rows")
    print(f"components.json: {len(components)} rows")
    print(f"apis.json: {len(apis)} rows")

    print("\nRunning validate_envelope.py --strict as the gating check...")
    result = subprocess.run(
        [sys.executable, os.path.join(os.path.dirname(__file__), "validate_envelope.py"), "--strict", KNOWLEDGE_DIR]
    )
    if result.returncode != 0:
        sys.exit("build_index.py: validate_envelope.py --strict failed -- index was written but is built on an incomplete corpus, fix the envelope gaps above and re-run")


if __name__ == "__main__":
    main()
