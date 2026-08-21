Architecture/block diagram (Figure 2.4, a reproduced ITU-T slide titled "Y.3061 Architecture framework for Autonomous Networks") showing the draft ITU-T Y.3061 reference architecture.

Main boxes, arranged as a stack with a vertical "E2E Network Orchestrator" bar on the right connected to all of them via labelled reference points (RP-AN-1 through RP-AN-13):

- **"Knowledge Base subsystem"** (top), containing "Information Bases", linked via RP-AN-6/RP-AN-7 to the E2E Network Orchestrator and via RP-AN-1/RP-AN-2/RP-AN-3 down the left side.
- **"Autonomy Engine"** (dashed box) containing two sub-boxes: "Exploratory Evolution subsystem" (with "Evolution controllers") and "Experimentation subsystem" (with "Experiment controller" and "AN Sandbox"); linked via RP-AN-8/RP-AN-9 to an "AN Orchestrator" bar, which itself links to the E2E Network Orchestrator.
- **"Dynamic Adaptation subsystem"**, containing "Curation controllers", "Selection controllers", "Operation controllers", and "Service endpoint"; linked via RP-AN-4, RP-AN-11, RP-AN-12.
- **"Underlay Network"** (bottom), containing "Hardware components", "Software components", "Orchestrator", "Controllers"; linked via RP-AN-5, RP-AN-13.

To the right of the main stack, a separate expanded callout box shows the internals of the **"Knowledge Base Subsystem"**: "Heterogeneous Data Processing", "Knowledge Processing Controller", "Knowledge Lifecycle Management" (top row) and "Data Repository", "Software Modules", "Controllers", "Utility Functions" (bottom row, under "Information Bases"), annotated "Ongoing draft Y.KM-AN".

Below the diagram, explanatory bullet text: exploratory evolution, experimentation, and dynamic adaptation are the three main concepts — exploration/evolution adapts controllers to underlay changes, experimentation continuously monitors/optimizes deployed controllers, and dynamic adaptation equips the network with autonomy to handle new scenarios — supported by knowledge and orchestration.
