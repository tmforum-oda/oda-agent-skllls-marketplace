# Using these skills in another repository

This repo's `skills/` are built to be used from *outside* this repo — in
any project where you want an agent to reason about TM Forum ODA use
cases, components, and Open APIs. This doc is for that consumer, not for
building or refreshing this repo itself (see [`spec/spec.md`](spec/spec.md)
and [`spec/tasks.md`](spec/tasks.md) for that).

There are two ways to get set up, with a real tradeoff between them —
pick based on which cost you'd rather pay:

| | Option A: sparse clone | Option B: Claude Code plugin |
|---|---|---|
| Works with | any agent that can read local files | Claude Code only |
| Footprint | one clone, ~108MB, wherever you put it | plugin cache, ~64MB per plugin, bundled again inside `dist/consumer/` and/or `dist/creator/` |
| Discovery | manual — skills only work from that clone's directory | automatic — works from any project, any cwd, once installed |
| Staying current | `git pull` | reinstall/update the plugin |

Both are real, both are verified working (see `spec/tasks.md` Phase 8)
— this isn't "one recommended, one theoretical."

## Option A: a sparse, partial clone

Every skill's instructions read `knowledge/` at paths relative to
wherever the agent's working directory is — that's how they work when
run directly from this repo (or a partial clone of it). It means:

- You need **both** `skills/` and `knowledge/`, not `skills/` alone, and
  they need to land as **siblings** — same parent directory.
- You do **not** need `references/` (raw DOCX/PDF — `knowledge/` is
  already generated from it), `tools/` (this repo's own refresh
  pipeline), or `spec/` (this repo's own design docs).

A full `git clone` also pulls `references/`'s raw files (spec.md §10:
"under 100MB" on its own) and the whole git history's blob objects for
them — none of which a consumer needs. A **sparse, partial clone**
fetches only `knowledge/` and `skills/`, and stays fully git-native:
versioned, pinnable, updatable with a plain `git pull`.

```bash
git clone --filter=blob:none --sparse \
  https://github.vodafone.com/Innovation-Network/tm-forum-sdlc.git \
  tm-forum-oda
cd tm-forum-oda
git sparse-checkout set knowledge skills
```

**Windows only** — a real gotcha found while testing this: some cached
API sample-payload filenames under `knowledge/apis/*/samples/` are long
enough to exceed Windows' default 260-character path limit, and
`sparse-checkout set` above will fail partway through with
`Filename too long` errors if so. Fix once, before running the commands
above (global, not per-repo — this is a Windows/git limitation, not
specific to this one repository):

```bash
git config --global core.longpaths true
```

Verified against the real repo: the resulting clone lands at ~108MB
total (~65MB `knowledge/` working tree, ~44MB `.git` objects, `skills/`
itself a few KB) — `references/`'s content is never fetched at all, not
even into `.git`.

**Pointing your agent at the skills**: where `skills/` needs to live
depends on your own agent harness's skill-discovery convention (e.g.
Claude Code looks for a configured skills directory such as
`.claude/skills/`) — that part is specific to whatever you're running.
Whatever you point it at, keep `knowledge/` as that directory's sibling.

**Staying up to date**: TM Forum republishes on a ~4–8 week cadence
(spec.md §6), and this repo's own refresh cycle tracks that.
Sparse-checkout patterns persist across `git pull`, so refreshing only
ever touches `knowledge/`/`skills/` — nothing else gets fetched. To pin
to a specific point in time instead of always tracking `main` (e.g. for
a reproducible build), clone as above, then `git checkout <commit-or-tag>`.

## Option B: install as a Claude Code plugin

There are two plugins, not one — a **consumer** plugin
([`dist/consumer/`](dist/consumer/)) with the skills for building a
product against ODA, and a **creator** plugin
([`dist/creator/`](dist/creator/)) with the skills for drafting and
extending ODA itself. Install whichever matches what you're doing, or
both. Each is a ready-to-install Claude Code plugin — its skill subset and
a full copy of `knowledge/`, bundled together, with every skill's
`knowledge/...` path reference rewritten to
`${CLAUDE_PLUGIN_ROOT}/knowledge/...` so it resolves correctly no matter
where Claude Code installs the plugin or what project you're working in
when you invoke it. That rewrite, and the reason it's necessary, is
explained in [`tools/build_plugin.py`](tools/build_plugin.py)'s docstring.

