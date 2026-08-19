---
name: generate-test-cases-from-usecase
description: Given a TM Forum ODA use-case id (TMFSxxx), reads its sequence-diagram section and linked component/API frontmatter, then drafts BDD-style (Gherkin) test scenarios grounded in the real component/API IDs and cached OpenAPI schemas in knowledge/apis/ -- never invented ones. Mirrors oda-canvas's write-bdd-feature Gherkin conventions, pointed at real use-case content instead of hand-written scenarios. Use this when asked to generate test cases, BDD scenarios, or acceptance tests for a TMFSxxx use case.
---

# Generate Test Cases from Use Case — Skill Instructions

## What this skill produces

BDD-style Gherkin scenarios for a TMFSxxx use case's interaction flow,
citing the real ODA component and Open API IDs the use case actually
depends on — never a plausible-sounding invented one. This is the check
this skill is validated against (spec.md §9's last success criterion):
every `TMFCxxx`/`TMFxxx` id in the output must trace back to something
actually present in the source use case's own frontmatter or a cached API
schema, not something that merely sounds right for the scenario.

This mirrors `oda-canvas`'s `write-bdd-feature` skill's Gherkin
conventions (tags, `Given`/`When`/`Then` structure, Scenario Outline +
Examples table), adapted to this repo's own id scheme — TM Forum's
`TMFSxxx` use-case numbering, not `oda-canvas`'s internal `UC{number}`
scheme, which is a different, unrelated numbering system for that repo's
own Canvas-lifecycle test suite. Don't borrow `UC{number}` literally.

## Step 0 — Check maturity first

Run `check-usecase-maturity` (this repo's other pilot skill) against the id
before drafting anything. Include its verdict at the top of the output
(e.g. "Source: TMFS030, Beta / Member Evaluated — scenarios below are
provisional and should be re-validated once this use case reaches GA").
Don't silently draft test cases against an Alpha/Beta use case as if it
were settled — the reader needs that caveat to weigh how much to invest in
the tests you're about to hand them.

## Step 1 — Read the use case body, not just frontmatter

```
knowledge/use-cases/{ID}/{ID}.md
```

Read the `# Description` and `# Sequence diagrams` sections (heading
wording varies slightly across documents — look for both). **Found while
building this skill, worth knowing up front**: the actual interaction
steps usually live in embedded diagram images, not in text. `docx2md.py`
extracts each document's original diagrams as real image files under
`knowledge/use-cases/{ID}/media/imageNN.png` (or `.jpeg`), referenced
inline as `![](media/imageNN.png)`. Don't treat these as decorative and
skip past them — **read every image a Sequence Diagrams section
references** (the Read tool handles images directly) to see the actual
actor/step flow; the surrounding prose is often only a partial gloss on
what the diagram shows, and sometimes (TMFS002, TMFS030) the only real
step breakdown is the sequence of `## Step N: ...` subheadings each
paired with one diagram.

Document shapes vary — don't assume one pattern:
- Prose-narrated with inline diagrams per step (TMFS001, TMFS002, TMFS030).
- Single diagram plus one summary paragraph naming the APIs involved by
  name, not ID (TMFS031) — you'll need Step 2 below to resolve these.
- A tabular scenario/outcome matrix instead of a sequence diagram at all
  (TMFS009's balance-management scenarios table) — when this is what a
  document actually has, draft scenarios from the table's rows directly;
  don't force a diagram-reading step that doesn't apply.

## Step 2 — Resolve every name to a real ID via frontmatter, never guess

The use case's own frontmatter is the authoritative id list:

```yaml
links:
  components:
    - id: TMFC020
      name: Digital Identity Management
  apis:
    - id: TMF632
      name: Party Management v4
```

Body prose frequently names a capability without its id ("Party
Interaction Management APIs", "the Product Catalog") — match it against
`links.components`/`links.apis` by name to get the real id. **If a
capability named in the body has no matching entry in frontmatter, say so
explicitly in the output rather than inventing a plausible `TMFCxxx`/
`TMFxxx` id for it** — this is the single most important rule this whole
skill exists to enforce (spec.md §9, §8's design principle 5, "links are
data, not prose"). A wrong-but-plausible id is worse than an honest gap.

Two gotchas found while validating this skill against TMFS020, worth
knowing before you hit them yourself:

- **Frontmatter isn't exhaustive of a document's own real ids.**
  `docx2md.py` only extracts `links.components`/`links.apis` from a
  document's dedicated References section (task 4.2). TMFS020's own body
  text, under "Main ODA Components involved in this process" beneath its
  Sequence Diagrams heading, names `TMFC001`, `TMFC002`, and `TMFC023` in
  plain text — real, correctly-formed TM Forum ids that never made it into
  this document's own frontmatter. These are NOT invented and are fine to
  cite — they're the source document's own words — but cite them with a
  "body text, not frontmatter" source note (e.g. "`TMFC001` — named in
  this document's own Sequence Diagrams section, not in its frontmatter
  links"), so the reader can tell the difference between an id backed by
  the structured envelope and one only backed by body prose.
- **`TMFCxxx` with a literal `???` instead of digits is the source
  document's own explicit placeholder, not a redacted real id.** The same
  TMFS020 section contains `TMFC??? ProductOffering Qualification / TMFC???
  Resource Qualification (tbc)` and `TMFC??? Party Request Management` —
  TM Forum's own authors marking "no component id assigned yet." Never
  resolve a `???` placeholder to a real id by guessing which existing
  `TMFCxxx` it probably means. If it's worth mentioning in the output at
  all, cite it verbatim as "not yet assigned (`TMFC???` in source)," not as
  a numbered id.

Also check `knowledge/index/usecase-component-matrix.json` for the same
id and cross-reference against `knowledge/index/matrix-discrepancies.md`
— if the use case you're drafting against is one of the flagged
disagreements, note that in the output too (e.g. "TMFC050 appears in
IG1228's matrix for this use case but not in the document's own
References section — included here on the matrix's authority, flagged as
matrix-only per `matrix-discrepancies.md`").

## Step 3 — Ground steps in the real API schema, not invented endpoints

For each resolved API id + version, read the cached schema:

```
knowledge/apis/{TMFxxx}/{TMFxxx}_v{version}.json
```

It's a Swagger/OpenAPI document — `paths` gives real resource paths
(`/individual`, `/individual/{id}`) and each operation's real
`operationId` (`listIndividual`, `createIndividual`, ...). Use these —
not invented endpoint names — when a Gherkin step needs to reference a
specific call. If the id's status in `knowledge/index/apis.json` is
`not_yet_specified` or `fetch_failed`, say so in the output instead of
drafting a step against a schema that doesn't exist; a `Given`/`When`
step can still describe the *intent* in plain language, just without
citing a concrete path/operation that isn't actually cached.

## Feature file conventions

Adapted from `oda-canvas`'s `write-bdd-feature` (same shape, this repo's
own id scheme):

```gherkin
# Generated from knowledge/use-cases/{ID}/{ID}.md ({maturity} / {approval_status})
# Component/API ids cited below are taken from this use case's own frontmatter
# links and/or knowledge/index/usecase-component-matrix.json -- see Sources.

@{ID}
@{ID}-F{feature-number}
Feature: {ID}-F{feature-number} {Feature Title}

    Background:
        Given [shared preconditions, if any]

    Scenario Outline: {Descriptive scenario name}
        Given [initial context, citing the real component/API by id+name]
        When [the action, citing the real API operation if one is grounded in Step 3]
        Then [expected outcome]

    Examples:
      | Name        | ...
      | Descriptive | ...
```

- File naming: `{ID}-F{feature-number}-{Descriptive-Title}.feature`
  (e.g. `TMFS030-F001-Request-Wholesale-Capacity-Quote.feature`).
- Two tags, same as `write-bdd-feature`: `@{ID}` (use-case level) and
  `@{ID}-F{feature-number}` (feature level).
- Prefer `Scenario Outline` + `Examples` over repeated individual
  `Scenario` blocks when the same flow varies only by data, matching
  `write-bdd-feature`'s stated preference.
- This repo has no `feature-definition-and-test-kit`-style directory of
  its own (that's an `oda-canvas`-specific test harness) — **don't write
  the `.feature` file into `knowledge/`**, which is generated,
  regeneratable output per spec.md principle 3. Return the feature file
  content to the caller; where they save it is their decision, not this
  skill's.

## Sources footer — required on every output

End every generated feature file with a citation block, since this is
exactly what task 6.3 checks:

```gherkin
# Sources:
#   TMFC020 Digital Identity Management -- knowledge/use-cases/{ID}/{ID}.md links.components
#   TMF632 Party Management v4.0.0      -- knowledge/apis/TMF632/TMF632_v4.0.0.json
#   TMFC050 -- knowledge/index/usecase-component-matrix.json only (not in this document's own References section; see matrix-discrepancies.md)
```

Every id that appears in a `Given`/`When`/`Then` step must have a matching
line here. If you can't cite where an id came from, it doesn't belong in
the scenario — go back to Step 2.

## What this skill does NOT do

- Does not invent component/API ids, endpoint paths, or operation names
  that aren't present in the source use case's own frontmatter, the
  matrix, or a cached schema (Step 2/3 above — this is the whole point).
- Does not assume `oda-canvas`-specific step vocabulary (`Given a running
  helm release`, Kubernetes/Helm lifecycle steps) unless the use case is
  actually about ODA component deployment lifecycle — most TMFSxxx use
  cases are business-process flows (order capture, party management,
  fault resolution), not component installation, and forcing Canvas
  test-kit phrasing onto a business scenario would misrepresent what's
  being tested.
- Does not write output files into this repository — `knowledge/` is
  skills-read-only generated content (spec.md principle 3); this skill's
  output is a deliverable for the caller to place wherever their own test
  suite lives.
- Does not skip Step 0 — a maturity caveat belongs on every output, not
  just GA ones.
