# ODA Agent Skills Marketplace

A set of Agent skills for **Consumers** and **Creators** of the TM Forum Open Digital Architecture, backed by an agent-friendly **knowledge** base.

The skills are packaged into two plugins `tm-forum-oda-consumer` and `tm-forum-oda-creator` and made available in a Marketplace. You can view the skills in:

[dist/consumer/skills](dist/consumer/skills)

[dist/creator/skills](dist/creator/skills)

The [knowledge](knowledge) is a machine-readable knowledge base built from TM Forum's
Open Digital Architecture (ODA) — use cases (`TMFSxxx`), ODA Components
(`TMFCxxx`), and Open APIs (`TMFxxx`) — organized so that Agent
Skills can query it directly, without re-parsing DOCX/PDF.

The full design rationale lives in [`spec/spec.md`](spec/spec.md); build
history and the reasoning behind every real bug/decision found along the
way is in [`spec/tasks.md`](spec/tasks.md). The human-readable Component
Specification PDF narrative alongside each `component.yaml` (see below)
has its own companion pair, [`spec/spec-components.md`](spec/spec-components.md)
and [`spec/tasks-components.md`](spec/tasks-components.md). 

## Layout

```
references/   raw downloaded input -- DOCX/PDF, unmodified, for provenance and re-conversion
knowledge/    generated, agent-facing corpus -- what skills actually read
skills/       Agent Skills built against knowledge/
tools/        the conversion/fetch/index pipeline that produces knowledge/ from references/
spec/         spec.md (design), tasks.md (build log), refresh-runbook.md (assisted-track checklist)
```

**`references/` contains the source artefacts and  `knowledge/`** contains the agent-friendly view
(spec.md principle 3). `references/` holds TM Forum member-gated content (IG1228, the `TMFSxxx` use-case
DOCX files) that a fresh clone has no other way to reproduce without a
TM Forum login; see spec.md §10 for the full reasoning. `knowledge/` is
regeneratable from `references/` plus the public GitHub/S3 sources —
skills should never need to touch `references/` directly.

Within `knowledge/`:

