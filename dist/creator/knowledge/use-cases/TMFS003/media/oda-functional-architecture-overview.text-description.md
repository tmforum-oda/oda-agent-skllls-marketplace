# oda-functional-architecture-overview.png

**Type:** Architecture/functional-block diagram.
**Source context:** `## Context or Background`, illustrating the ODA
functional blocks this use case's flow moves through.

A horizontal stack of ODA functional blocks, top to bottom, each
separated by a "DECOUPLING AND INTEGRATION" band: **Party Management**
(red) → **Core Commerce Management** (dark grey) → **Production** (dark
blue), flanked on the left by **Engagement Management** (purple) and on
the right by **Intelligence Management** (grey), both spanning the full
height and also separated from the central stack by their own
"DECOUPLING AND INTEGRATION" bands.

Inside the Production block, four parallel "factories" are shown, each
with the same internal three-layer pattern (Catalog → Orchestration →
Inventory): **Access Factory** (Service Catalog / Service Orchestration /
Service Inventory), **Network Service Factory** (same three layers),
**Soft Service Factory** (same three layers), and **Supply Chain
Factory** (Supply Chain Catalog / Supply Chain Orchestration / Supply
Chain Inventory).
