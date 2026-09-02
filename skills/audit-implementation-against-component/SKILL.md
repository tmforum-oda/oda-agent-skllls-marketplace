---
name: audit-implementation-against-component
description: Given a TMFCxxx component id and a description of an existing implementation, checks conformance at Component-boundary granularity, split explicitly the way component.yaml itself is split -- Core Function (does it expose/consume the real exposedAPIs/dependentAPIs) and Supporting Function (does it provide the managementFunction/securityFunction behaviors the spec describes) -- reported as two separate dimensions, never blended into one score. Use this to audit a component's full contract independent of any specific use case; see audit-implementation-against-usecase for flow-level auditing against one use case's narrative instead.
---

# Audit Implementation Against Component — Skill Instructions

## What this skill answers

"Does our implementation of TMFCxxx actually honor the component's full contract?" The boundary-level counterpart to `audit-implementation-against-usecase`, which checks *flow* fidelity against one use case's narrative — this skill checks *contract* fidelity against one component's own spec, independent of which use case (if any) is driving the audit.

## Step 1 — Establish the real contract before looking at the implementation

Look up the id in `knowledge/index/components.json`. If the id isn't in the
index at all, say so plainly rather than guessing a nearby id — that's a
different, more basic problem than the next check. A `status` of
`not_yet_specified` means the id is real but there's no real Core Function
contract to audit against yet — say so and stop. Otherwise read
`knowledge/components/{TMFCxxx}/component.yaml` directly and split it into
the two dimensions the spec itself already draws (confirmed structurally
consistent across every one of the 26 currently-cached components, e.g.
`TMFC012`, `TMFC062`):

- **Core Function** (`spec.coreFunction`): `exposedAPIs` (each with a real `id` and a `required: true/false` flag) and `dependentAPIs`.
- **Supporting Function** (`spec.managementFunction`, `spec.securityFunction`): a metrics endpoint (`managementFunction.exposedAPIs`, typically `apiType: prometheus`), and a security role/secrets pattern (`securityFunction.exposedAPIs` — typically `TMF669` or `TMF672` party-role/permission management, `required: true`, plus `secretsManagement`/`canvasSystemRole`).

**One data-quality trap in `managementFunction`, confirmed in every one of
the 26 cached components, not an occasional glitch**: `managementFunction.
exposedAPIs[].id`/`.version`/`.developerUI` are always the literal unfilled
strings `"exposedAPI_id"`/`"exposedAPI_version"`/`"exposedAPI_developerUI"`
— TM Forum's own spec template, never customized per component — and
`managementFunction.dependentAPIs` is always one entry of the same kind of
placeholder (`"dependentAPI_id"`, `"dependentAPI_name"`, etc., `url:
"dependentAPI_spec"`). Only `name` (real: `"metrics"`), `apiType` (real:
`"prometheus"`), and the `path`/`port`/`implementation` Helm-template
strings in `managementFunction.exposedAPIs` carry actual information —
`securityFunction.exposedAPIs` doesn't have this problem (its `id`/`name`
are always real API ids like `TMF669`, confirmed across all 26). Treat
`managementFunction.dependentAPIs` as always empty of real content and
never cite its placeholder fields as if they were a genuine spec fact — the
same discipline `generate-test-cases-from-usecase` already applies to a
TM Forum author's own `TMFC???` placeholders: a template gap TM Forum left
unfilled is real, surveyed information about the spec, not something to
paper over by treating it as data.

Build both checklists from the spec alone, before reading anything about the implementation — the same discipline `audit-implementation-against-usecase` Step 2 already uses, so the audit isn't unconsciously shaped by what the implementation already does.

## Step 2 — Audit Core Function conformance

For each `exposedAPIs` entry, check whether the implementation actually exposes that API — and specifically, whether the operations it serves match the cached schema (`knowledge/apis/{TMFxxx}/{TMFxxx}_v{version}.json`), the same way `audit-implementation-against-usecase` Step 3 checks calls against a schema. Distinguish `required: true` from `required: false` in the finding — a missing optional API is a real but lower-severity gap than a missing mandatory one, and the report must say which.

For each `dependentAPIs` entry, check whether the implementation actually calls it, and whether the calls target real operations in that API's own cached schema. **`dependentAPIs` entries carry their own `required` flag too, not just `exposedAPIs`** — confirmed on `TMFC012`, where `TMF634` is `required: true` while `TMF669`/`TMF632`/`TMF673`/`TMF674`/`TMF675`/`TMF639` are all `required: false` dependents. Apply the same required-vs-optional severity distinction to a missing dependent call as to a missing exposed API — don't report every uncalled dependent at the same severity just because the field lives in a different list.

## Step 3 — Audit Supporting Function conformance, separately

Check the metrics endpoint against `managementFunction.exposedAPIs`'s declared `path`/`port` pattern (`/{{.Release.Name}}-{{.Values.component.name}}/metrics` is the corpus's own template — an implementation doesn't need the literal Helm-templated string, but should have an equivalent metrics surface at an analogous path). Don't extend this check to `managementFunction.dependentAPIs` or to the `id`/`version`/`developerUI` fields on the exposed metrics entry itself — per Step 1, those are TM Forum's own unfilled template placeholders in every cached component, not something this specific component actually declares. Check the security role pattern against `securityFunction.exposedAPIs` (does the implementation actually integrate with the declared party-role/permission API, or handle authorization some other, non-conforming way) and `secretsManagement` (does it follow the declared pattern — e.g. sidecar-based — or a different one).

This is necessarily a looser match than Step 2's schema-level check — Supporting Functions describe integration *patterns*, not exact operation calls. Report each as **present** (a real, recognizable equivalent exists), **absent** (no equivalent found), or **partial** (an equivalent exists but doesn't fully match the declared pattern), not a strict pass/fail.

## Step 4 — Report the two dimensions separately, never blended

Core Function and Supporting Function conformance are reported as two distinct sections with their own findings — never averaged or combined into one score. A component can be fully Core-Function-conformant while having no real metrics endpoint at all, and that's a meaningful, specific finding a blended score would hide.

## Output format

Two sections, **Core Function** and **Supporting Function**, each a findings list (not a pass/fail verdict) citing the real spec element every finding traces to (`spec.coreFunction.exposedAPIs[TMF716].required: true`) and, for Core Function findings, whether the gap is on a required or optional API.

## What this skill does NOT do

- Does not blend Core Function and Supporting Function conformance into one score — Step 4's separation is required output, not a stylistic choice.
- Does not check flow fidelity against a specific use case's narrative — that's `audit-implementation-against-usecase`; this skill is scoped to the component's own contract, independent of any use case.
- Does not invent a Core or Supporting Function requirement not present in the real cached `component.yaml` — an audit finding must trace to a real spec element.
- Does not cite `managementFunction.dependentAPIs` or the `id`/`version`/`developerUI` fields under `managementFunction.exposedAPIs` as if they were real per-component data — Step 1's trap is required output when a Supporting Function finding touches this area, not a detail to silently work around.
- Does not modify the implementation or the cached spec — read-only, same posture as every other audit/assurance skill in this corpus.
- Does not treat a missing optional (`required: false`) exposed API the same as a missing mandatory one — Step 2's severity distinction is required, not optional detail.