```
knowledge/use-cases/{TMFSxxx}/{TMFSxxx}.md   one Markdown file per use case, YAML frontmatter + body
knowledge/components/{TMFCxxx}/               component.yaml + component.meta.json + {TMFCxxx}.md (narrative, from the PDF spec -- 25 of 31 components have one, spec-components.md §3.1/§6)
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
by reading one of these files:

| File | What it answers |
|---|---|
| `use-cases.json` / `components.json` / `apis.json` | the full corpus, one row per artefact, with forward and reverse links |
| `usecase-list.json` | every `TMFSxxx` id IG1228 knows about, including `planned`/`not available` ones with nothing converted yet |
| `usecase-component-matrix.json` | IG1228's own corpus-level "which use case touches which component" table |
| `matrix-discrepancies.md` | where a use case's own document disagrees with that matrix, logged to feedback to the use-case team (spec.md §5.4) — read **both** sources for a complete answer; |
| `gaps-backlog.md` | capability gaps TM Forum's own authors already flagged in use cases' "Lessons learned" sections — proposed components/APIs that don't exist yet, consolidated across every use case that raises each one (spec.md §11.2, `skills/harvest-gaps-from-lessons-learned/`) |
| `component-folder-map.json` / `api-samples-folder-map.json` | id → upstream GitHub folder lookups, internal to `tools/fetch_*.py` |

Regenerate all three main index files with `python tools/build_index.py`
(idempotent — safe to re-run any time, byte-identical output on unchanged
input).

## Running a refresh

TM Forum republishes on a rolling 8 week cadence. There are two
independent tracks — see [`spec/refresh-runbook.md`](spec/refresh-runbook.md)
for the full step-by-step, and `spec/spec.md` §6 for why they're split:

- **Assisted** (`spec/refresh-runbook.md`) — IG1228 and `TMFSxxx` use cases.
  Requires a logged-in TM Forum member session and a human to click
  through the download; cannot be scheduled.
- **Automated** (`python tools/fetch_component.py --all-referenced && python tools/fetch_api.py`) —
  ODA Component specs and Open API schemas. Fully public, unauthenticated,
  safe to run on a schedule; only rewrites files whose content actually
  changed. The human-readable Component Specification PDFs (`{TMFCxxx}.md`,
  `tools/pdf2md_component.py`) belong to this same track — no login gate
  either — but are heavier: each component's PDF link has to be resolved
  from a real directory-page load first (spec-components.md §3), not a
  tag-listing lookup, and that discovery+download half isn't yet its own
  checked-in script (done per-component via a driven browser so far,
  spec-components.md §7, spec/tasks-components.md Phase 8.4).

Either way, finish with `python tools/build_index.py` then
`python tools/refresh_report.py` to regenerate the index and append a
dated entry to `CHANGELOG.md` describing what changed — maturity/status
transitions (`Beta → GA`) called out explicitly, per spec.md §6.3's
finding that a newly-changed use case is very likely pre-GA.

## Skills

Built against `knowledge/`, read-only, no network calls needed at
skill-run time. Two audiences, packaged as two separate plugins
(`tm-forum-oda-consumer` / `tm-forum-oda-creator`, see
[`tools/build_plugin.py`](tools/build_plugin.py)) so each install's skill
list stays focused on what that audience actually invokes: **consumers**
build a product using ODA; **creators** extend ODA itself.

**Consumers** (`tm-forum-oda-consumer`)

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

**Creators** (`tm-forum-oda-creator`)

| Skill | Given | Produces |
|---|---|---|
| [`harvest-gaps-from-lessons-learned`](skills/harvest-gaps-from-lessons-learned/SKILL.md) | the whole corpus | capability gaps TM Forum's own authors already flagged, consolidated in [`knowledge/index/gaps-backlog.md`](knowledge/index/gaps-backlog.md) |
| [`propose-matrix-correction`](skills/propose-matrix-correction/SKILL.md) | a `matrix-discrepancies.md` entry | a specific, submittable correction for the next IG1228 revision |
| [`draft-new-usecase-from-scenario`](skills/draft-new-usecase-from-scenario/SKILL.md) | a business scenario | a new use-case document in this corpus's own structure |
| [`propose-component-or-api-extension`](skills/propose-component-or-api-extension/SKILL.md) | a capability gap | a draft component skeleton (real IG1242 shape) or API schema extension |
| [`lint-usecase-draft`](skills/lint-usecase-draft/SKILL.md) | a draft use-case document | a pre-submission check against known conversion-breaking document shapes |

Using these skills from another repository? See [`CONSUMING.md`](CONSUMING.md) —
covers both a sparse clone (lighter, git-native) and installing
[`dist/consumer/`](dist/consumer/) or [`dist/creator/`](dist/creator/) as a
Claude Code plugin (heavier — bundles `knowledge/` inside the plugin — but
zero manual clone/update management).

**Repo maintenance**

Two skills write to `knowledge/` instead of just reading it, and are
deliberately excluded from both `dist/consumer/` and `dist/creator/` — a
consumer or creator building against this corpus has no use for a skill
that edits it:

| Skill | Given | Produces |
|---|---|---|
| [`process-usecase-media`](skills/process-usecase-media/SKILL.md) | a `TMFSxxx` id | renames each of its raw extracted images descriptively, reverse-engineers UML sequence diagrams into PlantUML, and writes a text description for everything else — see spec.md §12 |
| [`process-component-media`](skills/process-component-media/SKILL.md) | a `TMFCxxx` id | renames each of its raw extracted images descriptively, reverse-engineers the component architecture/eTOM-SID-link/API-structure diagrams into PlantUML, and writes a text description for everything else — see spec-components.md §4.2 |

## Tools

Every script in `tools/` opens with a `Reads:`/`Writes:`/`Track:` header
stating what it touches and whether it belongs to the assisted or
automated refresh track (or is a shared helper/gating check used by both)
— check there before reading further into any one script's docstring for
the *why*.
