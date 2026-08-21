ASCII-art architecture diagram (Figure 3.3.4, "IETF NMP Framework for a Network Anomaly Detection Architecture") illustrating the IETF proactive-assurance anomaly-detection architecture as a set of cooperating functions and their streaming data flows, drawn as nested monospace boxes connected by "Stream", "Subscribe", and "Publish" labelled lines.

Main boxes and their connections:

- **"Service Inventory"** feeds a **"Post-mortem System"** (Stream) and connects across to **"Network Model"** (bottom-left area).
- **"Alarm and Problem Management System"** receives a Stream from **"Message Broker with Analytical Network Data"**.
- **"Profile and Generate SDD Config"** and **"Fine Tune SDD Config"** feed down into **"Service Disruption Detection Configuration"**, which exchanges a "Schedule Detection" link with **"Service Disruption Detection"**.
- **"Alarm Aggregation for Anomaly Detection"** and **"Store Label"** feed/receive Streams to/from **"Service Disruption Detection"** and **"Replay Data Storage"**.
- **"Network Model"**, **"Data Aggr. Process"**, and **"Store Operational Data"** exchange Streams with each other and with **"Message Broker with Operational Network Data"**.
- At the bottom, **"Network Node with Network Telemetry Subscription"** exchanges "Subscribe"/"Publish" links with **"Network Telemetry Data Collection"**.

This is a dense, code-style block diagram (not a UML class or sequence diagram) describing the internal data-flow architecture — inventory, alarm/problem management, service-disruption-detection configuration and tuning, anomaly-detection alarm aggregation, replay/data storage, network modelling, and telemetry subscription/publishing — that underlies the anomaly-detection framework referenced in this section.
