ASCII-art architecture diagram (FIG 3.3.2, "Example of Network incident Identification IETF NMOP Network Incident YANG-03") illustrating an "Incident Identification service VPN Degradation Example" from the Reactive assurance models section.

The diagram is a box-and-line tree drawn in monospace text:

- **"Orchestrator"** (top box), connected down to
- **"controller"** (middle box), which receives an upward-pointing arrow labelled **"^VPN A Degradation"** from below, and itself receives two upward arrows from the layer below labelled **"Packet Loss"** and **"Path Delay"**.
- The bottom row represents a **"VPN A"** topology: a chain of four device boxes — **PE1 — P1 — P2 — PE2** — with backslash/forward-slash marks on the outer edges indicating the VPN extends beyond PE1 and PE2 to other sites.

The diagram shows how low-level VPN A network resource symptoms (Packet Loss at P1, Path Delay at P2) are reported upward through the controller as an aggregated "VPN A Degradation" incident to the Orchestrator — illustrating the IETF NMOP incident-identification pattern applied to a VPN degradation scenario.
