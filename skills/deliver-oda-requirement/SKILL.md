---
name: deliver-oda-requirement
description: Given a plain-language requirement, orchestrates the full Discover-to-Run chain of existing consumer skills against it -- finding or decomposing the requirement, capturing it as requirements, drafting architecture/event designs, gating on validate-design-against-oda, generating a Build-stage implementation (asking which of the two options to use, never defaulting), generating mocks/tests/conformance checks, and auditing the result. Use this for an end-to-end requirement delivery; it adds no ODA reasoning of its own -- every real decision is made by the skill it invokes at that step, not by this one.
---

# Deliver ODA Requirement — Skill Instructions

## What this skill answers

"Take this requirement all the way from a plain-language ask to a working, audited implementation." This is an **orchestration** skill, not a knowledge skill: it invokes the right existing skill at the right step and hands its output to the next one. It has no ODA reasoning of its own — every real judgment call (which use case matches, what the schema says, whether a design is sound) is made by the skill actually doing that step. If a step's output looks wrong, the fix belongs in that skill, not in this one's own logic.

**ODA-first, not ODA-only** — inherited from every skill this one invokes, not restated independently here. This skill's own job is sequencing, not judgment.

## The chain

```
requirement
    → recommend-oda-components-for-requirement  (Step 1)
       or decompose-requirement-against-oda      (Step 1, if that one comes up empty)
    → capture-requirements-from-usecase          (Step 2, once a use case is identified)
    → draft-architecture-diagram-from-usecase    (Step 3)
    → draft-event-design-for-component           (Step 4, only if new events are needed)
    → validate-design-against-oda                (Step 5 — gate)
    → generate-implementation-scaffold-from-usecase   (Step 6 — ASK which)
       or implement-oda-component                     (Step 6 — ASK which)
    → generate-api-mocks-from-usecase            (Step 7, parallel to Build)
    → generate-test-cases-from-usecase           (Step 8)
    → generate-api-conformance-tests             (Step 9, once a real implementation exists)
    → audit-implementation-against-usecase and/or audit-implementation-against-component  (Step 10)
```

## Step 1 — Find or decompose

Run `recommend-oda-components-for-requirement` against the requirement first, always. Read its own output honestly:
- If it found a real (even imperfect) matching use case, continue to Step 2 with that use case.
- If it explicitly came up empty (per its own Step 1's "if nothing matches closely, say so"), run `decompose-requirement-against-oda` instead. Its output may have no use case to hand to Step 2 at all — if `candidate_components`/`candidate_apis` are populated but there's no real `TMFSxxx` to anchor Step 2's requirements-capture on, say so and skip to Step 3 with the decomposition's own candidate architecture instead of forcing a nonexistent use case through Step 2.

## Step 2 — Capture requirements

Run `capture-requirements-from-usecase` against the identified use case. Skip this step (state explicitly that it's skipped, don't silently omit it) if Step 1 ended in a decomposition with no real use case to capture requirements from.

## Step 3 — Draft the architecture diagram

Run `draft-architecture-diagram-from-usecase` against the use case (or, absent one, describe that this step needs a real `TMFSxxx` to run against and is being skipped — don't force it against a bare component/API list the skill wasn't designed to read).

## Step 4 — Draft event design, only if needed

Run `draft-event-design-for-component` **only if the requirement or Step 1's output implies a new event is needed** that no existing component's `eventNotification` already covers — check this before running it, don't run it by default on every requirement. State explicitly whether this step ran or was judged unnecessary.

## Step 5 — Validate the design (gate)

Run `validate-design-against-oda` against whatever design has accumulated through Steps 1-4. **This is a real gate, not a formality**: if it reports drift, stop and surface that to the requester before proceeding to Step 6 — don't continue building against a design already flagged as resting on a false assumption.

**A real, non-buggy outcome of this step can be "nothing to validate."** Confirmed on a real pilot case: when Step 1 finds a genuinely close-matching use case (not a `decompose-requirement-against-oda` fallback) and Step 4 was judged unnecessary, the accumulated "design" is just that use case's own already-real, already-cached `links.components`/`links.apis` — there's no *novel* claim beyond what's already validated by the use case existing in the corpus at all. Report this plainly ("no new claims beyond the matched use case's own frontmatter — nothing for this gate to check") rather than inventing a claim to validate just to make this step look like it did something. The gate becomes materially meaningful specifically when Step 1's decomposition path or Step 4's event design introduces a claim that genuinely isn't already in the corpus.

## Step 6 — Build (ask which, never default)

**Explicitly ask which Build-stage option to use before proceeding — this is a hard requirement, not a suggestion:**

> "Two options for the Build step:
> 1. `generate-implementation-scaffold-from-usecase` — lightweight, language-agnostic, no side effects. Produces typed models and route stubs with `TODO` markers, nothing more.
> 2. `implement-oda-component` — TM Forum's own complete, opinionated Node.js/Helm reference stack. **Has real side effects**: writes source code and a Helm chart to the working directory, and can build/push Docker images and `helm install` into a real cluster if carried through its own Steps 7-9.
>
> Which would you like?"

If option 2 is chosen, state plainly (again, not just once in this prompt) that the invoked skill has real side effects before it runs — the same disclosure `implement-oda-component`'s own `SKILL.md` requires of itself, restated here since this orchestrator is what a caller sees first.

## Step 7 — Generate mocks

Run `generate-api-mocks-from-usecase` against the use case's linked APIs. This can run in parallel with Step 6's real backend work conceptually, but sequence it after Step 6 in this orchestration's own execution — there's no dependency forcing a particular order, but running it right after Build keeps the mocks available immediately for whatever Step 8/9 need next.

## Step 8 — Generate test cases

Run `generate-test-cases-from-usecase` against the use case.

## Step 9 — Generate conformance tests, once there's something to test

Run `generate-api-conformance-tests` against the APIs involved. If Step 6 produced only a scaffold with no real running implementation (option 1, or option 2 without carrying through its own Steps 7-9), this step produces a standalone suite "ready to run once an implementation exists," per that skill's own output format — don't fabricate a pass/fail here just because a Build step ran.

## Step 10 — Audit

Choose based on what actually exists to audit:
- A specific use case's flow was implemented → `audit-implementation-against-usecase`.
- A specific component's full contract needs checking, independent of one use case → `audit-implementation-against-component`.
- Both are relevant (a component-scoped implementation specifically delivering this use case) → run both, and report their findings separately — don't blend a flow-level finding with a boundary-level one into one summary.

## Output format

A short log of which step ran, which skill it invoked, and a one-line summary of that skill's own output — not a full re-print of every intermediate skill's complete output (the caller can open any step's own result if they need the detail). End with what was skipped and why (Step 4 judged unnecessary, Step 2/3 skipped for lack of a real use case, etc.) so a reader can see the whole run's shape at a glance.

## What this skill does NOT do

- Does not perform any ODA reasoning itself — every judgment call belongs to the skill invoked at that step. If a step's output seems wrong, fix that skill, not this orchestrator's own logic.
- Does not default the Step 6 Build-stage choice — asking is required output, every time, not a one-time setup question.
- Does not run `draft-event-design-for-component` unconditionally — Step 4 requires checking whether a new event is actually needed first.
- Does not fabricate a pass/fail conformance result when no real implementation exists yet — Step 9 defers to `generate-api-conformance-tests`'s own honest "standalone suite" framing.
- Does not silently skip a step for lack of a real use case — Step 1's decomposition path requires stating explicitly which downstream steps don't apply and why.
