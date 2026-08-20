---
name: assess-change-impact
description: Given a TM Forum ODA component (TMFCxxx) or Open API (TMFxxx) id and a proposed change (deprecation, breaking version bump, removal), lists every TMFSxxx use case that depends on it and drafts a migration/impact report grounded in already-computed reverse links. Reads only ${CLAUDE_PLUGIN_ROOT}/knowledge/index/*.json, no document-body parsing. Use this before deprecating, breaking, or removing a component or API.
---

# Assess Change Impact — Skill Instructions

## What this skill answers

"If we change TMFC020 (or TMF632, or a specific version of it), which use
cases break, and how risky is that?" A pure reverse-link traversal over
data `tools/build_index.py` already computes, plus a maturity cross-check
— no document-body reading, no judgment calls about what a use case's
prose means.

## Step 1 — Identify the id type and look it up

`TMFCxxx` is a component, `TMFxxx` (not `TMFCxxx`) is an API — the id's
own shape tells you which without asking. Look it up in the matching
index file:

```
${CLAUDE_PLUGIN_ROOT}/knowledge/index/components.json   -- one row per component, keyed by id
${CLAUDE_PLUGIN_ROOT}/knowledge/index/apis.json         -- one row per (id, version) pair
```

**Components are unique per id** — `components.json` has exactly one row
per `TMFCxxx`, so there's no ambiguity to resolve.

**APIs are not** — `apis.json` can have multiple rows for the same `id`
at different `version`s, since `fetch_api.py` allows multiple versions of
one API to be cached side by side. If the proposed change is
version-specific ("deprecating v4 in favor of v5"), match on **both**
`id` and `version` and report only that version's `used_by` — merging
across versions would overstate the blast radius of a version-specific
change. If the caller hasn't specified a version, list every cached
version's `used_by` separately, not merged into one number.

If the id isn't in the index at all, say so plainly — don't guess a
nearby id. A component with `status: "not_yet_specified"` or an API with
`status: "fetch_failed"` has no real spec to change yet; report that
directly rather than proceeding as if it had one.

## Step 2 — Read `used_by`, already computed

Every row in `components.json`/`apis.json` carries a `used_by` field —
sorted `TMFSxxx` ids, computed once by `build_index.py` from every use
case's own `links.components`/`links.apis` forward links. This is the
entire "which use cases depend on this" answer — no need to grep the
corpus.

**One real caveat, worth stating in the output, not just knowing
privately**: `used_by` is only as complete as the frontmatter it's built
from, and frontmatter is not always exhaustive of a use case's real
dependencies — `docx2md.py`'s extraction is scoped to a document's own
References section. A component/API a use case names only in body prose
(like TMFS020's own `TMFC001`/`002`/`023`) won't show up in `used_by` at
all. Also cross-check `${CLAUDE_PLUGIN_ROOT}/knowledge/index/usecase-component-matrix.json` and
`${CLAUDE_PLUGIN_ROOT}/knowledge/index/matrix-discrepancies.md` for the same id — if the id is
one of the matrix-only entries there, the real blast radius is larger
than `used_by` alone suggests. Say so in the report rather than silently
presenting `used_by` as the complete picture.

## Step 3 — Cross-check each affected use case's own maturity

For every id in `used_by`, look up that row in `${CLAUDE_PLUGIN_ROOT}/knowledge/index/use-cases.json`
and read its `maturity`/`approval_status`/`release_status` fields (the
same ones `check-usecase-maturity` reads). This is what turns a bare list
of ids into an actual risk assessment:

- `GA` / `TM Forum Approved` use cases are firm, stable dependents — a
  breaking change here has real consumers relying on the current shape.
- `Alpha`/`Beta` use cases are still provisional themselves (per
  `check-usecase-maturity`'s own decision table) — a dependent that's
  itself not yet settled is lower-risk to disrupt than one that's GA.

Don't just list affected ids — group or flag them by this distinction so
the reader can see at a glance which dependents actually matter for a
go/no-go decision, versus which are still exploratory anyway.

## Output format

A short report, not a raw dump of `used_by`. Example, for "deprecating
TMF632 v4.0.0":

> **TMF632 v4.0.0** (Party Management, currently generation `v4`) — 6
> use cases depend on it via their own frontmatter:
>
> | Use case | Maturity / approval | Risk |
> |---|---|---|
> | TMFS001 | GA / TM Forum Approved | **High** — stable, real dependency |
> | TMFS006 | GA / TM Forum Approved | **High** |
> | TMFS004 | GA / TM Forum Approved | **High** |
> | TMFS016 | GA / TM Forum Approved | **High** |
> | TMFS030 | Beta / Member Evaluated | Low — itself still provisional |
> | TMFS031 | Alpha / Member Evaluated | Low — itself still provisional |
>
> 4 of 6 dependents are GA — a breaking change to TMF632 v4 needs a
> migration path for those before it ships. `used_by` is frontmatter-derived
> only; not cross-checked against the matrix for this id in this run.

Always state whether the matrix cross-check (Step 2's caveat) was
actually done for this particular id, not just that the caveat exists in
the abstract.

## What this skill does NOT do

- Does not read any use case's document body — only the three
  `${CLAUDE_PLUGIN_ROOT}/knowledge/index/*.json` files and nothing else. If the caller needs to
  know *how* a use case uses the component/API (which step, which
  operation), that's `generate-test-cases-from-usecase`'s job, not this
  skill's.
- Does not modify anything — this is a read-only impact report to inform
  a human decision, not an automated approval or rejection of the change.
- Does not assume `used_by` is exhaustive — Step 2's caveat is required
  output, not optional caution.
