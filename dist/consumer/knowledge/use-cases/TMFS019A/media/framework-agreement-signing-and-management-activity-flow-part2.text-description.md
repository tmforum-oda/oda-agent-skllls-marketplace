UML activity diagram (bottom part, continuing directly from [framework-agreement-legal-contract-activity-flow-part1.png](framework-agreement-legal-contract-activity-flow-part1.png)). Together the two images make up Figure 4.1/4.2 "Framework Agreement / Legal Contract Activity Flow" and "Activity diagram for TMFS019A Sub Scenario processes Step 3 focus" in the "Diagrams" section.

It continues the **"TMFS019-4 FrameworkAgreement Signing - Step 3{}"** partition:
- Entry-criteria note: "Contractual Agreement Instance Created"
- Activity sequence: "Identify Partners" → "Credit check and validation of Partners" → "Prepare Signature" → "Execute Agreement" (annotated with two free-floating notes, "Execute Agreement" and "Step 3 Protocol Exchange")
- A fork bar splits into two parallel branches: "Review Contract Terms" → "Partner 1 Signing" (left branch) and "Review Contract Terms" → "Partner n.. Signing" (right branch), representing signature collection from multiple partners in parallel.
- A join bar merges the branches back together into "Record & Archive" (exit-criteria note: "Contractual Agreement Instance(s) Signed") → "Distribute Signed Multiparty Contractual Agreement".

The flow then enters the **"TMFS019-5 FrameworkAgreement Management - Step 3{}"** partition (the same partition begun at the bottom of part 1):
- Activity: "evaluate Amendment" (entry-criteria note: "Contractual Agreement Instance(s) Signed / Amendment proposal")
- Decision "FrameworkAgrementAdjustment" with five outgoing branches, each leading to its own activity before rejoining at a common merge node: "Product OfferingSpecification Addition" → "Add Product Offering"; "ProductOfferingSpecfication Removal" → "Remove Product Offering"; "Term and condition Addition" → "Add Term and condition"; "Term and condtion Removal" → "Remove Term and condition"; "other" → "help".
- All five branches rejoin at a merge node leading to "Amendment Actioned and Distributed" (exit-criteria note: "Updated FrameworkAgreement Instance(s) Signed").
- The diagram ends at a UML final node (filled black circle inside a ring) at the bottom.
