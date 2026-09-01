---
name: generate-implementation-scaffold-from-usecase
description: Given a TMFSxxx use-case id (or an explicit component/API set from recommend-oda-components-for-requirement/decompose-requirement-against-oda), generates typed request/response models and route/handler stubs directly from its linked APIs' cached OpenAPI schemas, in a language of the caller's choosing -- with a TODO marker at every point real domain logic belongs. Also handles the case where a non-ODA legacy interface needs an anti-corruption adapter layer into the chosen ODA contract. Use this when a design needs implementation scaffolding, not implemented business logic, and does not want TM Forum's own opinionated Node.js/Helm reference stack (see implement-oda-component for that alternative).
---

# Generate Implementation Scaffold From Use Case — Skill Instructions

## What this skill answers

"We've settled on which ODA APIs to build against — generate the boilerplate so a developer starts from typed models and route stubs, not a blank file." A Build-stage skill, and a narrow one by design: it scaffolds the *shape* a cached OpenAPI schema defines, it does not write what the implementation should actually do.

**This is not `implement-oda-component` (a different, coexisting skill).** That one generates TM Forum's own complete, opinionated Node.js/Helm reference implementation for a whole Component and can build/push/deploy it — real side effects, one specific stack. This skill is lightweight, language-agnostic, and has none: no build, no push, no deploy, and no opinion about the target language beyond what the caller states. Ask which one is wanted if it isn't obvious from context; don't default to this one just because it has no side effects.

## Step 1 — Resolve the target APIs and the target language

**APIs**: if given a `TMFSxxx` id, read its `links.apis` frontmatter (`${CLAUDE_PLUGIN_ROOT}/knowledge/use-cases/{ID}/{ID}.md`) for the real API ids to scaffold. If given an explicit component/API set instead (e.g. `recommend-oda-components-for-requirement`'s proposed architecture, or `decompose-requirement-against-oda`'s `candidate_apis`), use that list directly — don't re-derive it from a use case that wasn't given.

For each api id, check `${CLAUDE_PLUGIN_ROOT}/knowledge/index/apis.json`: a `status` other than a real fetched version (`not_yet_specified`, `fetch_failed`, or simply absent from the index) means there's no real schema to scaffold from — flag that api explicitly and skip it, don't fabricate a schema shape to fill the gap.

**Language**: ask which target language/framework to scaffold in if it isn't already stated or obvious from surrounding codebase context (an existing `package.json`, `pom.xml`, `go.mod`, etc. in the working directory is a reasonable signal to infer from — a bare, unstated request is not). Never silently default to one language; this skill's whole value is being usable regardless of stack.

## Step 2 — Generate typed models from each API's real schema

Read `${CLAUDE_PLUGIN_ROOT}/knowledge/apis/{TMFxxx}/{TMFxxx}_v{version}.json` directly (`definitions`, or `components.schemas` for OpenAPI 3-shaped files — check which the specific cached file uses, both exist across this corpus). For each resource the use case/candidate set actually touches (not necessarily every resource the whole API defines — scope to what's relevant), generate one typed model per schema object, with every field name and type copied exactly as the schema defines it. **A resource's `_Create` and `_Update` variants are two separate schema objects, not one** — confirmed on `TMF679`: `ProductOfferingQualification_Create` and `ProductOfferingQualification_Update` exist independently, each with its own distinct field set (e.g. `_Update` includes `state`/`qualificationResult`, fields that make sense to change after creation but not to set at creation, so `_Create` omits them). Generate a model per variant that actually appears in the schema's own `paths` (the POST body's `$ref` for `_Create`, the PATCH body's `$ref` for `_Update`) — don't assume one variant can stand in for the other, and don't skip generating one just because it looks similar to the full-resource type or to its sibling variant.

Cite the exact schema object name in a comment above each generated model (`// from TMF679's ProductOfferingQualification`) so a reader can trace it back without re-reading the schema themselves.

**Bounded rule for `$ref` fields, confirmed against a real schema, not arbitrary**: expand every `$ref` a top-level resource directly references into its own fully-typed model, one level deep — TM Forum's common `{Name}Ref` pattern (`id`/`href`/`name`/`@type`/...) is almost always a small, flat shape, and typing it properly costs little (confirmed on `TMF679`'s own `CategoryRef`/`ChannelRef`/`RelatedParty` — all flat). Do **not** recurse a second level: if that referenced type itself references further complex sub-types (confirmed on the same schema's `ProductOfferingQualificationItem`, which references seven more schemas including arrays of further objects), stop there and type the field as an untyped placeholder (`dict`/`Any`/the target language's nearest equivalent) with a comment citing the unexpanded schema's real name — don't silently flatten it to `Any` with no trace of what it actually is, and don't keep recursing until the whole schema graph is expanded (unbounded scope creep for a scaffolding skill).

