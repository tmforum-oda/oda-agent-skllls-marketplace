# architecture-approach-b-sor-steers.jpeg

**Type:** Architecture/block diagram.
**Source context:** `# Appendix` — "Approach B: SoR steer the process,"
the second row of the same architecture comparison table, paired with
`architecture-approach-a-soe-steers.jpeg`.

Same two-block layout as the Approach A image, with one key difference:

- **Engagement Management** (purple): still contains a **Frontend** box
  (green), but the frontend itself is now empty — no process-step
  chevrons inside it.
- **Party Management / Core Commerce Management** (red / dark blue): the
  Core Commerce Management block now contains a **Process Flow** box
  with the row of process-step chevrons moved *into* it — illustrating
  that in this approach, the System of Record (SoR) side owns and steers
  the process via the Process Flow capability (TMF701), not the
  frontend.

Matches the accompanying text: "Based on independent components... TMF701
Process Flow API is used here to decouple front-ends and process
layers... APIs and components are directly reusable by any Front-End."
