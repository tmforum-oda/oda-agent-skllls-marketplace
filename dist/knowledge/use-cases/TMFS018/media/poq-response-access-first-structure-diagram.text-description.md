# poq-response-access-first-structure-diagram.png

**Type:** Payload-structure mind-map (a tree illustrating the shape of
an example API response message), not an entity-relationship data
model.
**Source context:** `# Sequence diagrams` / `### ProductOfferingQualification
for Initial Provide`, the same worked example as
`poq-response-profile-first-structure-diagram.png` but restructured to
list WB Access offerings first, each with its dependent WB Bitstream
Profile options.

Tree: `POQ` → `qualifiedPOItem` → two numbered items:

1. `PO: XGS-PON (WB Access)` with a `place` branch (`role:
   serviceAddress`, `role: accessNode`) and an `itemRelationship` →
   `qualifiedPOItem` → three profile options: `PO: 1Gbps (WB Bitstream
   Profile)`, `PO: 500Mbps (WB Bitstream Profile)`, `PO: 100Mbps (Wb
   Bitstream Profile)`.
2. `PO: VDSL-35b (WB Access)` with the same `place` structure and an
   `itemRelationship` → `qualifiedPOItem` → two profile options: `PO:
   300Mbps (WB Bitstream Profile)`, `PO: 100Mbps (WB Bitstream
   Profile)`.
