Architecture/block diagram showing the ODA component model for this use case's B2B2X scenario. Appears in the "ODA component model" subsection of the Description, illustrating the components and TM Forum Open APIs involved across the Marketplace Owner and its two Business Partners.

Three dashed-outline domain boxes, left to right:

**Marketplace owner** domain contains:
- **Product Order Capture and validation (TMFC002)** — connects down via **TMF 622 (No API exposure - Notification only)** to:
- **Product Order Delivery & Orchestration (TMFC003)** — the central component, connected to:
  - **Party Management (TMFC028)** via **TMF632** (arrow points from Party Management back to the orchestration component)
  - **Service Catalog Management (TMFC006)** via **TMF633** (arrow points from Service Catalog Management back to the orchestration component)
  - **Resource Inventory Management (TMFC012)** via **TMF716**
  - **Service Order Management (TMFC007)** via **TMF 641**
  - **AI driven Intent based Orchestration** (no component ID given) via a **TBD** labelled connection
  - **Product Inventory Management (TMFC005)** via **TMF637**
  - Both **Resource Inventory Management** and **Service Order Management** additionally connect out to **Product Order Delivery & Orchestration / Service Order Management (TMFC003 / TMFC007)** in the partner domains via **TMF 622 / TMF641** (two long horizontal lines running to the right, one from the Service Order Management box area, one along the bottom of the marketplace-owner box)

**Gaming SW developer** domain contains:
- **Product Inventory Management (TMFC005)**, connected upward via **TMF 637** from:
- **Product Order Delivery & Orchestration / Service Order Management (TMFC003 / TMFC007)** — which receives the **TMF 622 / TMF641** connection from the Marketplace owner's orchestration component.

**MEC provider** domain contains the identical pair of components as the Gaming SW developer domain:
- **Product Inventory Management (TMFC005)**, connected upward via **TMF 637** from:
- **Product Order Delivery & Orchestration / Service Order Management (TMFC003 / TMFC007)** — which receives its own **TMF622 / TMF641** connection from the Marketplace owner's orchestration component (the bottom-most long horizontal line).

In short: the Marketplace Owner's central Product Order Delivery & Orchestration component fans out to its own Party Management, Service Catalog Management, Resource Inventory Management, Service Order Management, AI-driven orchestration, and Product Inventory Management components, and separately reaches across the B2B2X boundary via TMF622/TMF641 to an equivalent Order Delivery & Orchestration/Service Order Management pairing inside each of the two Business Partner domains (Gaming SW developer and MEC provider), each of which maintains its own Product Inventory Management component via TMF637.
