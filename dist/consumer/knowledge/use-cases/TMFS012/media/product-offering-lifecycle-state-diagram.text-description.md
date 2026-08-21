# product-offering-lifecycle-state-diagram.png

**Type:** UML state diagram.
**Source context:** `# Information View` / `## Lifecycles` / `###
Product Offering Lifecycle`, an informative (not normative) state
machine proposed for illustration since no lifecycle is defined for
Product Offering in SID or TMF620.

States, from the initial node: `inDesign` (Initial) transitions to
`designed` ("ProductOffering design completed") or to `rejected`
("ProductOffering definition abandoned"). From `designed`: to `active`
("ProductOffering Test ok, ready to be use for commercial purpose") or
to `rejected` ("ProductOffering test KO abandoned"). From `active`: to
`launched` ("Start of marketing, ProductOffering ready to be ordered &
delivered") or to `retired` ("ProductOffering not launched
commercially"). From `launched`: to `unavailable` ("no more available
for new Product Offering bundles or direct sales, and still used at
least by one active or launched Product Offering bundle") or to
`retired` ("no more available and not used in any available
productOffering bundle"). From `unavailable`: to `retired` ("no more
available and not used in any available productOffering bundle"). From
`retired`: to `obsolete` ("no more installed product using this
productOffering"). Both `rejected` and `obsolete` transition ("final")
to the final node.
