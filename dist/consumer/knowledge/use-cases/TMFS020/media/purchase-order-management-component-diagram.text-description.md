Architecture/component ("opening the box") diagram, appearing in the "Sequence diagrams" section under "4.B Step 2 Framework Agreement instanciation through Implementation Agreement between CSP and its Customer", in the table row "instanciation of Implementation Agreement, focus on purchase order from CSP to its Supplier". It is the component-level companion to the sequence diagram `purchase-order-management-sequence.png`.

Elements shown, inside an "Organization" boundary box (with a "Supplier" boundary box below it):
- **TMFC002 POCV** (hexagon, left) connected to **TMFC033 Purchase Mgt** (hexagon, centre) by a bidirectional arrow labelled "1, 9" (POST SupplierOrder in, and the final OK/PurchasedProductID response out).
- TMFC033 Purchase Mgt connected to **Product Catalog / TMFC001** (hexagon, bottom) via arrow "4" (identify ad hoc Supplier).
- TMFC033 Purchase Mgt connected to **Product Inventory / TMFC005** (hexagon, right) via arrow "5, 9" (initialize/update the Product ordered to Supplier).
- TMFC033 Purchase Mgt connected downward via a dashed arrow "6" to a hexagon **TMFC002 POCV** (labelled "Supplier") in the Supplier boundary box, representing the order placed to the Supplier (POST TMF622).
- A yellow cloud note "or purchased Product Inventory?" next to the Product Inventory connection, flagging an open modelling question about whether the ordered Supplier product should be represented as a purchased Product Inventory item.

The diagram is the component-level view of the numbered POST SupplierOrder / TMF620 / TMF637 / TMF622 message flow in the paired sequence diagram, showing which ODA components (Purchase Mgt, Product Catalog, Product Inventory, and the Supplier's own POCV) are involved in organising a purchase order to a Supplier.
