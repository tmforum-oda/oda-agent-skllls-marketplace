Architecture/block diagram (Figure 2.3, "IETF Network Controller models and standards for Technology Domain Managers") showing a layered stack of IETF/BBF network model standards inside a green-dashed box labelled "Self Healing Controller Autonomous Domain / Service Based API", fed from a "Service Intent RFC9315v2" input at the top and exposing a "Network Based API" on the right.

Boxes inside the dashed domain, top to bottom:

- **"Network Service Models — BBF Model+other RFC8299,9182,8466,9291"** and, alongside it, **"Network/Service Applications & Automation"**.
- Both feed down into **"Network Core Model + Extensions — BBF TR-455/RFC8345"**.
- That feeds down into **"Network Abstraction — Abstracted Control of Traffic Engineered Networks RFC8453"**.
- That feeds down into **"Network Inventory/Network Telemetry RFC8348"**, which connects (outside the dashed box, at the bottom) to two device icons labelled **"Heritage/Non-Model Driven"** and **"Model Driven"**.

To the right, outside the main vertical chain but inside the dashed domain, two parallel boxes: **"Service Assurance Intent Based Networking RFC9417"** and **"Network Anomaly Framework RFC9232"**, both exposed via the "Network Based API" on the right edge of the domain.

The diagram maps out which IETF/BBF RFCs and models correspond to each functional layer (service models, core network model, abstraction, inventory/telemetry) and to the assurance/anomaly-detection functions of a self-healing technology domain controller.
