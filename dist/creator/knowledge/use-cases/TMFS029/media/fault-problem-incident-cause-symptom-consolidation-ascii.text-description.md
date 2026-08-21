ASCII-art conceptual diagram ("Figure 5: Consolidation of Symptoms and Causes"), embedded inline in the Terminology table's "Incident" row, illustrating how the IETF NMOP terminology concepts Fault, Problem, Incident, Cause, and Symptom relate to one another.

Five labelled boxes connected by dashed arrows:

- **"Fault"** (bottom left) points right to **"Problem"** (bottom middle), which points right to **"Incident"** (bottom right).
- **"Fault"** also points up to **"Cause"** (middle), which points right to **"Symptom"** (top right); **"Cause"** also has a self-referencing loop arrow (drawn as a short vertical stub below it) and receives an arrow back from **"Problem"** below it.

The overall shape traces: a Fault gives rise to both a Cause and (via the bottom row) a Problem; the Cause is linked bidirectionally with the Problem and produces a Symptom; and the Problem is what is reported upward as an Incident. This diagram illustrates the terminology scenario referenced immediately after it in the table's "Interpretation" column: "This scenario assumes incidents are timestamped."
