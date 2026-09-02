---
name: propose-component-or-api-extension
description: Given a capability gap (e.g. from knowledge/index/gaps-backlog.md) and the nearest existing component/API, drafts a proposed extension -- a new component skeleton in IG1242's real shape, or a new field/endpoint on an existing OpenAPI schema -- consistent with the corpus's own conventions and grounded in a real cached spec. Use this to design a fix for a gap, not just identify one.
---

# Propose Component or API Extension — Skill Instructions

## What this skill produces

A concrete draft — a new component skeleton or an API schema extension —
for a gap that's already been identified, most often one already logged
in `knowledge/index/gaps-backlog.md`. This picks up where
`feedback-harvest-gaps-from-lessons-learned` leaves off: that skill finds and
consolidates the gap, this one designs the fix.

## Step 1 — Ground the gap first

If the gap comes from `knowledge/index/gaps-backlog.md`, read that
entry's full citation list (every use case that raises it, every
JIRA/TAC ticket) before drafting anything — a proposal that only
addresses one of several use cases' framings of the same gap is
incomplete. If the gap is new (not already in the backlog), state that
explicitly and note it hasn't been cross-corroborated the way the
backlog entries have.

## Step 2 — For a new component, use the real IG1242 shape

Read an existing component similar in scope to the proposed one (e.g. a
component in the same functional block) to see the real shape:

```
knowledge/components/{TMFCxxx}/component.yaml
```

The real structure: `spec.componentMetadata` (`id`/`name`/`version`/
`description`/`status`/`functionalBlock`/`owners`/`maintainers`/`eTOMs`/
`functionalFrameworkFunctions`/`SIDs`), then `spec.coreFunction`/
`managementFunction`/`securityFunction`, each with `exposedAPIs`/
`dependentAPIs` lists (`id`/`apiType`/`apiSDO`/`name`/`required`/
`specification`/`resources`), and `spec.eventNotification`. Draft the
proposal in this same shape — a reader familiar with real ODA component
specs should recognize the structure immediately, not have to translate
a different format.

Use a literal `TMFCxxx` placeholder for `componentMetadata.id` (no real
digits) and `status: "proposed"` — never assign a real id or claim
`status: "specified"` for something that hasn't gone through TM Forum's
own publication process.

For `dependentAPIs`/`exposedAPIs`, cite real API ids from
`knowledge/index/apis.json` wherever the gap's own description names a
capability that already has a real API — e.g. a proposal reusing party
data should cite the real `TMF632`, not invent a new one for a capability
that already exists.

## Step 3 — For an API extension, ground it in the real cached schema

```
knowledge/apis/{TMFxxx}/{TMFxxx}_v{version}.json
```

Read the existing `paths`/`definitions` before proposing a new field or
endpoint — match the schema's existing naming conventions (property
casing, resource naming pattern) rather than introducing a
differently-styled addition. State clearly which parts are the existing,
real schema (unchanged) and which are the proposed addition — a reviewer
needs to see the diff, not a full schema that mixes real and proposed
content indistinguishably.

## Step 4 — Note what the proposal does NOT resolve

A proposal at this stage is a design sketch for review, not a finished
spec — call out open questions explicitly (e.g. which functional block a
new component belongs in, if that's genuinely ambiguous between two
plausible answers) rather than picking one silently. A reviewer should
be able to see exactly what still needs a decision.

## Output format

For a new component: a `component.yaml`-shaped draft per Step 2, with a
short preamble stating which gap-backlog entry it addresses and which
use cases' framings it was checked against. For an API extension: the
specific added `paths`/`definitions` entries per Step 3, clearly marked
as additions to the named existing schema, not a full replacement.

## What this skill does NOT do

- Does not assign a real `TMFCxxx`/`TMFxxx` id or claim TM Forum publication status — this is a proposal, not a specification.
- Does not invent dependent/exposed APIs that don't exist — every API cited in a new component draft must be a real id from `knowledge/index/apis.json`, or explicitly marked as itself a new, proposed API rather than presented as if it already existed.
- Does not resolve genuine open design questions on its own — Step 4's caveats are required output, not optional hedging.
