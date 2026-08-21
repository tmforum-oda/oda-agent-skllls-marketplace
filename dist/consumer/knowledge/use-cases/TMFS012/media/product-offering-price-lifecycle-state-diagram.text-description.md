# product-offering-price-lifecycle-state-diagram.png

**Type:** UML state diagram.
**Source context:** `# Information View` / `## Lifecycles` / `###
Product Offering Price Lifecycle`, an informative (not normative) state
machine proposed for illustration since no lifecycle is defined for
Product Offering Price in SID or TMF620.

States, from the initial node: `inDesign` ("Initial - A POP is
designed") transitions to `available` ("POP available for new PO") or
to `retired` ("POP design abandoned"). From `available`: to
`unavailable` ("POP not available for new PO but still used at least by
one active/available/designed PO") or to `retired` ("POP not available
for new PO and not used in any active/available/designed PO"). From
`unavailable`: to `retired` ("POP unavailable and not used in any
active/available/designed PO"). From `retired`: to `obsolete` ("No more
customer owning a PO linked to this POP"), which transitions ("final")
to the final node.
