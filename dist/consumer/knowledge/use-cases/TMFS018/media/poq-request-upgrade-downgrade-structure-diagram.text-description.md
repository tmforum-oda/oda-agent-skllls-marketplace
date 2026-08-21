# poq-request-upgrade-downgrade-structure-diagram.png

**Type:** Payload-structure mind-map (a tree illustrating the shape of
an example API request message), not an entity-relationship data model.
**Source context:** `## Operational Stage: Upgrade/Downgrade` / `###
ProductOfferingQualification for Upgrade/Downgrade`, illustrating the
POQ request used to qualify upgrade/downgrade offerings against an
existing product.

Tree: `POQ` → `searchCriteria` → `P` (a repeatable/polymorphic field
node) with `id: 1234` — referencing the existing product id the
upgrade/downgrade qualification is being requested against.
