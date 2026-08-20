# product-specification-lifecycle-state-diagram.png

**Type:** UML state diagram.
**Source context:** `# Information View` / `## Lifecycles` / `###
Product Specification Lifecycle`, an informative (not normative) state
machine proposed for illustration since no lifecycle is defined for
Product Specification in SID or TMF620.

States, from the initial node: `inDesign` (Initial) transitions to
`designed` ("ProductSpec design approved") or to `rejected` ("ProductSpec
design abandoned"). From `designed`: to `active` ("ProductSpec Test ok.
The productSpec is ready to be ordered in production") or to `rejected`
("ProductSpec test KO abandoned"). From `active`: to `unavailable` ("no
more available for new productOffering and still used at least by one
available productOffering") or to `retired` ("no more available for new
productOffering and not used in any available productOffering"). From
`unavailable`: to `retired` ("no more used by any launched
productOffering"). From `retired`: to `obsolete` ("no more installed
product using this productSpecification"). Both `rejected` and
`obsolete` transition ("final") to the final node.
