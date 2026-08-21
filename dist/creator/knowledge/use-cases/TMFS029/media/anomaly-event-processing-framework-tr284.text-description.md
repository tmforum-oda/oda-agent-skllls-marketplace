Process/flow diagram (Figure 3.3.6, "Framework of Anomaly Event processing TR284") showing the end-to-end anomaly event processing pipeline as four dashed-box stages connected left to right by arrows, with a feedback loop arrow running along the bottom from the last stage back to the first.

Stages, left to right:

- **"Anomaly Detection"**: "Data Capture" (1.1) → "Exception awareness" (1.2), and "Data Capture" also feeds "Service Impact Analysis" (2.1) in the next stage.
- **"Anomaly Event Assessment"**: "Anomaly event identification" (2.2, fed by Exception awareness) and "Service Impact Analysis" (2.1) both feed "Anomaly Event Demarcation" (2.3), which feeds "Anomaly Event Location" (2.4).
- **"Anomaly Event Mitigation"**: "Match mitigation resolution" (3.1) → "Evaluate Feasibility of Mitigation Solution" (3.2) → "Determine Mitigation Solution" (3.3), which feeds "Execute Mitigation Solution" (4.1) → "Service recovery verification and report" (4.2).
- **"Anomaly Event Learning Management"**: "Anomaly Event Case History" (5.1) → "Knowledge Assimilation" (5.2), with a feedback arrow running back along the bottom of the whole diagram to "Data Capture" (1.1), closing the loop.

The body text below the figure defines each stage: Anomaly Detection (monitoring quality/state, collecting and preprocessing data, identifying exceptions to support awareness), Anomaly Event Assessment (four submodules — service impact analysis, anomaly event identification, demarcation, and locating), Anomaly Event Mitigation (matches, evaluates, determines, and executes the mitigation solution, then verifies and reports recovery), and Anomaly Event Learning Management (extracts and applies knowledge — identification rules, diagnosis/location logic, resolution matching rules, service verification policies — to continuously enrich the closed-loop capability).
