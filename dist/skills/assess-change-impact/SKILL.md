---
name: assess-change-impact
description: Given a TM Forum ODA component (TMFCxxx) or Open API (TMFxxx) id and a proposed change (deprecation, breaking version bump, removal), lists every TMFSxxx use case that depends on it, describes specifically how each one uses it, and drafts a maturity-weighted migration/impact report. Use this before deprecating, breaking, or removing a component or API.
---

# Assess Change Impact — Skill Instructions

## What this skill answers

"If we change TMFC020 (or TMF632, or a specific version of it), which use
cases break, how exactly do they depend on it, and how risky is that?"

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
at different `version`s, since more than one version of an API can be
cached side by side. If the proposed change is version-specific
("deprecating v4 in favor of v5"), match on **both** `id` and `version`
and report only that version's `used_by` — merging across versions would
overstate the blast radius of a version-specific change. If the caller
hasn't specified a version, list every cached version's `used_by`
separately, not merged into one number.

If the id isn't in the index at all, say so plainly — don't guess a
nearby id. A component with `status: "not_yet_specified"` or an API with
`status: "fetch_failed"` has no real spec to change yet; report that
directly rather than proceeding as if it had one.

## Step 2 — Read `used_by`

Every row in `components.json`/`apis.json` carries a `used_by` field —
sorted `TMFSxxx` ids of every use case whose own frontmatter links to
this component/API. This is the starting "which use cases depend on
this" list.

**One real caveat, worth stating in the output, not just knowing
privately**: `used_by` is only as complete as the frontmatter it's built
from, and frontmatter isn't always exhaustive of a use case's real
dependencies — a use case's References section drives this extraction,
so a component/API named only in body prose elsewhere in the document
(like TMFS020's own `TMFC001`/`002`/`023`) won't show up in `used_by` at
all. Also cross-check `${CLAUDE_PLUGIN_ROOT}/knowledge/index/usecase-component-matrix.json` and
`${CLAUDE_PLUGIN_ROOT}/knowledge/index/matrix-discrepancies.md` for the same id — if the id is
one of the matrix-only entries there, the real blast radius is larger
than `used_by` alone suggests. Say so in the report rather than silently
presenting `used_by` as the complete picture.

## Step 3 — Cross-check each affected use case's own maturity

For every id in `used_by`, look up that row in `${CLAUDE_PLUGIN_ROOT}/knowledge/index/use-cases.json`
and read its `maturity`/`approval_status`/`release_status` fields (the
same ones `check-usecase-maturity` reads):

- `GA` / `TM Forum Approved` use cases are firm, stable dependents — a
  breaking change here has real consumers relying on the current shape.
- `Alpha`/`Beta` use cases are still provisional themselves (per
  `check-usecase-maturity`'s own decision table) — a dependent that's
  itself not yet settled is lower-risk to disrupt than one that's GA.

## Step 4 — Describe specifically how each affected use case depends on it

A bare id + maturity level isn't enough detail to act on — read each
affected use case's own document to find *how* it actually uses the
component/API, the same way `generate-test-cases-from-usecase` resolves
a use case's real interaction flow:

```
${CLAUDE_PLUGIN_ROOT}/knowledge/use-cases/{ID}/{ID}.md
```

Search the `# Description` and `# Sequence diagrams` sections for where
the target id (or its name) actually appears, including the diagram
images themselves where relevant — the real step-by-step usage often
lives there, not just in a components list. Summarize specifically what
the use case does with it (e.g. "TMFC020 verifies the customer's identity
at account-creation step 2, before Party Management proceeds" rather than
"TMFS001 depends on TMFC020"). This is what turns "6 use cases are
affected" into something a reviewer can actually act on — which specific
step in each use case's flow needs a migration plan, not just which ids
are on a list.

For a long `used_by` list, prioritize this detailed read for the
highest-risk (GA/TM Forum Approved) dependents first — do all of them if
asked, but don't let a large list become an excuse to skip Step 4
entirely for the ones that matter most.

## Output format

A short report, not a raw dump of `used_by`. Example, for "deprecating
TMF632 v4.0.0":

> **TMF632 v4.0.0** (Party Management, currently generation `v4`) — 6
> use cases depend on it via their own frontmatter:
>
> | Use case | Maturity / approval | Risk | How it's actually used |
> |---|---|---|---|
> | TMFS001 | GA / TM Forum Approved | **High** | Creates the Individual resource at account-creation step 3; also read/updated later for profile changes |
> | TMFS006 | GA / TM Forum Approved | **High** | Looks up the existing Individual to attach a Legal Guardian relationship |
> | TMFS030 | Beta / Member Evaluated | Low — itself still provisional | References the Party as the MNO/SNO contracting entity, not a core flow step |
>
> 4 of 6 dependents are GA — a breaking change to TMF632 v4 needs a
> migration path for those before it ships, starting with TMFS001's
> create-and-update flow since it's the deepest dependency. `used_by` is
> frontmatter-derived only; not cross-checked against the matrix for this
> id in this run.

Always state whether the matrix cross-check (Step 2's caveat) was
actually done for this particular id, not just that the caveat exists in
the abstract.

## What this skill does NOT do

- Does not modify anything — this is a read-only impact report to inform a human decision, not an automated approval or rejection of the change.
- Does not assume `used_by` is exhaustive — Step 2's caveat is required output, not optional caution.
- Does not stop at a bare id list — Step 4's per-use-case detail is required for at least the high-risk dependents, not an optional enrichment.
