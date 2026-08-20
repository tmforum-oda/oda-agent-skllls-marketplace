"""Reads: skills/**, knowledge/**.
Writes: dist/skills/** (SKILL.md files with knowledge/ path references
rewritten to ${CLAUDE_PLUGIN_ROOT}/knowledge/...), dist/knowledge/**
(verbatim copy), dist/.claude-plugin/plugin.json.
Track: n/a -- packaging step, not part of either refresh track. Run after
any change to skills/ or knowledge/ to regenerate the distributable
plugin bundle in dist/.

tools/build_plugin.py -- package skills/ + knowledge/ as a Claude Code
plugin in dist/, installable via .claude-plugin/marketplace.json at the
repo root. CONSUMING.md's sparse clone is the lighter-weight alternative
for a consumer who'd rather not accept a full plugin install; this is the
other end of that tradeoff, deliberately -- the user explicitly chose to
bundle knowledge/ inside the plugin, accepting that it breaks the norm
that plugins should be small/fast.

dist/ is committed to git, not gitignored, for the same reason knowledge/
itself is (spec.md principle 3/§10): a plugin is installed by Claude Code
fetching directory contents directly from this repo's git history --
consumers don't run this script themselves, so the artefact it produces
has to already be there when they install.

The one non-mechanical step this script exists to do: skills/*/SKILL.md
are authored with plain relative paths (knowledge/use-cases/...) so they
work unmodified for a direct clone or CONSUMING.md's sparse clone, where
the agent's cwd contains knowledge/ as a sibling. A plugin installs to
~/.claude/plugins/cache/... instead -- NOT the user's project cwd -- so a
bare relative path would silently resolve against the wrong directory
there. Claude Code substitutes ${CLAUDE_PLUGIN_ROOT} to the plugin's real
install directory, but ONLY inside plugin skills, so baking that syntax
into the canonical skills/*/SKILL.md would make it inert (literal,
unsubstituted text) for the direct-clone/sparse-clone case. Resolved by
keeping one canonical source (plain paths) and mechanically rewriting
`knowledge/` -> `${CLAUDE_PLUGIN_ROOT}/knowledge/` only in the copies
under dist/ -- the same "generate the packaged form, never hand-maintain
two versions" pattern this repo already uses for knowledge/ itself
(generated from references/).

Must be idempotent (spec.md principle 7): dist/ is deleted and rebuilt
from scratch every run, so two consecutive runs with no source changes
produce an identical file set and identical file content.

Usage:
    python build_plugin.py
"""
import json
import os
import shutil

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")
SKILLS_SRC = os.path.join(REPO_ROOT, "skills")
KNOWLEDGE_SRC = os.path.join(REPO_ROOT, "knowledge")
DIST_DIR = os.path.join(REPO_ROOT, "dist")

# Repo-maintenance skills that write to knowledge/ (spec.md 12) -- a different
# category from every other skill here, which only ever reads knowledge/. Not for
# external distribution: a consumer installing the plugin to build against this
# corpus has no use for a skill that edits it, and shipping one invites someone
# running it against a knowledge/ they don't actually maintain (e.g. a sparse
# clone with no way to push changes back). Stays in skills/ -- and in this repo's
# own git history -- just never copied into dist/.
INTERNAL_ONLY_SKILLS = {"process-usecase-media"}

PLUGIN_MANIFEST = {
    "name": "tm-forum-oda",
    "version": "1.0.0",
    "description": "TM Forum ODA use cases, components, and Open APIs as a provenance-tracked knowledge base, queryable via Agent Skills.",
    "author": {"name": "Lester Thomas"},
}


def rewrite_knowledge_paths(text):
    return text.replace("knowledge/", "${CLAUDE_PLUGIN_ROOT}/knowledge/")


def copy_skills():
    dst = os.path.join(DIST_DIR, "skills")
    shutil.copytree(SKILLS_SRC, dst, ignore=lambda _dir, names: INTERNAL_ONLY_SKILLS & set(names))
    rewritten = 0
    for root, _, files in os.walk(dst):
        for name in files:
            if name != "SKILL.md":
                continue
            path = os.path.join(root, name)
            with open(path, encoding="utf-8") as f:
                text = f.read()
            new_text = rewrite_knowledge_paths(text)
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_text)
            rewritten += new_text.count("${CLAUDE_PLUGIN_ROOT}/knowledge/")
    return rewritten


def copy_knowledge():
    shutil.copytree(KNOWLEDGE_SRC, os.path.join(DIST_DIR, "knowledge"))


def write_manifest():
    manifest_dir = os.path.join(DIST_DIR, ".claude-plugin")
    os.makedirs(manifest_dir, exist_ok=True)
    with open(os.path.join(manifest_dir, "plugin.json"), "w", encoding="utf-8") as f:
        json.dump(PLUGIN_MANIFEST, f, indent=2)
        f.write("\n")


def main():
    if os.path.exists(DIST_DIR):
        shutil.rmtree(DIST_DIR)
    os.makedirs(DIST_DIR)

    rewritten = copy_skills()
    copy_knowledge()
    write_manifest()

    skill_count = sum(1 for _, _, fs in os.walk(os.path.join(DIST_DIR, "skills")) for f in fs if f == "SKILL.md")
    print(f"dist/skills/: {skill_count} skill(s), {rewritten} knowledge/ path reference(s) rewritten to ${{CLAUDE_PLUGIN_ROOT}}")
    print(f"dist/knowledge/: copied from {KNOWLEDGE_SRC}")
    print("dist/.claude-plugin/plugin.json: written")


if __name__ == "__main__":
    main()
