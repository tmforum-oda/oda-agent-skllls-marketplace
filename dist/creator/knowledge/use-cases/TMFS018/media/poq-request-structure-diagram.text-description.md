# poq-request-structure-diagram.png

**Type:** Payload-structure mind-map (a tree illustrating the shape of
an example API request message), not an entity-relationship data model.
**Source context:** `# Sequence diagrams` / `### ProductOfferingQualification
for Initial Provide`, directly under "POQ Request", illustrating the
proposed structure of a Product Offering Qualification (POQ) request
message.

Tree: `POQ` → `agreement` (a sibling branch) and `searchCriteria`, which
branches (via a `P` node, "P" likely marking a repeatable/polymorphic
field) into three leaves: `category: WholesaleBroadbandProfile`,
`ProductSpecification: WholesaleBroadbandProfile or
WholesaleBroadbandAccess`, and `serviceAddress`.
