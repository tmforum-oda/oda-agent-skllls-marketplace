Architecture/process overview diagram, captioned "Figure 3. Pre-order and Order Processes for Wholesale NTN Cell Capacity". Appears at the start of the "Description" section, giving a high-level view of the Buyer/Seller ODA component landscape and the three-step process flow between them for the product "Wholesale NTN Cell Capacity".

Two dashed rounded-rectangle domains, left and right, each listing ODA components as colored boxes with their component IDs:

**Buyer/Customer — Mobile Network Operator** (grey box):
- Product Order Capture *(for Business Partner)* — TMFC002 (teal)
- Product Catalog — TMFC001 (teal)
- Product Order Capture — TMFC002 (teal)
- Product Inventory — TMFC005 (teal)
- Product Order Delivery — TMFC003 (teal)

**Seller/Supplier — Satellite Network Operator** (dark blue box):
- Agreement — TMFC039 (red)
- Party — TMFC028 (red)
- Account — TMFC005 (red)
- Product Inventory — TMFC005 (teal)
- Product Catalog — TMFC001 (teal)
- Product Order Capture — TMFC002 (teal)
- Product Configurator — TMFC027 (teal)
- Product Order Delivery — TMFC003 (teal)
- Service Qualification — TMFC009 (dark navy)
- Location — TMFC014 (dark navy)
- Resource Inventory — TMFC012 (dark navy)
- Service Order — TMFC007 (dark navy)

Between the two domains, three horizontal double-headed-arrow interaction bands, top to bottom:
1. **Product Offering Qualification ("I need it there. Can you offer?")** — a bidirectional arrow pair, with a grey overlay callout reading "License, Geo Restrictions, SLA limitations".
2. **Quote ("Give me a proposal")** — a bidirectional arrow pair.
3. **Product Order ("I will take it")** — a bidirectional arrow pair.

This diagram sets up the three sequence diagrams that follow later in the document (Product Offering Qualification, Quote Preparation, and Ordering), each elaborating one of these three interaction bands in full TM Forum Open API detail.
