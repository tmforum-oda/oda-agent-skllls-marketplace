Architecture/conceptual block diagram (color-coded comparison table rendered as boxes, not a UML or entity-relationship diagram). Appears after the "Legal Aspect vocabularies" list as Figure 8.1.2 "Model Mapping challenges", giving an overview of the technical challenge of mapping three different specification technologies for Agreements.

Titled "Overview of Technical challenge", with a callout note top-right reading "Priority for GSMA OPG Legal Aspects" (a magenta speech-bubble) pointing at the second "Mapping" arrow.

The layout is three columns, each headed by a dark-blue rounded box naming a specification, with two left-pointing "Mapping" arrows (dark blue, double-outlined) drawn between the columns at the top (between column 1↔2 and column 2↔3), indicating bidirectional mapping challenges between adjacent specifications:

| | Column 1 | Column 2 | Column 3 |
|---|---|---|---|
| **Specification** | SID Agreement ISA 757 | TMF651 Agreement Management | Oasis eContract |
| **Technology** (green box) | UML Model | REST/JSON Resource Model | XSD/RDF Model |
| **Scope** (blue box) | Scope: Contracts and Agreement incl. Implementation agreements | Scope: Agreement Documents and Attachments | Scope: Contract Documents Structure and attachments, general contract vocabulary e.g. Signatures |
| **Gaps** (magenta box) | Incomplete Attributes | Precise mapping to SID Incomplete attributes | Contract specific Legal Attributes by reference to legal ontologies e.g. Sali LMSS Missing |

Each row is labelled by a small white box at the left edge of column 1 ("Technology", "Scope", "Gaps") that applies across all three columns. The diagram's overall point is that mapping between the UML-based SID model, the REST/JSON TMF651 API, and the XSD/RDF-based OASIS eContract format is technically challenging because each has a different modelling technology and incomplete attribute coverage, especially for contract-specific legal attributes that need to reference external legal ontologies.
