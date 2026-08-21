Architecture/block diagram (Figure 3.3.5, "Anomaly management Closed Loop functions TR284A") showing the TM Forum Anomaly Management architectural framework as a layered OODA-style (Observe/Orient/Decide/Act) model, with two vertical columns ("Security" and "Integration, Orchestration, Performance Management") crossing four horizontal function layers, and a "Key Anomaly Management Closed Loops" callout on the right.

Rows, top to bottom, each labelled with an OODA stage on the left:

- **ACT (MODEL & EXECUTE PROCESSES)** — row "Process Execution (Model and execute processes - Action Management)": boxes Actuator, Notifier/Reporter, Monitor, Exception Handler, Presentor.
- **DECIDE (MODEL & EXECUTE DECISION)** — row "Decision Execution (Insights / Intelligence Management)": boxes AI Model Trainer, AI Model Validator, AI Model Tester, AI Model Operator.
- **ORIENT (BUILD INFORMATION Analysis & Dissemination ACROSS DATA SOURCES)** — row "Data Composition (Data Science / Analytics Management)": boxes Data Acquirer, Data Cleanser, Data Transformer, Data Modeler (Analysis).
- **OBSERVE (CONNECT RESOURCES e.g. APPS/SERVICES... AND DATA)** — row "Data Collection (Collection & Storage Management)": boxes Operational Data Handler, Performance Data Handler, Usage Data Handler, Context Handler.
- Bottom row, **"Resources & Services"** (black band): boxes Functional Services, Virtual Infrastructure, Connectivity Services, Any Infrastructure, Edge Devices.

Footnote boxes at the bottom read: "Cross layer/level/domain concern in any stack. Security consideration for the automation, different levels of activities in the layers. Security is not a component or one component. It's a function that has multivariate concerns" (left) and "Orchestration Management, Integration Management, Interaction Governance, Performance Management" (right).

The right-hand callout lists the "Key Anomaly Management Closed Loops": Anomaly Mitigation/Recovery, Anomaly Assessment, Anomaly Prediction, Anomaly Detection, and Events & Data/Telemetry collection — each shown as a stack of layered cards.

This diagram identifies the functions needed for Anomaly Management closed loops, mapped onto the Observe/Orient/Decide/Act model (functionally similar to the awareness/analysis/decision/execution model used in the Autonomous Network Functional Architecture).
