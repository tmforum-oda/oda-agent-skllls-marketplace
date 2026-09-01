---
name: audit-implementation-against-component
description: Given a TMFCxxx component id and a description of an existing implementation, checks conformance at Component-boundary granularity, split explicitly the way component.yaml itself is split -- Core Function (does it expose/consume the real exposedAPIs/dependentAPIs) and Supporting Function (does it provide the managementFunction/securityFunction behaviors the spec describes) -- reported as two separate dimensions, never blended into one score. Use this to audit a component's full contract independent of any specific use case; see audit-implementation-against-usecase for flow-level auditing against one use case's narrative instead.
---

# Audit Implementation Against Component — Skill Instructions

## What this skill answers

"Does our implementation of TMFCxxx actually honor the component's full contract?" The boundary-level counterpart to `audit-implementation-against-usecase`, which checks *flow* fidelity against one use case's narrative — this skill checks *contract* fidelity against one component's own spec, independent of which use case (if any) is driving the audit.

## Step 1 — Establish the real contract before looking at the implementation

Look up the id in `knowledge/index/components.json`. A `status` of `not_yet_specified` means there's no real Core Function contract to audit against — say so and stop. Otherwise read `knowledge/components/{TMFCxxx}/component.yaml` directly and split it into the two dimensions the spec itself already draws (confirmed structurally consistent across every component checked so far, e.g. `TMFC012`, `TMFC062`):

- **Core Function** (`spec.coreFunction`): `exposedAPIs` (each with a real `id` and a `required: true/false` flag) and `dependentAPIs`.
- **Supporting Function** (`spec.managementFunction`, `spec.securityFunction`): a metrics endpoint (`managementFunction.exposedAPIs`, typically `apiType: prometheus`), and a security role/secrets pattern (`securityFunction.exposedAPIs` — typically `TMF669` or `TMF672` party-role/permission management, `required: true`, plus `secretsManagement`/`canvasSystemRole`).

Build both checklists from the spec alone, before reading anything about the implementation — the same discipline `audit-implementation-against-usecase` Step 2 already uses, so the audit isn't unconsciously shaped by what the implementation already does.

## Step 2 — Audit Core Function conformance

For each `exposedAPIs` entry, check whether the implementation actually exposes that API — and specifically, whether the operations it serves match the cached schema (`knowledge/apis/{TMFxxx}/{TMFxxx}_v{version}.json`), the same way `audit-implementation-against-usecase` Step 3 checks calls against a schema. Distinguish `required: true` from `required: false` in the finding — a missing optional API is a real but lower-severity gap than a missing mandatory one, and the report must say which.

For each `dependentAPIs` entry, check whether the implementation actually calls it, and whether the calls target real operations in that API's own cached schema. **`dependentAPIs` entries carry their own `required` flag too, not just `exposedAPIs`** — confirmed on `TMFC012`, where `TMF634` is `required: true` while `TMF669`/`TMF632`/`TMF673`/`TMF674`/`TMF675`/`TMF639` are all `required: false` dependents. Apply the same required-vs-optional severity distinction to a missing dependent call as to a missing exposed API — don't report every uncalled dependent at the same severity just because the field lives in a different list.

## Step 3 — Audit Supporting Function conformance, separately

Check the metrics endpoint against `managementFunction.exposedAPIs`'s declared `path`/`port` pattern (`/{{.Release.Name}}-{{.Values.component.name}}/metrics` is the corpus's own template — an implementation doesn't need the literal Helm-templated string, but should have an equivalent metrics surface at an analogous path). Check the security role pattern against `securityFunction.exposedAPIs` (does the implementation actually integrate with the declared party-role/permission API, or handle authorization some other, non-conforming way) and `secretsManagement` (does it follow the declared pattern — e.g. sidecar-based — or a different one).

This is necessarily a looser match than Step 2's schema-level check — Supporting Functions describe integration *patterns*, not exact operation calls. Report each as **present** (a real, recognizable equivalent exists), **absent** (no equivalent found), or **partial** (an equivalent exists but doesn't fully match the declared pattern), not a strict pass/fail.

## Step 4 — Report the two dimensions separately, never blended

Core Function and Supporting Function conformance are reported as two distinct sections with their own findings — never averaged or combined into one score. A component can be fully Core-Function-conformant while having no real metrics endpoint at all, and that's a meaningful, specific finding a blended score would hide.

## Output format

Two sections, **Core Function** and **Supporting Function**, each a findings list (not a pass/fail verdict) citing the real spec element every finding traces to (`spec.coreFunction.exposedAPIs[TMF716].required: true`) and, for Core Function findings, whether the gap is on a required or optional API.

## What this skill does NOT do

- Does not blend Core Function and Supporting Function conformance into one score — Step 4's separation is required output, not a stylistic choice.
- Does not check flow fidelity against a specific use case's narrative — that's `audit-implementation-against-usecase`; this skill is scoped to the component's own contract, independent of any use case.
- Does not invent a Core or Supporting Function requirement not present in the real cached `component.yaml` — an audit finding must trace to a real spec element.
- Does not modify the implementation or the cached spec — read-only, same posture as every other audit/assurance skill in this corpus.
- Does not treat a missing optional (`required: false`) exposed API the same as a missing mandatory one — Step 2's severity distinction is required, not optional detail.
