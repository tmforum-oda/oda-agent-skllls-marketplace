# modify-wb-profile-structure-diagram.png

**Type:** Payload-structure mind-map (a tree illustrating the shape of
an example ProductOrder request for a WB Bitstream Profile change), not
an entity-relationship data model.
**Source context:** `## Operational Stage: Upgrade/Downgrade` / `###
ProductOrder for Upgrade/Downgrade`, illustrating a "modify" order item
example that changes a customer from one WB Bitstream Profile to
another.

Tree: `ProductOrder, productChange, requestedCompletionDate` →
`1, modify, created` → two branches: `P: 123-2 (PO: BigNetwork M)` (the
existing product instance being modified, with its new product offering
reference) and `PO: BigNetwork L` (the product offering it is being
changed from).
