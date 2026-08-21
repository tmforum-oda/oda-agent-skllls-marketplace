Architecture/conceptual diagram (Figure 3.1, "Connectivity service model TR255 GB999 ODA Production Implemtnation Guidelines"), a slide titled "Connectivity Service Domain — Flow/Connection elements" (subtitled "Primary focus CFS / Works also for RFS (Resource Technology Specific)").

The main illustration is a large blue rounded shape representing a "Connectivity Service Domain", inside which six labelled points (A, B, C, D, X, Z) are interconnected by a dense mesh of thin dashed lines, with one path (through B, C, A, X, Z) highlighted as a thick red curved line. Points B and X are marked with a blue "SAP" (Service Access Point) tag; points C and Z are marked with an orange "CP"/"TP" (Connection Point/Termination Point) tag.

Four callout boxes point at this illustration, explaining the concepts it depicts:

- **"Connectivity Service Domain (new)"** — pointing at the overall blue shape.
- **"Flow / Connection TR255A"**, with a linked box **"ResourceFunctions & SID ConfigurationFeature (Aka TR 255B Feature Groups, Features)"** — pointing at the mesh of connections.
- **"Service Topology — Static constraints on Flows"** — pointing at the mesh from the top right.
- **"Connection Points"** — pointing at the CP/TP tagged points.

A footnote clarifies: "Endpoint: Service Access Point/Termination Point — Points of Presence for Connectivity Service Domain."

This is a conceptual explanation of the TR255A connectivity/flow model (not a UML class diagram) — it illustrates the topology-graph notion of connectivity service domains, flows/connections, resource functions, and connection points that the later MEF SD-WAN and IP service information models (in this document) are built on.
