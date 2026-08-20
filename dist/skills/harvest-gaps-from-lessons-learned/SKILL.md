---
name: harvest-gaps-from-lessons-learned
description: Mines every TMFSxxx use case's "Lessons learned"/"Impacts identified" sections for capability gaps TM Forum's own authors have already written down -- proposed new ODA components or Open APIs that don't exist yet -- cross-checks each against the current ${CLAUDE_PLUGIN_ROOT}/knowledge/index/{components,apis}.json to confirm it's still genuinely missing, and consolidates cross-corroborated gaps (the same gap raised independently in multiple use cases) into one backlog entry. Use this to find what ODA is missing without re-reading the whole corpus by hand.
---

# Harvest Gaps from Lessons Learned — Skill Instructions

## What this skill answers

"What capability gaps has TM Forum's own use-case corpus already identified, that nobody has aggregated into one place?" This is a §11.2 contributor-facing skill (spec.md), a different audience from §8/§11.1's consumer-facing skills — it's for someone deciding what ODA should build next, not someone building against what already exists.

**The core insight this skill is built on, confirmed against the real corpus before writing this**: 21 of the 24 converted use cases carry both a `## Lessons learned` and `## Impacts identified` subsection under their closing `# Conclusion`, and these sections are where authors record things they noticed were missing while writing the use case — sometimes with a real JIRA/TAC ticket already open, sometimes not. This is real, already-written contributor intent sitting unindexed in `${CLAUDE_PLUGIN_ROOT}/knowledge/use-cases/**`, not something to infer or guess at.

## Step 1 — Read the Lessons learned / Impacts identified section of every use case

```
${CLAUDE_PLUGIN_ROOT}/knowledge/use-cases/{ID}/{ID}.md
```

Find `## Lessons learned` (heading text and presence varies slightly — TMFS018 nests "Impacts identified" as a subheading *under* "Lessons learned" rather than as a sibling; TMFS009 has neither) and read through to the next `# Conclusion`-level section or `# Appendix`, whichever comes first. Don't read the whole document — this section only. If a use case has neither section (checked: only TMFS009, as of the current corpus), skip it and don't fabricate content for it.

## Step 2 — Classify what you find; most of it is NOT this skill's target

The volume of content here is large, and most of it is **not** a "new component/API" gap — don't harvest everything indiscriminately:

- **Enhancement requests to an existing API** ("add a PATCH operation," "add an attribute for X," most `AP-xxxx`/`ISA-xxxx` JIRA tickets) — these are evolution of something that already exists. Not this skill's target; there are far too many of these across the corpus to aggregate meaningfully, and they don't represent a missing *asset*.
- **SID (Information Framework) gaps** (e.g. "SoftwareSupportPackageSpec is missing in SID") — real gaps, but `${CLAUDE_PLUGIN_ROOT}/knowledge/sid/` is reserved and empty (spec.md §7) with nothing to cross-check against yet. Note these separately, lightly, without trying to verify them against a corpus that doesn't exist locally.
- **What this skill IS looking for**: an explicit proposal for a component or API that doesn't exist *at all* yet — signaled by a `TMFCxxx`/`TMFxxx` written with no real number (literal `TMFCxxx`/`TMFxxx` as placeholder text, not a redacted real id — same convention documented in `generate-test-cases-from-usecase/SKILL.md`), by prose like "a new component should be introduced," "there is no component exposing X," or by a `TAC-xxxx`-tracked "Create and Publish: TMFCxxx New ODA Component for..." ticket.

## Step 3 — Corroborate across use cases before treating anything as a single data point

**The single most valuable thing this skill does that reading one document at a time can't**: the same gap is frequently raised independently, in different words, by multiple use cases written at different times. Found while building this — a genuine cluster, not a hypothetical: an "API exposure / gateway" gap for B2B component-boundary translation is raised independently by TMFS018 (BuyerGW/SellerGW, tracked as TAC-841), TMFS021 (needs an exposure layer, no ticket), TMFS026 ("Open Gateway Façade"), and TMFS030 (formalizes it as a proposed "Delegate Component" type, citing a named Accelerate 2026 proposal) — four different documents, four different names for what is recognizably the same architectural gap. Don't report these as four separate backlog items; report one item citing all four sources, with TMFS030's as the most mature articulation since it's the most recent and most detailed.

Similarly, TMFS008 and TMFS011 independently cite the *same* JIRA ticket (`TAC-280`, "Service & Resource Orchestration") for a fallout/exception-handling capability — that shared ticket id is the corroboration signal, not something to infer from prose similarity alone.

## Step 4 — Cross-check every surviving gap against the current corpus

For each gap that survives Step 2/3, check `${CLAUDE_PLUGIN_ROOT}/knowledge/index/components.json` and `${CLAUDE_PLUGIN_ROOT}/knowledge/index/apis.json` for anything matching the proposed name or capability — a gap identified two years ago may already be resolved. **This isn't hypothetical — one of the use cases in this corpus self-reports exactly this**: TMFS030 itself notes "*That gap is addressed in TMFC027 v2.2.0, which was not yet available when this document began but has since appeared*" for a different, smaller gap in the same document. Don't trust a use case's own gap list as still-current without checking; report a gap as resolved (with the id that resolved it) rather than repeating stale information, and report a gap as still-open only after actually checking, not by assumption.

Also distinguish two different kinds of "missing" — don't conflate them in the backlog: a component id that's already assigned but `status: "not_yet_specified"` in `components.json` (TM Forum has reserved the id, e.g. `TMFC033` "Purchase Management" per TMFS020's own frontmatter, just hasn't published the spec) is a **different, more advanced** stage than a gap with no id assigned at all yet (the literal `TMFCxxx` placeholder cases from Step 2). Label each backlog entry with which stage it's at.

## Output format

A consolidated backlog, one entry per genuinely distinct gap (post-corroboration), each with: a short name, every use case that raises it (not just the first one found), any JIRA/TAC ticket ids cited, its current status per the Step 4 cross-check, and which corpus stage it's at (no id assigned / id assigned but not_yet_specified). Write this to `${CLAUDE_PLUGIN_ROOT}/knowledge/index/gaps-backlog.md`, in the same spirit as `${CLAUDE_PLUGIN_ROOT}/knowledge/index/matrix-discrepancies.md` — a logged, dated finding, not a one-off answer to a single query, since the value here is in the corpus-wide aggregation surviving past this one run.

## What this skill does NOT do

- Does not draft the proposed component/API itself — that's `propose-component-or-api-extension`'s job (spec.md §11.2). This skill only finds and consolidates the gap, it doesn't design the fix.
- Does not treat every JIRA-ticketed item as a gap for this backlog — Step 2's filter is required, not optional; a linter-style "count every ticket" run would drown the genuine new-asset gaps in enhancement-request noise.
- Does not report a gap as open without actually checking Step 4 against the current `${CLAUDE_PLUGIN_ROOT}/knowledge/index/*.json` — "the use case says it's missing" is a starting point, not the final answer.
