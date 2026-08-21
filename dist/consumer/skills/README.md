# tm-forum-oda-consumer

TM Forum ODA use cases, components, and Open APIs as a provenance-tracked knowledge base, queryable via Agent Skills -- for building software against ODA.

This plugin bundles 9 Agent Skills. Your agent invokes one automatically when your request matches what it does -- you don't need to name the skill directly, just describe what you want.

## Skills

### assess-change-impact

Given a TM Forum ODA component (TMFCxxx) or Open API (TMFxxx) id and a proposed change (deprecation, breaking version bump, removal), lists every TMFSxxx use case that depends on it, describes specifically how each one uses it, and drafts a maturity-weighted migration/impact report. Use this before deprecating, breaking, or removing a component or API.

**Example:**
> We're deprecating TMF632 v4.0.0 -- which use cases break, and how badly?

### audit-implementation-against-usecase

Given a TMFSxxx use-case id and an existing implementation (codebase, API contract, or integration config), checks whether the implementation actually follows the use case's described flow and calls the right real APIs, flagging drift from spec. Use this to audit an existing system against ODA, not to design a new one.

**Example:**
> Does our current order-capture service actually implement TMFS030 the way the use case describes?

### capture-requirements-from-usecase

Given a TMFSxxx use-case id, reads its Description/Scope/Objective sections and drafts user stories and acceptance criteria, citing the exact component/API ids from frontmatter for any integration touchpoint rather than inventing them. Use this to turn an existing use case into requirements a delivery team can work from.

**Example:**
> Turn TMFS030 into user stories and acceptance criteria for the delivery team.

### check-usecase-maturity

Given a TM Forum ODA use-case id (TMFSxxx), reads its cached frontmatter and returns a plain-language maturity/trust verdict -- whether it's safe to build against today. Reads only YAML frontmatter, no document-body parsing. Use this before starting requirements or test-case work against any TMFSxxx use case.

**Example:**
> Is TMFS030 safe to build against right now?

### draft-architecture-diagram-from-usecase

Given a TMFSxxx use-case id, reads its sequence-diagram images and linked component/API frontmatter, and emits a Mermaid sequence or architecture diagram as a design-doc-ready artifact, citing only real component/API ids. Use this when asked for an architecture diagram, sequence diagram, or component interaction diagram for a use case.

**Example:**
> Draw a sequence diagram for TMFS030's wholesale ordering flow.

### generate-api-mocks-from-usecase

Given a TMFSxxx use-case id, uses its linked APIs' cached OpenAPI schemas and real sample payloads to scaffold a mock server or example request/response fixtures for integration testing before a real backend exists. Use this when asked for API mocks, stub responses, or test fixtures for a use case's dependencies.

**Example:**
> Scaffold mock API responses for TMFS030's dependencies so we can start integration testing before the real backend exists.

### generate-test-cases-from-usecase

Given a TM Forum ODA use-case id (TMFSxxx), reads its sequence-diagram section and linked component/API frontmatter, then drafts BDD-style (Gherkin) test scenarios grounded in the real component/API IDs and cached OpenAPI schemas in ${CLAUDE_PLUGIN_ROOT}/knowledge/apis/ -- never invented ones. Mirrors oda-canvas's write-bdd-feature Gherkin conventions, pointed at real use-case content instead of hand-written scenarios. Use this when asked to generate test cases, BDD scenarios, or acceptance tests for a TMFSxxx use case.

**Example:**
> Generate Gherkin/BDD test scenarios for TMFS030.

### recommend-oda-components-for-requirement

Given a plain-language business requirement (not yet a TMFSxxx id), finds the closest-matching existing use case(s) by name and component/API overlap, and proposes a starting architecture grounded in real component/API ids -- never invented ones. Use this at the start of a design, before a requirement has been mapped to a specific ODA use case.

**Example:**
> We need to let customers manage their own SIM swaps online -- what ODA components and APIs should this be built on?

### validate-design-against-oda

Given a proposed component or API design that claims to extend or depend on existing ODA components/APIs, checks those claims against the real cached specs and flags drift -- fields, operations, or behavior the design assumes exist but don't. Use this before building against an assumed ODA capability, to confirm the assumption is real.

**Example:**
> Check whether our design's assumption that Party Management (TMF632) exposes a loyaltyPoints field actually holds.
