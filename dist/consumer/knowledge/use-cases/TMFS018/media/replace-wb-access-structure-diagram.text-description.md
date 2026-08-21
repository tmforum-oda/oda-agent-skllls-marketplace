# replace-wb-access-structure-diagram.png

**Type:** Payload-structure mind-map (a tree illustrating the shape of
an example ProductOrder request that replaces a WB Access technology),
not an entity-relationship data model.
**Source context:** `## Operational Stage: Upgrade/Downgrade` / `###
ProductOrder for Upgrade/Downgrade`, illustrating an access-technology
replacement (e.g. VDSL to X-GPON) that requires four coordinated order
items.

Tree: `WholesaleAgreement` → `ProductOrder, newBitstream,
requestedCompletionDate` → four numbered order items: (1) `add` `PO:
X-GPON Line (WB Access)`; (2) `noChange` on `P: 123-2 (WB Profile)`,
annotated `dependsOn 1`; (3) `add` `PO: CPE Installation` with an
`Appointment` and `dependsOn 1`; (4) `delete` on `P: 123-1 (WB Access -
VDSL)`, which references `R: lineId: 99123`.
