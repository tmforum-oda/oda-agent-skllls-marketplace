# poq-response-profile-first-structure-diagram.png

**Type:** Payload-structure mind-map (a tree illustrating the shape of
an example API response message), not an entity-relationship data
model.
**Source context:** `# Sequence diagrams` / `### ProductOfferingQualification
for Initial Provide`, illustrating a POQ response listing WB Bitstream
Profile offerings first, each with its dependent WB Access options —
the worked example for the "1Gbps download/500Mbps upload... 500Mbps...
100Mbps..." natural-language response described in the surrounding
text.

Tree: `POQ` → `qualifiedPOItem` → three numbered items:

1. `PO: 1Gbps (WB Bitstream Profile)` with an `itemRelationship` →
   `qualifiedPOItem` → item 1 `PO: XGS-PON (WB Access)`, itself
   branching into `serviceAddress` and `accessNode`.
2. `PO: 500Mbps (WB Bitstream Profile)` with an `itemRelationship` →
   `qualifiedPOItem` → item 1 `PO: XGS-PON (WB Access)`.
3. `PO: 100Mbps (WB Bitstream Profile)` with an `itemRelationship` →
   `qualifiedPOItem` branching into two options: `PO: XGS-PON (WB
   Access)` and `PO: VDSL (WB Access)`.
