# ODA Knowledge Base

A machine-readable, provenance-tracked knowledge base built from TM Forum's
Open Digital Architecture (ODA) — use cases (`TMFSxxx`), ODA Components
(`TMFCxxx`), and Open APIs (`TMFxxx`) — organized so that Agent
Skills can query it directly, without re-parsing DOCX/PDF or guessing
whether a document is safe to build against.

The full design rationale lives in [`spec/spec.md`](spec/spec.md); build
history and the reasoning behind every real bug/decision found along the
way is in [`spec/tasks.md`](spec/tasks.md). This file is the map, not the
explanation — read those two for *why* the repo looks like this.

## Layout

```
references/   raw downloaded input -- DOCX/PDF, unmodified, for provenance and re-conversion
knowledge/    generated, agent-facing corpus -- what skills actually read
skills/       Agent Skills built against knowledge/
tools/        the conversion/fetch/index pipeline that produces knowledge/ from references/
spec/         spec.md (design), tasks.md (build log), refresh-runbook.md (assisted-track checklist)
```

**`references/` vs `knowledge/`** is the one split everything else follows
(spec.md principle 3). `references/` is committed too, not gitignored —
it holds TM Forum member-gated content (IG1228, the `TMFSxxx` use-case
DOCX files) that a fresh clone has no other way to reproduce without a
TM Forum login; see spec.md §10 for the full reasoning. `knowledge/` is
regeneratable from `references/` plus the public GitHub/S3 sources —
skills should never need to touch `references/` directly.

Within `knowledge/`:

```
knowledge/use-cases/{TMFSxxx}/{TMFSxxx}.md   one Markdown file per use case, YAML frontmatter + body
knowledge/components/{TMFCxxx}/               component.yaml + component.meta.json
knowledge/apis/{TMFxxx}/                      {TMFxxx}_v{version}.json + .meta.json (multiple versions coexist)
knowledge/index/                              the ID registry -- see below
```

Every artefact carries the same five-field envelope (`id`, `type`, `name`,
`version`, `status`) plus provenance (`source.origin`/`retrieved`/`sha256`)
and, for use cases, maturity/approval fields — spec.md §5.0/§5.4 explains
why, and it's what makes `check-usecase-maturity` (below) possible without
a network call.

## The ID registry — `knowledge/index/`

Every "what exists, and what links to what" question should be answerable
by reading one of these files, not by scanning the corpus:

| File | What it answers |
|---|---|
| `use-cases.json` / `components.json` / `apis.json` | the full corpus, one row per artefact, with forward and reverse links |
| `usecase-list.json` | every `TMFSxxx` id IG1228 knows about, including `planned`/`not available` ones with nothing converted yet |
| `usecase-component-matrix.json` | IG1228's own corpus-level "which use case touches which component" table |
| `matrix-discrepancies.md` | where a use case's own document disagrees with that matrix, logged rather than silently resolved one way (spec.md §5.4) — read **both** sources for a complete answer; neither alone is |
| `component-folder-map.json` / `api-samples-folder-map.json` | id → upstream GitHub folder lookups, internal to `tools/fetch_*.py` |

Regenerate all three main index files with `python tools/build_index.py`
(idempotent — safe to re-run any time, byte-identical output on unchanged
input).

## Running a refresh

TM Forum republishes on a rolling ~4–8 week cadence. There are two
independent tracks — see [`spec/refresh-runbook.md`](spec/refresh-runbook.md)
for the full step-by-step, and `spec/spec.md` §6 for why they're split:

- **Assisted** (`spec/refresh-runbook.md`) — IG1228 and `TMFSxxx` use cases.
  Requires a logged-in TM Forum member session and a human to click
  through the download; cannot be scheduled.
- **Automated** (`python tools/fetch_component.py --all-referenced && python tools/fetch_api.py`) —
  ODA Component specs and Open API schemas. Fully public, unauthenticated,
  safe to run on a schedule; only rewrites files whose content actually
  changed.

Either way, finish with `python tools/build_index.py` then
`python tools/refresh_report.py` to regenerate the index and append a
dated entry to `CHANGELOG.md` describing what changed — maturity/status
transitions (`Beta → GA`) called out explicitly, per spec.md §6.3's
finding that a newly-changed use case is very likely pre-GA.

## Skills

Built against `knowledge/`, read-only, no network calls needed at
skill-run time (spec.md §8):

- [`skills/check-usecase-maturity/`](skills/check-usecase-maturity/SKILL.md) — given a `TMFSxxx` id, a plain-language "is this safe to build against" verdict from frontmatter alone.
- [`skills/generate-test-cases-from-usecase/`](skills/generate-test-cases-from-usecase/SKILL.md) — given a `TMFSxxx` id, drafts BDD/Gherkin test scenarios grounded in the use case's real linked components/APIs and their cached schemas, citing every id back to its exact source.

Using these skills from another repository? See [`CONSUMING.md`](CONSUMING.md) —
`skills/` needs `knowledge/` alongside it as a sibling, and a sparse
partial clone gets you both without `references/`'s DOCX/PDF weight.

## Tools

Every script in `tools/` opens with a `Reads:`/`Writes:`/`Track:` header
stating what it touches and whether it belongs to the assisted or
automated refresh track (or is a shared helper/gating check used by both)
— check there before reading further into any one script's docstring for
the *why*.
