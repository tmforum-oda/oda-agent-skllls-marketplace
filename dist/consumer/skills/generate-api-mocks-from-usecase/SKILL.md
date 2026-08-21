---
name: generate-api-mocks-from-usecase
description: Given a TMFSxxx use-case id, uses its linked APIs' cached OpenAPI schemas and real sample payloads to scaffold a mock server or example request/response fixtures for integration testing before a real backend exists. Use this when asked for API mocks, stub responses, or test fixtures for a use case's dependencies.
---

# Generate API Mocks from Use Case — Skill Instructions

## What this skill produces

Mock responses / fixture files for the real APIs a use case depends on,
grounded in the cached OpenAPI schema and (where available) real sample
payloads TM Forum's own API authors wrote — not invented JSON shaped to
look plausible.

## Step 1 — Resolve the use case's real API list

Read `links.apis` from `${CLAUDE_PLUGIN_ROOT}/knowledge/use-cases/{ID}/{ID}.md`'s frontmatter.
Each entry gives an id and name; check `${CLAUDE_PLUGIN_ROOT}/knowledge/index/apis.json` for
its cached version and `status`. An id with `status: "not_yet_specified"`
or `fetch_failed` has no real schema to mock from — say so, don't
fabricate a plausible-looking schema for it.

## Step 2 — Use the cached schema for shape, real samples for content

```
${CLAUDE_PLUGIN_ROOT}/knowledge/apis/{TMFxxx}/{TMFxxx}_v{version}.json       -- the OpenAPI/Swagger schema
${CLAUDE_PLUGIN_ROOT}/knowledge/apis/{TMFxxx}/samples/                        -- real example payloads, if fetched
```

Not every API has a `samples/` directory — it's optional, best-effort
enrichment (fetched from a separate, private TM Forum GitHub org repo),
so its absence isn't an error, just means Step 2 has less to work with
for that particular API.

When samples exist, prefer them over hand-building a payload from the
schema alone — they're real, human-authored examples TM Forum wrote for
conformance testing. Note what a sample actually is before using it: some
files under `samples/` are plain request/response bodies for a specific
operation, others are event-notification payloads (e.g.
`*CreateEvent`/`*AttributeValueChangeEvent`, wrapping the resource inside
an `event` envelope with `eventType`/`eventTime`/etc.) — don't use an
event-notification sample as if it were a plain resource response, the
shapes are different.

When no sample exists for an operation, build a minimal valid example
directly from the schema's `paths`/`definitions` — real property names
and types from the schema, not invented field names. State clearly which
of the two sources (real sample vs. schema-derived) each mock came from.

## Step 3 — Scaffold, don't over-build

Output request/response fixture files per operation actually used by the
use case (grounded in Step 1's schema paths, or the operations
`generate-test-cases-from-usecase` would cite for this same use case, if
that's already been run) — not every operation the API happens to
expose. A use case that only calls `POST /individual` and
`GET /individual/{id}` doesn't need mocks for every other Party
Management endpoint.

## Output format

One fixture per operation: the real path + method, the real
`operationId`, and the payload (marked as `sample-sourced` or
`schema-derived` per Step 2). If scaffolding an actual mock server
(rather than static fixtures), keep the server as thin as possible —
route matching plus returning the fixture — not a reimplementation of
the API's business logic.

## What this skill does NOT do

- Does not invent field names, resource shapes, or endpoints not present in the cached schema — a mock that doesn't match the real contract is worse than no mock.
- Does not treat an event-notification sample as a plain response body, or vice versa — the envelope shapes differ and mixing them produces a mock that doesn't match how the real API actually behaves.
- Does not attempt to mock an API with `status: not_yet_specified`/`fetch_failed` — report the gap instead of fabricating a schema to mock against.
