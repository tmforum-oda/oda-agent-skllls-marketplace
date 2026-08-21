# poq-response-access-profiles-transports-structure-diagram.png

**Type:** Payload-structure mind-map (a large tree illustrating the
shape of an example API response message), not an entity-relationship
data model.
**Source context:** `# Sequence diagrams` / `### ProductOfferingQualification
for Initial Provide`, extending the worked example with WB Bitstream
Transport options and their selectable (non-purchasable) supporting
ENNI resources, illustrating "information about specific ENNI resources
that the Seller can present as selectable options".

Tree: `POQ` → `qualifiedPOItem` → seven numbered items:

1. `PO: FTTH (WB Access)`, with a `place` branch (`role:
   serviceAddress`, `role: accessNode`) and an `itemRelationship` →
   `qualifiedPOItem` → five items: three WB Bitstream Profile options
   (1Gbps/500Mbps, 500Mbps/200Mbps, 100Mbps/30Mbps) plus two WB
   Bitstream Transport options (`Local Network`, `National Network`).
2. `PO: Local Network (WB Bitstream Transport)`, with a
   `supportingResource` branch listing three selectable `Resource`
   entries (ENNI-QQ/QQ-RR-200, ENNI-QQ1/QQ-RR-300, ENNI-QQ2/QQ-RR-400,
   each `Type: ENNI` with a "Local ENNI N" description), and an
   `itemRelationship` back to `PO: FTTH (WB Access)`.
3. `PO: National Network (WB Bitstream Transport)`, structured
   identically to item 2 but with "National ENNI N" descriptions for
   its three supporting ENNI resources.
4-7. The three WB Bitstream Profile options plus a fourth "100Mbps
   Download / 30Mbps Upload" variant, each with its own
   `itemRelationship` back to `PO: FTTH (WB Access)`.
