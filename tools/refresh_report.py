"""Reads: knowledge/index/*.json (current, on disk) and
git HEAD:knowledge/index/*.json (previous committed version).
Writes: CHANGELOG.md (appends an entry; creates the file on first use).
Track: shared -- run after either refresh track, or both, at the very end
of a refresh cycle (spec.md 6.1 step 6).

tools/refresh_report.py -- diff the just-regenerated knowledge/index/*.json
against the last git-committed version and append a human-readable entry to
CHANGELOG.md (spec/spec.md 6.1 step 6, tasks.md 5.2).

Run this AFTER build_index.py (and, on the assisted track, after
docx2md.py/add_usecase_metadata.py) -- it reads whatever is currently on disk
against `git show HEAD:<path>`, so uncommitted changes are exactly what gets
reported. If a given index file doesn't exist yet at HEAD (first run ever),
its "old" side is treated as empty -- everything currently on disk reports as
new, which is the correct answer for a from-scratch run.

Three index files, three key strategies, because the three artefact types
don't identify a "version" the same way:
  - use-cases.json: keyed by id. docx2md.py overwrites TMFSxxx.md in place on
    a version bump, so a new version of an already-known use case is a
    CHANGE to its existing row, not a new row.
  - components.json: keyed by id, same reasoning (component.yaml is
    overwritten in place; not_yet_specified -> specified is a status change
    on the same row, not a new one).
  - apis.json: keyed by meta_path, NOT id. Multiple API versions genuinely
    coexist side by side (fetch_api.py's own docstring) -- TMF632_v4.0.0 and
    TMF632_v5.0.0 are two distinct cached files under one id. Keying by id
    here would make a new version look like a "changed" row and silently
    hide that the old version is still there too.

spec.md 6.3's single most important refresh-process finding -- a newly
changed use case is very likely pre-GA, and the report must surface that,
not bury it -- is why maturity/approval_status/release_status are watched
fields for use-cases specifically, not just version/status.

Usage:
    python refresh_report.py
"""
import datetime as _dt
import json
import os
import subprocess
import sys

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")
INDEX_DIR = os.path.join(REPO_ROOT, "knowledge", "index")
CHANGELOG_PATH = os.path.join(REPO_ROOT, "CHANGELOG.md")

USE_CASE_FIELDS = ["version", "status", "maturity", "approval_status", "release_status"]
ARTEFACT_FIELDS = ["version", "status"]


def load_git_json(rel_path):
    result = subprocess.run(
        ["git", "show", f"HEAD:{rel_path}"], cwd=REPO_ROOT, capture_output=True, text=True
    )
    if result.returncode != 0:
        return []  # not committed yet -- everything on disk is new
    return json.loads(result.stdout)


def load_disk_json(rel_path):
    path = os.path.join(REPO_ROOT, rel_path)
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def diff_rows(old_rows, new_rows, key_fn, watch_fields):
    """Returns (added, removed, changed). changed is a list of
    (key, field, old_value, new_value) tuples, one per changed field --
    a row with three changed fields produces three entries, so the report
    can list "TMFS020: maturity Beta -> GA" and "TMFS020: approval_status
    ... -> ..." as separate, individually readable lines."""
    old_by_key = {key_fn(r): r for r in old_rows}
    new_by_key = {key_fn(r): r for r in new_rows}

    added = sorted(new_by_key.keys() - old_by_key.keys())
    removed = sorted(old_by_key.keys() - new_by_key.keys())

    changed = []
    for key in sorted(new_by_key.keys() & old_by_key.keys()):
        old_row, new_row = old_by_key[key], new_by_key[key]
        for field in watch_fields:
            old_val, new_val = old_row.get(field), new_row.get(field)
            if old_val != new_val:
                changed.append((key, field, old_val, new_val))

    return added, removed, changed


def format_section(title, count_label, rows_by_key, added, removed, changed, added_label_fn):
    lines = [f"**{title}:** {len(rows_by_key)} total, {len(added)} new, {len(removed)} removed, {len(changed)} field change(s)"]
    if not (added or removed or changed):
        return None
    for key in added:
        lines.append(f"- {added_label_fn(key)}")
    for key in removed:
        lines.append(f"- {key}: no longer cached (file removed)")
    for key, field, old_val, new_val in changed:
        lines.append(f"- {key}: {field} {old_val!r} -> {new_val!r}")
    return "\n".join(lines)


def main():
    old_uc = load_git_json("knowledge/index/use-cases.json")
    new_uc = load_disk_json("knowledge/index/use-cases.json")
    old_comp = load_git_json("knowledge/index/components.json")
    new_comp = load_disk_json("knowledge/index/components.json")
    old_api = load_git_json("knowledge/index/apis.json")
    new_api = load_disk_json("knowledge/index/apis.json")

    uc_added, uc_removed, uc_changed = diff_rows(old_uc, new_uc, lambda r: r["id"], USE_CASE_FIELDS)
    comp_added, comp_removed, comp_changed = diff_rows(old_comp, new_comp, lambda r: r["id"], ARTEFACT_FIELDS)
    api_added, api_removed, api_changed = diff_rows(old_api, new_api, lambda r: r["meta_path"], ARTEFACT_FIELDS)

    new_uc_by_id = {r["id"]: r for r in new_uc}
    new_comp_by_id = {r["id"]: r for r in new_comp}
    new_api_by_path = {r["meta_path"]: r for r in new_api}

    sections = [
        format_section(
            "Use cases", "use case", new_uc_by_id, uc_added, uc_removed, uc_changed,
            lambda k: f"{k}: newly converted (\"{new_uc_by_id[k]['name']}\", {new_uc_by_id[k]['maturity']}/{new_uc_by_id[k]['approval_status']})",
        ),
        format_section(
            "Components", "component", new_comp_by_id, comp_added, comp_removed, comp_changed,
            lambda k: f"{k}: newly cached (\"{new_comp_by_id[k]['name']}\", {new_comp_by_id[k]['status']})",
        ),
        format_section(
            "API versions", "API version", new_api_by_path, api_added, api_removed, api_changed,
            lambda k: f"{new_api_by_path[k]['id']} {new_api_by_path[k]['version']}: newly cached",
        ),
    ]
    reportable = [s for s in sections if s is not None]

    if not reportable:
        print("No changes detected against the last commit -- nothing appended to CHANGELOG.md.")
        return

    date = _dt.date.today().isoformat()
    entry = f"## {date}\n\n" + "\n\n".join(reportable) + "\n"

    if not os.path.exists(CHANGELOG_PATH):
        with open(CHANGELOG_PATH, "w", encoding="utf-8") as f:
            f.write("# Changelog\n\nRefresh-cycle history, generated by `tools/refresh_report.py` (spec.md 6.1/6.3).\nNewest entry at the bottom -- append-only, matching tasks.md 5.2's design.\n\n")

    with open(CHANGELOG_PATH, "a", encoding="utf-8") as f:
        f.write("\n" + entry)

    print(entry)
    print(f"Appended to {CHANGELOG_PATH}")


if __name__ == "__main__":
    main()
