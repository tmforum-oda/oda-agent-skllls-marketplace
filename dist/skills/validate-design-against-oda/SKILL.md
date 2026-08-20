---
name: validate-design-against-oda
description: Given a proposed component or API design that claims to extend or depend on existing ODA components/APIs, checks those claims against the real cached specs and flags drift -- fields, operations, or behavior the design assumes exist but don't. Use this before building against an assumed ODA capability, to confirm the assumption is real.
---

# Validate Design Against ODA — Skill Instructions

## What this skill answers

"Does this proposed design's assumptions about existing ODA components/
APIs actually hold?" A pre-build check on a design someone has already
sketched — the mirror of `propose-component-or-api-extension`, which
drafts a new proposal from a gap, and of `audit-implementation-against-usecase`,
which checks something already built. This skill sits earlier: check the
assumptions before either building or extending against them.

## Step 1 — Identify every existing component/API the design claims to touch

From the proposed design, list every `TMFCxxx`/`TMFxxx` id it names, plus
every capability it describes in prose without an id ("extends Party
Management to add X," "depends on the Quote API for Y"). For prose
references, resolve them to a real id via `${CLAUDE_PLUGIN_ROOT}/knowledge/index/{components,apis}.json`
by name — same discipline as every other skill here: don't validate
against an id the design merely implies, validate against the real one.

## Step 2 — Read the real spec for each

```
${CLAUDE_PLUGIN_ROOT}/knowledge/components/{TMFCxxx}/component.yaml
${CLAUDE_PLUGIN_ROOT}/knowledge/apis/{TMFxxx}/{TMFxxx}_v{version}.json
```

For a component, check `componentMetadata.status` — a design extending a
`not_yet_specified` component has nothing real to extend yet; flag that
directly. For an API, read the actual `paths`/`definitions` the design's
claims depend on.

## Step 3 — Check every claim against the real content, not the design's own description of it

This is the actual validation, and it has to be checked against the
schema directly, not assumed from the design's own summary of what it
depends on:

- A field the design assumes exists on a resource (e.g. "extends the
  Individual resource's `loyaltyPoints` field") — check the real
  `definitions` block for that resource. If the field isn't there, this
  isn't an "extension," it's a genuinely new field the design is adding
  — say so, don't let the design's own framing ("extends") stand
  uncorrected if what it actually does is add something new.
- An operation the design assumes is available (a specific HTTP
  method on a specific path) — check `paths` for that exact
  method+path combination.
- A version assumption — if the design assumes v5 behavior but only v4
  is cached in `${CLAUDE_PLUGIN_ROOT}/knowledge/index/apis.json` for that id (or vice versa),
  flag the mismatch explicitly rather than validating against whichever
  version happens to be cached.

## Step 4 — Distinguish "doesn't exist yet" from "doesn't exist at all"

If a claimed capability isn't in the cached spec, check
`${CLAUDE_PLUGIN_ROOT}/knowledge/index/gaps-backlog.md` before reporting it as simply wrong —
it may be a known, already-corroborated gap the design is correctly
anticipating, not a design error. Report these differently: a claim
matching a known gap is "building ahead of a real, tracked gap," not
drift to be fixed.

## Output format

A findings list: for each claim, whether it holds against the real spec,
and if not, whether it's (a) a genuine addition mischaracterized as an
extension, (b) a version mismatch, or (c) building against a known gap
per Step 4. Don't summarize with a single pass/fail — a design can be
mostly sound with one real drift point, and the report should let a
reviewer see exactly which claim that is.

## What this skill does NOT do

- Does not validate the design's own internal logic or business correctness — only whether its stated dependencies on existing ODA components/APIs actually hold against the cached specs.
- Does not modify the design or the cached specs — read-only, same posture as `assess-change-impact` and `audit-implementation-against-usecase`.
- Does not treat a mismatch against a known gap-backlog entry the same as an unexplained drift — Step 4's distinction is required output.
