# Using these skills in another repository

This repo's `skills/` are built to be used from *outside* this repo — in
any project where you want an agent to reason about TM Forum ODA use
cases, components, and Open APIs. This doc is for that consumer, not for
building or refreshing this repo itself (see [`spec/spec.md`](spec/spec.md)
and [`spec/tasks.md`](spec/tasks.md) for that).

## What you need locally: `skills/` + `knowledge/`, kept as siblings

Every skill's instructions read `knowledge/` at paths relative to wherever
it's run from (e.g. `knowledge/use-cases/{ID}/{ID}.md`) — not relative to
the skill's own folder. That's deliberate: both skills already share one
`knowledge/` today rather than each carrying a private copy (see the design
note in [`README.md`](README.md)). It means:

- You need **both** `skills/` and `knowledge/`, not `skills/` alone.
- They need to land as **siblings** — same parent directory — for the
  skills' relative paths to resolve.
- You do **not** need `references/` (the raw DOCX/PDF — `knowledge/` is
  already generated from it) or `tools/` (this repo's own refresh
  pipeline, irrelevant to a consumer) or `spec/` (this repo's own design
  docs).

## Recommended: a sparse, partial clone

A full `git clone` of this repo also pulls `references/`'s raw DOCX/PDF
files (spec.md §10: "under 100MB" on its own) and the whole git history's
blob objects for them — none of which a consumer needs. A **sparse,
partial clone** fetches only `knowledge/` and `skills/` (plus the small
root-level files like this one), which is meaningfully lighter and still
fully git-native: versioned, pinnable, updatable with a plain `git pull`.

```bash
git clone --filter=blob:none --sparse \
  https://github.vodafone.com/Innovation-Network/tm-forum-sdlc.git \
  tm-forum-oda
cd tm-forum-oda
git sparse-checkout set knowledge skills
```

**Windows only** — a real gotcha found while testing this: some of the
cached API sample-payload filenames under `knowledge/apis/*/samples/` are
long enough to exceed Windows' default 260-character path limit, and the
`sparse-checkout set` step above will fail partway through with
`Filename too long` errors if so. Fix once, before running the commands
above:

```bash
git config --global core.longpaths true
```

(Global, not per-repo, since this is a Windows/git limitation that isn't
specific to this one repository.)

Verified against the real repo while writing this: the resulting clone
lands at ~108MB total (~65MB `knowledge/` working tree, ~44MB `.git`
objects, `skills/` itself is a few KB) — `references/`'s content is never
fetched at all, not even into `.git`, because it's outside the sparse
patterns and the `--filter=blob:none` partial clone only pulls blobs for
paths actually checked out.

## Pointing your agent at the skills

Where `skills/` needs to live depends on your own agent harness's
skill-discovery convention (e.g. Claude Code looks for a configured skills
directory such as `.claude/skills/`) — that part is specific to whatever
you're running, not something this repo can dictate. Whatever you point
it at, keep `knowledge/` as that directory's sibling, per above.

## Staying up to date

TM Forum republishes on a ~4–8 week cadence (spec.md §6), and this repo's
own refresh cycle tracks that. To pick up a refresh:

```bash
cd tm-forum-oda
git pull
```

Sparse-checkout patterns persist across `pull`, so this only ever touches
`knowledge/`/`skills/` — nothing else gets fetched.

To pin to a specific point in time instead of always tracking `main`
(e.g. for a reproducible build), clone as above, then:

```bash
git checkout <commit-or-tag>
```

## An alternative worth knowing about, not built yet

If you'd rather not maintain even a sparse local clone — e.g. you want
skills that always read the current `knowledge/` with zero local
footprint and no update step — that needs a different mechanism (a
remote-fetch-capable skill, or an MCP server wrapping `knowledge/`, per
spec.md §7). Both trade away this repo's "no network call needed at
skill-run time" design principle in exchange for zero staleness; the
sparse clone above keeps that principle and is what's actually built and
verified today. Ask if you want to explore that direction instead.
