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
| `gaps-backlog.md` | capability gaps TM Forum's own authors already flagged in use cases' "Lessons learned" sections — proposed components/APIs that don't exist yet, consolidated across every use case that raises each one (spec.md §11.2, `skills/harvest-gaps-from-lessons-learned/`) |
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
skill-run time. Two audiences: **consumers** build a product using ODA;
**contributors** extend ODA itself.

**Consumers**

| Skill | Given | Produces |
|---|---|---|
| [`check-usecase-maturity`](skills/check-usecase-maturity/SKILL.md) | a `TMFSxxx` id | a plain-language "is this safe to build against" verdict from frontmatter alone |
| [`recommend-oda-components-for-requirement`](skills/recommend-oda-components-for-requirement/SKILL.md) | a plain-language requirement | the closest matching use case(s) and a starting component/API architecture |
| [`capture-requirements-from-usecase`](skills/capture-requirements-from-usecase/SKILL.md) | a `TMFSxxx` id | user stories and acceptance criteria, citing real component/API ids |
| [`generate-test-cases-from-usecase`](skills/generate-test-cases-from-usecase/SKILL.md) | a `TMFSxxx` id | BDD/Gherkin test scenarios grounded in the use case's real linked components/APIs and cached schemas |
| [`generate-api-mocks-from-usecase`](skills/generate-api-mocks-from-usecase/SKILL.md) | a `TMFSxxx` id | mock/fixture payloads for its linked APIs, from cached schemas and real sample payloads |
| [`draft-architecture-diagram-from-usecase`](skills/draft-architecture-diagram-from-usecase/SKILL.md) | a `TMFSxxx` id | a Mermaid diagram redrawn from the use case's own sequence diagrams |
| [`validate-design-against-oda`](skills/validate-design-against-oda/SKILL.md) | a proposed component/API design | a drift report checking its claimed dependencies against the real cached specs |
| [`assess-change-impact`](skills/assess-change-impact/SKILL.md) | a `TMFCxxx`/`TMFxxx` id + proposed change | every use case that depends on it (index reverse links) and a maturity-weighted migration risk report |
| [`audit-implementation-against-usecase`](skills/audit-implementation-against-usecase/SKILL.md) | a `TMFSxxx` id + an existing implementation | a drift report against what the use case actually specifies |

**Contributors**

| Skill | Given | Produces |
|---|---|---|
| [`harvest-gaps-from-lessons-learned`](skills/harvest-gaps-from-lessons-learned/SKILL.md) | the whole corpus | capability gaps TM Forum's own authors already flagged, consolidated in [`knowledge/index/gaps-backlog.md`](knowledge/index/gaps-backlog.md) |
| [`propose-matrix-correction`](skills/propose-matrix-correction/SKILL.md) | a `matrix-discrepancies.md` entry | a specific, submittable correction for the next IG1228 revision |
| [`draft-new-usecase-from-scenario`](skills/draft-new-usecase-from-scenario/SKILL.md) | a business scenario | a new use-case document in this corpus's own structure |
| [`propose-component-or-api-extension`](skills/propose-component-or-api-extension/SKILL.md) | a capability gap | a draft component skeleton (real IG1242 shape) or API schema extension |
| [`lint-usecase-draft`](skills/lint-usecase-draft/SKILL.md) | a draft use-case document | a pre-submission check against known conversion-breaking document shapes |

Using these skills from another repository? See [`CONSUMING.md`](CONSUMING.md) —
covers both a sparse clone (lighter, git-native) and installing
[`dist/`](dist/) as a Claude Code plugin (heavier — bundles `knowledge/`
inside the plugin — but zero manual clone/update management).

## Tools

Every script in `tools/` opens with a `Reads:`/`Writes:`/`Track:` header
stating what it touches and whether it belongs to the assisted or
automated refresh track (or is a shared helper/gating check used by both)
— check there before reading further into any one script's docstring for
the *why*.
