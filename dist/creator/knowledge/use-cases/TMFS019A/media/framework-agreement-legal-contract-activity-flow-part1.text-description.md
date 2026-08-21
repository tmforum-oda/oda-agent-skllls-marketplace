UML activity diagram (top part). Appears in the "Diagrams" section under "Activity Diagrams for FrameworkAgreement(type= LegalContract) and Framework-Agreement definition", captioned in the body as Figure 4.1 "Framework Agreement / Legal Contract Activity Flow". It continues onto a second image (see [framework-agreement-signing-and-management-activity-flow-part2.png](framework-agreement-signing-and-management-activity-flow-part2.png), captioned Figure 4.2).

The diagram is titled "FrameworkAgreement/ Legal Contract Activity Flow" and starts from a UML initial node (filled black circle) at the top. It is organised into two large swimlane-like activity partitions, each corresponding to a TMFS019 sub-scenario from Table 2-1:

**Partition "TMFS019-2 Foundation 'Partner/Supplier' FrameworkAgreement- Step 2{}"**
- Entry-criteria note: "FrameworkAgreement Specification/Template"
- Activity: "Identify Foundation Partner/Suppliers"
- Activity: "Define Partner/Supplier FrameworkAgreementInstance"
- Exit-criteria note: "FrameworkAgreement Instance Created"

**Partition "TMFS019-3 Partner/Supplier FrameworkAgreementInstance -Step 2{}"**
- Entry-criteria note: "FrameworkAgreement Instance"
- Activity sequence: "Identify Contractual Partner/Suppliers" → "Review Contract Terms" → "Define Obligations" → "Agree attachment of T&C, Agreement Items etc. to FrameworkAgreement Instance"
- Decision "Terms Agreed?": the "not agreed" branch loops through "Negotiate Terms" (annotated "Discuss changes") → "Review Contract Terms and Conditions, AgreementItems, Documents, Attachments,etc." and back to the decision; the "agreed" branch continues forward.
- Activity: "Draft FrameworkAgreement(type=LegalContract) Instance" → "Legal Review"
- Decision "Legal Approved?": the "not agreed" branch loops through "Request Modifications" (annotated "Revise terms") → "Review Contract Terms" (annotated "Discuss changes") → "Negotiate Terms" (annotated "Step 2 Protocol Exchange") → "Review Contract Terms" and back to the decision; the "agreed" branch continues forward.
- Activity: "Defined Partner/Supplier FrameworkAgreement(type=LegalContract) Instance"
- Exit-criteria note: "FrameworkAgreement Instance Created"

The flow then enters a nested partition **"TMFS019-5 FrameworkAgreement Management - Step 3{}"** (continued in part 2): a decision "Add Contracted Product Offering?" whose "yes" branch leads to "Product OfferingSpecification Addition" (exit-criteria note: "Product Offering Instance Created") and whose "no" branch skips directly to a merge/decision node, which is where this image is cropped and continues in part 2.
