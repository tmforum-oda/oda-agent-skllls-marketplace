# end-to-end-high-level-flow-diagram.png

**Type:** High-level component/flow diagram (numbered circular flow
markers connecting named components, each component box showing its
relevant catalog/inventory contents), not a UML sequence diagram with
lifelines and not a pure entity-relationship model.
**Source context:** `# Sequence diagram` / `## High Level Flow`, Figure
4.1.1 ("End to End High Level Flow"), an overview of how the order flows
through Product/Service/Resource layers alongside the catalog and
inventory items each stage touches. The body notes that
serviceability/feasibility steps are omitted here for simplicity.

Flow, in numbered order:

1. Customer Order Received based on the Offerings in Product Catalog →
   into `Product Order Configuration and Validation (POCV)`, which holds
   the `Business Slice Product Order` (containing `Package Product
   Order Item` and `Business Slice Product Order Item`).
2. "Product Order with associated order items created in Product Order
   inventory" — POCV validates order items against `Product Catalog
   Management` (containing Platinum/Gold/Silver Package Product Spec
   and Business Slice Product Specification), which responds "Product
   Order Item Validated".
3. "POCV Creates inventory items for Business Slice and Package" →
   `Product Inventory Management` (containing `Package Product` and
   `Business Slice Product`).
4. "POOM receives notification on the Event Bus" → `Product Order
   Orchestration and Management (POOM)`.
5. "POOM Updates inventory items for Business Slice and Package" back
   into Product Inventory Management.
6. "POOM decomposes Product Order and initiates Service Order request",
   and separately "Selects matching Service Spec and prepares Service
   Order" from `Service Catalog Management` (containing, under CFS:
   `Business Slice CFS` and `Service Profile Template CFS`; under NSMF:
   `Slice RFS` and `Slice Profile Template RFS`; under NSSMF: `(RAN/
   Core/Transport) Slice Subnet RFS` and `(Optional) Subnet Profile
   Template RFS`) → into `Service Order Management` (containing `CSMF`,
   `NSMF`, `NSSMF`), where the "Service Order validated against Service
   Spec".
7. "SOM prepares: 1) Service Profile and Business Slice (CFS) Instance,
   2) Slice Profile and creates Slice (RFS) Instance" → `Service
   Inventory Management` (containing `Business Slice`, `Service
   Profile`, `Slice`, `Slice Profile`, `Slice Subnet`, `Slice Subnet
   Profile`).
8. "SOM initiates Slice Resource Order request on ROM with Service
   Profile details" → `Resource Order Management`; "The copy of the
   Slice Profile and Slice Instance is stored in Resource Inventory"
   (arrow from Service Inventory Management into Resource Order
   Management).
9. "ROM prepares specific resources and updates RIM" → `Resource
   Inventory Management` (containing `RAN VNF`, `Transport VNF`, `Core
   VNF`, `RAN PNF`, `Transport PNF`, `Core PNF`).
