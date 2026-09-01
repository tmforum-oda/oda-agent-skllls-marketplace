---
name: generate-api-conformance-tests
description: Given a TMFxxx id and version, generates conformance test assertions directly from its cached OpenAPI schema -- required-field presence, enum-value validity, declared operations per path, and expected status codes -- using real sample payloads as fixtures where they exist and pass/fail. If a real implementation (a base URL or example request/response pairs) is supplied, also reports pass/fail per assertion; without one, produces a standalone suite ready to run once an implementation exists. Use this to check or generate conformance tests for one specific TM Forum Open API, not a whole use case's flow (see generate-test-cases-from-usecase for that).
---

# Generate API Conformance Tests — Skill Instructions

## What this skill answers

"Does (or will) our implementation of TMFxxx actually conform to what the real schema says?" API-contract-level, not use-case-flow-level — the same family as `generate-test-cases-from-usecase`/`generate-api-mocks-from-usecase`, but scoped to one API's schema instead of a use case's end-to-end narrative.

## Step 1 — Resolve the API and check it's real

Look up the id+version in `knowledge/index/apis.json`. A `status` other than a real fetched version (`not_yet_specified`, `fetch_failed`, or absent) means there's no real schema to test against — say so and stop, don't test against an assumed shape. If no version is given and more than one is cached for this id, ask which, or generate a suite per version rather than silently picking one.

## Step 2 — Extract assertions directly from the schema

Read `knowledge/apis/{TMFxxx}/{TMFxxx}_v{version}.json` (`definitions`, or `components.schemas` for OpenAPI 3-shaped files). For each resource relevant to the conformance check:

- **Required-field presence**: the schema's own `required` array, if present. Many TM Forum resources have no `required` array at all on the full resource type but do on its `_Create` variant (e.g. `Category` itself declares nothing required, `Category_Create` requires `name`) — check both, and don't report a false "no required fields" finding for the full type when the real constraint lives on the `_Create`/`_Update` variant instead.
- **Enum-value validity**: any property with a schema `enum` list. **Not every TM Forum API schema uses JSON-schema `enum` constraints for status-like fields** — some type them as a plain `string` with the allowed values only described in prose (confirmed: `TMF620`'s `Category.lifecycleStatus` has no `enum` in the schema despite behaving like one in practice). A resource with zero real `enum` fields produces zero enum assertions — that's a correct, honest result, not a sign to search harder or invent a constraint the schema doesn't actually declare.
- **Declared operations per path**: every path+method the schema's `paths` defines.
- **Expected status codes**: each operation's own `responses` keys (e.g. `200`/`201`/`204`/`400`).

## Step 3 — Select fixtures, validating every sample before trusting it

Prefer a real fixture from `knowledge/apis/{TMFxxx}/samples/` over a schema-derived generic one. **Before using any sample, check its field names against the schema's own properties for the resource it claims to represent — do not cite or use a sample on trust.** Confirmed as a real, recurring risk, not a hypothetical: `TMF679`'s cached schema is `v4.0.0`, but every file under its `samples/` is v5-shaped, with field names the v4 schema doesn't define (`generate-implementation-scaffold-from-usecase`'s own `SKILL.md` documents the full finding). A sample whose fields don't match the schema is not a usable fixture — fall back to a schema-derived generic value (correct types, satisfying `required`/`enum` constraints) and say explicitly that the real sample was rejected for a version mismatch, not silently swap it in anyway or silently drop it with no explanation.

Confirmed working, contrasting case: `TMF620`'s `Category_create_1_request.sample.json` — every field name in the sample matches `Category`'s real schema properties exactly, and it satisfies the `Category_Create` schema's `required: ["name"]` constraint. Use a sample like this directly.

## Step 4 — Generate the assertions

One test per assertion category per resource/operation, in a form the target language/framework can actually run (ask which framework if not stated, the same discipline `generate-implementation-scaffold-from-usecase` Step 1 uses for its own target-language question). Each assertion cites what it's checking and against which real schema element (`# asserts Category_Create.required includes 'name', per TMF620_v4.0.0.json`) — a reader should be able to trace every assertion back to the schema without re-reading it.

## Step 5 — Run against a real implementation, if one is supplied

If given a base URL or a set of example request/response pairs, actually check each assertion against it and report pass/fail per assertion, not a single aggregate verdict. If no implementation is supplied, the output is a standalone test suite explicitly marked "ready to run once an implementation exists" — don't fabricate a pass/fail result with nothing real to check it against.

## Output format

The generated test code, then a summary: assertions generated per category (required-field / enum / operation-coverage / status-code) per resource, which samples were used as fixtures vs. rejected as version-mismatched vs. fell back to schema-derived generic values, and — if an implementation was supplied — the pass/fail count per category.

## What this skill does NOT do

- Does not test business/semantic correctness beyond what the schema itself defines — a field being present and correctly typed is not the same as the implementation's business logic being correct, and this skill only checks the former.
- Does not invent a required field, enum value, or status code the schema doesn't declare — an API with no `enum`-constrained fields produces zero enum assertions, not a fabricated one.
- Does not use a sample payload without checking it against the schema first — a version-mismatched sample is worse than no sample (Step 3).
- Does not fabricate a pass/fail verdict when no real implementation was supplied — an unimplemented suite is reported as exactly that.
- Does not test a whole use case's end-to-end flow — that's `generate-test-cases-from-usecase`; this skill is scoped to one API's own contract.