## Step 3 — Generate route/handler stubs from each API's real paths

For each path+method the schema defines that's actually relevant to the use case's flow, generate one handler stub: correct method, correct path, request body typed to the Step 2 model the schema's own path definition specifies, response typed to the model its own success response defines. Where real sample payloads exist (`${CLAUDE_PLUGIN_ROOT}/knowledge/apis/{TMFxxx}/samples/`), reference one as an example in the stub's docstring/comment — never invent a plausible-looking example when a real one is cached.

**A cached sample is not guaranteed to match the cached schema's own version or field names — validate before citing it, don't cite on trust.** Confirmed on a real pilot case: `TMF679`'s cached schema is `v4.0.0` (`TMF679_v4.0.0.meta.json`), but its `samples/` payloads carry `href` values pointing at `.../v5/...` and use v5-generation subclassed `@type`s (`CheckProductOfferingQualification`, `EligibilityResultReason`) with field names the v4 schema doesn't define at all (`expectedQualificationCompletionDate` vs. the schema's `expectedPOQCompletionDate`, `checkProductOfferingQualificationItem` vs. the schema's `productOfferingQualificationItem`, a `provideResultReason` field the v4 schema has no equivalent for). Parsing the sample straight into a Step 2 model built strictly from the schema silently drops every one of those mismatched fields rather than erroring — confirmed directly by validating the sample against the generated model. Before citing any sample: check that its field names actually appear in the schema you generated the model from. If they don't, say so explicitly in the stub's comment (a version-mismatched sample, not a shape reference) rather than presenting it as reliable, and prefer a schema-example value or an empty-but-correctly-typed instance instead.

**Sample filenames are named by the real-world scenario they were captured from, not always by the schema's own resource name** — confirmed on `TMF679`: its samples are prefixed `CheckProductOfferingQualification_.../QueryProductOfferingQualification_...` even though the schema itself defines one resource, `ProductOfferingQualification`. Match a sample to a handler by **operation type** (create/retrieve/list/partialupdate/delete), not by expecting the filename to echo the schema's own definition name exactly.

**A `DELETE` handler usually has no request-body sample to cite, and that's expected, not a gap** — `DELETE` carries no body. A `...DeleteEvent_request...` sample that does exist alongside it is the **event-notification payload** sent to subscribers when the deletion happens (see `draft-event-design-for-component`'s own event-shape conventions), not a sample of the delete request itself — don't cite it as one.

**Every handler body is a `TODO` marker, nothing else.** In the target language's own idiomatic comment form (`// TODO: implement {operationId}`, `# TODO: implement {operationId}`, ...), stating what the real implementation needs to do in one line drawn from the operation's own schema description — not a generic "implement this." A schema grounds the shape of a handler; it says nothing about what the business logic inside should actually do, and this skill must never imply otherwise by writing a plausible-looking fake implementation.

## Step 4 — Integration-adapter mode, when a target interface isn't itself an ODA API

If the design also needs to bridge a non-ODA, legacy, or proprietary interface into the scaffolded contract (the `oda-integration-adapter` case), generate that translation as a **separate adapter file**, never mixed into the same file as the ODA-side scaffold from Steps 2-3. Comment it explicitly as an anti-corruption boundary (`// Adapter: translates legacy {system} shape -> TMF679 ProductOfferingQualification`), mapping legacy fields to the real Step 2 model's fields one by one. The adapter's own internal translation logic (not domain logic — just shape translation) can be filled in, since that mapping is exactly what this skill is grounded to produce; the domain logic on the ODA-contract side of the boundary still gets a `TODO`, same as Step 3.

## Output format

A file tree of what was generated, then each file's content. Close with a summary: every API scaffolded (and any skipped per Step 1's cache-status check, named explicitly), how many models and how many route stubs per API, and a total count of `TODO` markers left for a human to fill in — so a reader knows exactly how much is scaffold vs. how much is still unwritten, not left to count manually.

## What this skill does NOT do

- Does not write business/domain logic — every handler body is a `TODO`, deliberately, never a plausible-looking guess at what the logic should do.
- Does not invent a field, resource, or operation not present in the cached OpenAPI schema — an API missing from the cache is flagged and skipped (Step 1), never backfilled from assumption.
- Does not choose the target language unasked — Step 1 requires either an explicit statement or a genuine codebase signal, never a silent default.
- Does not build, push, or deploy anything — no side effects at all, in contrast to `implement-oda-component`, which explicitly does.
- Does not blend adapter-layer translation code into the same file as ODA-contract scaffolding — Step 4's separation is required, not a style preference.
- Does not cite a cached sample payload as a shape example without checking it against the schema first — a sample can be a different, incompatible API version from what's actually cached (Step 3), and citing one uncritically is worse than citing none.
