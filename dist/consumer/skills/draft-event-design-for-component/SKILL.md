---
name: draft-event-design-for-component
description: Given a TMFCxxx component id (or one identified via decompose-requirement-against-oda/recommend-oda-components-for-requirement) and the APIs it exposes or depends on, drafts published/subscribed event definitions in the same shape every cached component.yaml's eventNotification block already uses -- resource-level create/attributeValueChange/stateChange/delete events tied to real resource names, never invented event types. Use this when a design needs new events and no existing eventNotification entry already covers them.
---

# Draft Event Design for Component — Skill Instructions

## What this skill answers

"This component needs to publish or subscribe to an event that doesn't exist in its cached spec yet — what should it look like?" A Design-stage skill: it drafts an addition consistent with how every other cached component already expresses events, it doesn't invent a new event-modeling convention.

**ODA-first, not ODA-only.** Check whether the event this design needs is already covered by an existing `eventNotification` entry — on this component or, if the event really belongs to a dependent API, on the component that actually owns that API — before drafting a new one. Draft only what's genuinely missing.

## Step 1 — Read the target component's own existing `eventNotification` block

```
${CLAUDE_PLUGIN_ROOT}/knowledge/components/{TMFCxxx}/component.yaml  →  spec.eventNotification.{publishedEvents,subscribedEvents}
```

Each entry is one API the component publishes events for (or subscribes to events from), shaped:

```yaml
- hub: "/{{.Release.Name}}-.../tmf-api/{apiName}/hub"          # publishedEvents only
  implementation: "/{{.Release.Name}}-{EventServiceName}"
  name: {ApiDisplayName}
  port: 80
  resources: [ {resourceName}CreateEvent, {resourceName}AttributeValueChangeEvent,
               {resourceName}StateChangeEvent, {resourceName}DeleteEvent, ... ]
  specification:
    - url: {the API's real swagger/OpenAPI spec URL}
      version: v{n}
  apiType: openapi
  id: TMFxxx
  apiSDO: not_defined
```

A `subscribedEvents` entry additionally carries a `callback` field (the inbound hub URL this component registers against the source API's hub).

**The `resources` naming isn't perfectly uniform across the corpus** — confirmed by comparing multiple real components directly: some use `{resource}CreateEvent`/`{resource}DeleteEvent`, others drop the `Event` suffix on `Create` (`{resource}Create`) while keeping it on the rest, and casing conventions vary slightly. **Fallback only, when Step 2's schema-defined event names aren't available**: match the target component's own existing style if it already has at least one `eventNotification` entry — don't impose a different convention just because another component does it differently. If neither the schema nor this component's own precedent settles it, use the majority pattern (`{resource}CreateEvent`/`AttributeValueChangeEvent`/`StateChangeEvent`/`DeleteEvent`) and say explicitly that no stronger precedent was available.

## Step 2 — Identify the real resource(s) the new event needs, and the event names the API's own schema already defines

The event must be tied to an actual resource defined in a real, cached OpenAPI schema — either this component's own `coreFunction.exposedAPIs`, or the dependent API whose event this actually is. Read the schema directly:

```
${CLAUDE_PLUGIN_ROOT}/knowledge/apis/{TMFxxx}/{TMFxxx}_v{version}.json  →  definitions / paths
```

Cite the exact resource name as it appears in the schema (e.g. `productOffering`, not a paraphrase). If the resource the design needs doesn't exist in any cached schema for this component's APIs, stop and say so — this skill drafts event definitions for real resources, it doesn't invent the underlying resource too (that's a schema-level gap outside this skill's remit; check `${CLAUDE_PLUGIN_ROOT}/knowledge/index/gaps-backlog.md` or hand off to `propose-component-or-api-extension` if the API itself needs the new resource).

**Before drafting anything, check whether another component already has an `eventNotification` entry for this exact API id** (`grep` every `component.yaml` for the target API's id under `eventNotification`) — a component that depends on the same API as a `subscribedEvents` entry will already carry the identical, already-cached `resources` list. When one exists, that's a stronger source than re-deriving from the schema: reuse its `resources`/`specification` values directly (adjusting only the publisher-vs-subscriber-specific fields — `hub` instead of `callback`, an `implementation` path shaped for this component) rather than independently re-deriving the same list. Confirmed on a real pilot case: `TMFC002`'s cached `subscribedEvents` entry for `TMF716` carried the exact same 8-event `resources` list `TMF716`'s own schema `/listener/` paths independently implied — the two sources agreed, which is exactly the cross-check this step is for.

**Check the schema's own `paths` for a `/listener/{eventName}` entry before inferring an event name from convention.** Many TM Forum API schemas already declare their own canonical event names this way — e.g. `TMF716`'s schema lists `/listener/resourceReservationCreateEvent`, `/listener/resourceReservationAttributeValueChangeEvent`, `/listener/resourceReservationDeleteEvent`, `/listener/resourceReservationStateChangeEvent`, and `/listener/resourceReservationInformationRequiredEvent` directly. When these exist, they're the authoritative event names for that resource — use them verbatim in the drafted `resources` list rather than deriving a name from the sibling-convention heuristic below, which is a fallback for when the schema doesn't already spell this out.

## Step 3 — Draft the event entry

Produce one `eventNotification.publishedEvents` (or `subscribedEvents`) entry in exactly the shape Step 1 established, with:

- `id`/`name`/`specification`/`apiType` copied from the real cached API's own envelope (`${CLAUDE_PLUGIN_ROOT}/knowledge/index/apis.json`), never invented.
- `resources` limited to the specific lifecycle events the design actually needs — don't pad the list with every possible event type "for completeness" if the design only calls for, say, a state-change notification.
- `hub`/`implementation` paths following the `{{.Release.Name}}`/`{{.Values...}}` Helm-templated convention every cached component already uses — copy the existing pattern's literal structure, substituting only the component/API/resource-specific segments.

## Step 4 — State what's new vs. what already exists

If the target component already has *an* `eventNotification` entry for this API but is missing one specific resource-event, show only the addition (the new `resources` array entry), not a full re-draft of the existing entry. If this is a wholly new API's first event entry, show the complete new entry.

## Output format

The drafted YAML fragment (Step 3), formatted exactly as it would appear inserted into `component.yaml`'s `spec.eventNotification` block, plus a short note: which real resource/API it's grounded in (Step 2's citation), which existing component's `eventNotification` style it followed (Step 1), and whether this is a new entry or an addition to an existing one (Step 4).

## What this skill does NOT do

- Does not invent an event type, resource name, or API id — every one must trace to a real cached schema or an existing `eventNotification` entry somewhere in the corpus.
- Does not draft an event for a resource that doesn't exist in any cached OpenAPI schema — that's a schema gap, not an event-design task; flag it and stop (Step 2).
- Does not impose one universal naming convention across the whole corpus — Step 1's own instruction is to match the target component's existing style, since the real corpus doesn't have just one.
- Does not modify `component.yaml` itself — produces a drafted fragment for a human (or a follow-on skill) to apply, the same read-only posture as `draft-architecture-diagram-from-usecase` and `validate-design-against-oda`.
