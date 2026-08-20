# architecture-approach-a-soe-steers.jpeg

**Type:** Architecture/block diagram, not a sequence diagram.
**Source context:** `# Appendix` — "Approach A: SoE steers the process,"
one row of the two-row architecture comparison table (paired with
`architecture-approach-b-sor-steers.jpeg`).

Two adjacent blocks:

- **Engagement Management** (purple): contains a **Frontend** box
  (green), inside which a row of small red chevron/arrow shapes
  represents the process steps being sequenced *within* the frontend
  itself — illustrating that in this approach, the System of Engagement
  (SoE) owns and steers the process logic.
- **Party Management / Core Commerce Management** (red / dark blue,
  side by side): each shown only as a colored block with a few small
  green hexagons (representing exposed capabilities/APIs), with no
  internal process shown — because in Approach A, these backend
  components are passive API providers, not process owners.

Matches the accompanying text: "Frontends can define the processes
autonomously while leveraging the Open APIs provided by the SoRs."
