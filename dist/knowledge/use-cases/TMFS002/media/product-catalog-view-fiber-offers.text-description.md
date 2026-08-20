# product-catalog-view-fiber-offers.png

**Type:** Information/catalog data model diagram, not a sequence diagram.
**Source context:** `# Information View` section — "PRODUCT CATALOG
View," illustrating the bullet points immediately above it about how a
single Product Specification can be commercialized through several
Product Offerings.

An entity-relationship diagram of three example `ProductOffering`
records under a shared structure:

- A `B2C Market Segment` (magenta) targets offerings sold through `All
  Sales Channels` (purple): **Fiber Contract Silver**, **Fiber Contract
  Gold**, and **Fiber + Mobile Contract** — each with its own welcome
  discount (-5€/-7€/-10€ per month for the first 10 months) shown as a
  blue `POPrice` box.
- Each contract *packages* one or more `Product Specification` entries
  (green), with min/max cardinality (`Min:1, Max:1`) — the Silver and
  Gold contracts package **Fiber Access Standard** (with
  speed-dependent pricing: 10€/month basic, 15€/month high) and/or
  **Fiber Access High Capacity** (17€/month flat), alongside placeholder
  "other offers (not described)" boxes for offerings out of scope for
  this diagram.
- Both Fiber Access product specs *commercialize* a shared **Fiber
  Access** resource, linked to a `Geo Address` entity and characterized
  by a `Speed` characteristic (values: Basic, High) that *determines
  productspec charvalue*.
- The Fiber Access resource *restricts* an orange **Fiber Access CFS
  spec** (`CFS specification`), marked "Technical Eligibility Test:
  Mandatory" — the data-model basis for the eligibility check performed
  in the use case's Step 3 sequence diagram
  (`fiber-eligibility-test-sequence.puml`).

A legend (top right) maps box colors/outlines to entity types: Product
Offering, Product Specification (with nested Characteristic/
Characteristic value), MarketSegment, SalesChannel, CFS specification.