This deliberately breaks the usual norm that a plugin should be small —
each of `dist/consumer/knowledge/` and `dist/creator/knowledge/` is a full
copy of the corpus, on top of the one already at the repo's own top level
(and on top of each other, if you install both plugins), chosen so each
plugin has zero dependency on any project-specific clone or directory
layout.

```
claude plugin marketplace add https://github.vodafone.com/Innovation-Network/tm-forum-sdlc.git --sparse .claude-plugin dist
claude plugin install tm-forum-oda-consumer@tm-forum-oda-marketplace
claude plugin install tm-forum-oda-creator@tm-forum-oda-marketplace
```

(Install just one of the two `claude plugin install` lines if you only
need one audience's skills — the `marketplace add` step above covers both,
since both plugins live under the same `dist/` directory.)

(`/plugin marketplace add ...` and `/plugin install ...` slash commands
exist too, for inside an interactive session — the commands above are the
`claude plugin` CLI form, which is what was actually tested for this
`--sparse` flag; whether the slash-command form also accepts `--sparse`
wasn't checked, so use the CLI form above if you want the scoping
confirmed below.)

**The `--sparse .claude-plugin dist` matters — don't drop it.** Adding
the marketplace requires cloning the repository the marketplace lives in
(to read `.claude-plugin/marketplace.json` and resolve each plugin's
`source: ./dist/consumer` or `./dist/creator` path), and that clone is a
*separate* thing from the actual installed plugin(s). Without `--sparse`,
that clone pulls the **entire repo** — including `references/`, the raw
TM Forum member-gated DOCX/PDF this repo deliberately never redistributes
(spec.md §10), plus `tools/` and `spec/` — into
`~/.claude/plugins/marketplaces/...` on every consumer's machine, even
though only `dist/` ever actually gets used. `--sparse .claude-plugin dist`
limits that clone to just what the marketplace needs to read plus both
plugins' content (it covers `dist/` as a whole, so it works whether you
install one plugin or both).

Skills install namespaced per plugin: e.g.
`/tm-forum-oda-consumer:check-usecase-maturity` and
`/tm-forum-oda-creator:draft-new-usecase-from-scenario`.

**Verified for real** (not just from the docs): the single-plugin
predecessor of this setup was verified end-to-end — loaded via
`claude --plugin-dir` from a directory with no `knowledge/` anywhere
nearby and confirmed skills resolve `${CLAUDE_PLUGIN_ROOT}` correctly;
separately confirmed the unscoped `marketplace add` really does pull the
whole repo, and that `--sparse .claude-plugin dist` fixes it, through a
full `marketplace add` → `install` → invoke cycle (see `spec/tasks.md`
Phase 8.3/8.4). The two-plugin split changes `plugin.json`'s location and
each plugin's skill subset, not that resolution mechanism, but the split
itself — `dist/consumer/` and `dist/creator/` as two separate installable
plugins from one marketplace entry each — has not yet been re-verified
end-to-end; treat this section as accurate to the build script's output
until that's done.

**Staying up to date**: reinstall or update the plugin through whatever
mechanism your Claude Code version provides (`/plugin` commands) —
there's no `git pull` step here, since a plugin install isn't a clone you
own locally.

## Cross-agent reach (Copilot, etc.) — not built, a later follow-up

Neither option above works outside Claude Code — Option B's plugin
mechanism (`${CLAUDE_PLUGIN_ROOT}`, `.claude-plugin/`) is Claude
Code-specific, and Option A's skills format has no equivalent in other
agents' own instruction-loading conventions. `knowledge/`'s actual data
is plain Markdown/JSON and trivially agent-agnostic — the gap is only in
how instructions get loaded. The one mechanism adopted by multiple
vendors today, including Copilot's MCP client, is MCP: an MCP server
wrapping `knowledge/` (spec.md §7) would be callable from Claude Code
*and* Copilot from the same running server, at the cost of actually
hosting one. Not built yet — ask if you want to explore that direction.
