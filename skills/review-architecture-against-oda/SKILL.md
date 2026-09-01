---
name: review-architecture-against-oda
description: Given a description of a proposed or existing multi-component architecture (not scoped to one use case or one component), reviews it against the cached ODA corpus for duplicated ownership (a capability the architecture assigns to a new/custom component that an existing TMFCxxx already owns), point-to-point coupling (a direct interaction where an existing cached Open API already mediates that exact interaction type), and component-boundary bypass (a described interaction that reaches into another component's internals instead of its declared coreFunction). Use this for a whole-architecture ODA conformance review; see validate-design-against-oda for checking one design's specific claimed dependencies, and the audit-implementation-against-* skills for auditing one use case or one component already built.
---

# Review Architecture Against ODA — Skill Instructions

## What this skill answers

"Does this whole proposed (or existing) architecture actually respect ODA's component/API boundaries?" The only skill in this corpus that reasons about a *whole* multi-component architecture's ODA conformance at once, rather than one design's specific claims (`validate-design-against-oda`), one use case's flow (`audit-implementation-against-usecase`), or one component's contract (`audit-implementation-against-component`).

**ODA-first, not ODA-only.** Every finding below is about the architecture reaching for a custom construct where ODA already provides a real, cached equivalent — not a demand that everything be ODA. A genuine gap (no existing component/API covers the capability) is not a finding under this skill; check `knowledge/index/gaps-backlog.md` before flagging something as a violation, the same discipline `decompose-requirement-against-oda` Step 6 already applies.

## Step 1 — Parse the architecture into components and interactions

From the description (prose, a diagram's own description, or a list of services), extract: each component/service named, the capability it claims to own, and each direct interaction between two of them (what calls what, and how — a REST call, a direct database read, an event, etc.). Build this list before checking anything against the cached corpus, so the review isn't shaped by assuming which existing components are "obviously" the right fit.

## Step 2 — Check for duplicated ownership

For each capability the architecture assigns to a new or custom component, search `knowledge/index/components.json` by name/description for an existing `TMFCxxx` that already owns that same capability. If one exists, that's a finding: the architecture is duplicating ownership ODA already assigns elsewhere. Cite the real component id and name, not just "an ODA component probably covers this." If nothing in the cached corpus covers it, check `knowledge/index/gaps-backlog.md` before concluding — a genuine, already-logged gap is not duplicated ownership, it's the architecture correctly filling a real hole.

## Step 3 — Check for point-to-point coupling an existing API already mediates

For each direct interaction the architecture describes between two components, check `knowledge/index/apis.json` for a cached `TMFxxx` whose purpose matches that exact interaction (e.g. two components directly sharing a database table to exchange order status, where a cached Open API already defines a real order-status resource and event). If a real, cached API already mediates this kind of interaction, flag the architecture's direct/proprietary link as avoidable coupling — cite the specific API id that should mediate instead.

## Step 4 — Check for component-boundary bypass

For each interaction that targets a component with a real cached `TMFCxxx` id, check whether it goes through that component's own `coreFunction.exposedAPIs` (a real, declared interface) or reaches around it — a description like "reads directly from Y's database" or "calls Y's internal service directly, not through its API" is a boundary bypass, regardless of whether the target component is real or hypothetical. Cite the specific exposed API the interaction should have gone through, drawn from the real component's own `component.yaml`.

## Step 5 — Report the three categories separately

Duplicated ownership, point-to-point coupling, and boundary bypass are three distinct findings categories — report them separately, the same "don't blend dimensions into one score" discipline `audit-implementation-against-component` Step 4 uses. An architecture can be clean on one axis and have a real problem on another; a single aggregate verdict would hide that.

## Output format

Three sections — **Duplicated Ownership**, **Point-to-Point Coupling**, **Boundary Bypass** — each a findings list citing the real `TMFCxxx`/`TMFxxx` id involved, or explicitly stating "none found" for a category with no findings (not omitting the section). Close with anything Step 2/3 checked against `gaps-backlog.md` and confirmed as a genuine gap rather than a violation, so that distinction is visible in the output, not just made silently during the review.

## What this skill does NOT do

- Does not check one design's specific claimed field/operation-level dependencies — that's `validate-design-against-oda`, which operates on one design's stated assumptions, not a whole architecture's component boundaries.
- Does not audit an already-built system against one use case's flow or one component's full contract — that's `audit-implementation-against-usecase`/`audit-implementation-against-component`, both narrower in scope than this skill.
- Does not flag a genuine, already-logged capability gap as a violation — Step 2/6-style gap-backlog cross-checking is required before any duplicated-ownership finding is reported as such.
- Does not invent a component/API to flag an architecture against — every finding must cite a real, cached id.
- Does not modify the architecture description or the cached corpus — read-only, same posture as every other assurance skill here.
