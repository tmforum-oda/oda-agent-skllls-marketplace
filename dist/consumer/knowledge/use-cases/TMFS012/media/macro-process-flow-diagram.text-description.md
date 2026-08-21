# macro-process-flow-diagram.png

**Type:** BPMN-style process flow diagram (start/end events, tasks, and
exclusive gateways), not a UML sequence diagram or an entity-relationship
model.
**Source context:** `# Description` section, the end-to-end macro
process for designing, testing, and launching a new Product Offering,
annotated with the seven steps detailed by the sequence diagrams in
`# Sequence diagrams`.

Flow: a start event leads to `Identify support Product Specification`,
then a gateway "Existing Product Specification to use for new offer?" —
"no" branches to `Create a new Product Specification` before rejoining,
"yes" continues directly (**step 1**) — into `Create a new Product
Offering (PO)` (**step 2**). A gateway "Need to associate a price?" — if
yes, either "a new POP is needed" (branches to `Create a new Product
Offering Price (POP)`, **step 3**) or "an existing POP can be reused"
(skips directly); if no, the flow skips price association entirely —
both paths converge into `Associate PO to (POP)` (**step 4**). A further
gateway leads to `Validate Product Offering Design`, then `Test Product
Offering` (**steps 5 & 6**). A final gateway, gated by "Marketing Launch
request & conditions", leads to `Launch Product Offering` (**step 7**)
and the end event.
