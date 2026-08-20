"""Reads: every artefact under knowledge/** (frontmatter and *.meta.json).
Writes: nothing -- exit code and stdout only.
Track: shared -- gating check run at the end of both refresh tracks (and
as the last step of build_index.py).

tools/validate_envelope.py -- check every artefact under knowledge/** carries the
five universal envelope fields (spec/spec.md 5.0: id, type, name, version, status),
regardless of artefact type. Run as the last step of every conversion/fetch script and
again in build_index.py (spec/tasks.md 0.7, 3.2), so a malformed envelope fails loudly
at creation time instead of silently breaking an index lookup later.

Reads frontmatter from *.md files and the envelope straight out of *.meta.json
sidecars -- same five keys, different container, per spec/spec.md 5.0.

A "TODO" stub (left by docx2md.py for fields that need the catalog page, spec/tasks.md
0.6) is reported but doesn't fail the run by default -- that's expected mid-Phase-1,
before tools/add_usecase_metadata.py has run. Pass --strict for the check
build_index.py should actually use, where a remaining TODO is a real failure: by
indexing time every artefact's metadata should be complete.

Usage:
    python validate_envelope.py [--strict] [knowledge_dir]
"""
import glob
import json
import os
import sys

import _yaml_lite as yaml_lite

REQUIRED = ("id", "type", "name", "version", "status")


def envelope_of(path):
    if path.endswith(".md"):
        with open(path, encoding="utf-8") as f:
            data, _ = yaml_lite.split(f.read())
        return data
    if path.endswith(".meta.json"):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return None


def check(path, data):
    problems = []
    for key in REQUIRED:
        if key not in data:
            problems.append(("MISSING", key))
        elif data[key] in (None, "", "TODO"):
            problems.append(("TODO" if data[key] == "TODO" else "EMPTY", key))
    return problems


def main():
    args = sys.argv[1:]
    strict = "--strict" in args
    args = [a for a in args if a != "--strict"]
    root = args[0] if args else "knowledge"

    # knowledge/index/ holds generated catalogs and static reference docs (id-registry.md) --
    # never artefact envelopes themselves (spec/spec.md 5.4: "generated, never hand-edited"),
    # so it's excluded regardless of what root is passed in.
    index_dir = os.path.normpath(os.path.join(root, "index"))
    # *.text-description.md (spec/spec.md 12, Phase 10) are sidecar image annotations under a
    # use case's own media/ folder, not standalone artefacts -- they describe one image, not a
    # thing with its own id/type/version/status. Excluded by suffix, not by directory, since
    # media/ is a normal subdirectory of a real artefact folder, not a category to blanket-skip.
    paths = [
        p
        for p in sorted(glob.glob(os.path.join(root, "**", "*.md"), recursive=True))
        + sorted(glob.glob(os.path.join(root, "**", "*.meta.json"), recursive=True))
        if not os.path.normpath(p).startswith(index_dir + os.sep) and not p.endswith(".text-description.md")
    ]

    hard_failures = 0
    todo_count = 0
    for path in paths:
        try:
            data = envelope_of(path)
        except ValueError as e:
            print(f"FAIL {path}: {e}")
            hard_failures += 1
            continue
        for kind, key in check(path, data):
            if kind == "TODO":
                todo_count += 1
                print(f"{'FAIL' if strict else 'todo'} {path}: {key} is still \"TODO\"")
                if strict:
                    hard_failures += 1
            else:
                print(f"FAIL {path}: {key} is {kind.lower()}")
                hard_failures += 1

    print(f"\n{len(paths)} artefact(s) checked, {hard_failures} failure(s), {todo_count} TODO stub(s)")
    sys.exit(1 if hard_failures else 0)


if __name__ == "__main__":
    main()
