Architecture/block diagram (Fig 1.2) illustrating an example of layering between ServCo and NetCo/InfraCo for an SD-WAN service.

Three horizontal bands, top to bottom:

- **Customer** (green box): two customer cloud icons, "Branch" and "HQ", each connected downward by a vertical line labelled "UNI" to the ServCo band.
- **ServCo** (blue box): three boxes — "SDWAN Edge (Physical)" (connected to the Branch UNI), "SD-WAN Controller" (connected via a line labelled "MEF LSO" up toward the space between Branch and HQ), and "SD-WAN Edge (Virtual)" (connected to the HQ UNI). The SD-WAN Controller is linked horizontally to both edge boxes.
- **NetCo InfraCo** (yellow/orange box, largely undetailed): connected upward to the ServCo band by two vertical lines, one labelled "UNI" (under the Physical SDWAN Edge) and one labelled "??? MEF" (under the SD-WAN Controller), plus a third "UNI" line under the Virtual SD-WAN Edge.

The diagram shows the customer-facing UNI (User-to-Network Interface) demarcation points, the ServCo-owned SD-WAN service layer (edges plus controller using MEF LSO), and the open question (marked "???") of what interface/protocol the ServCo SD-WAN layer uses to reach the underlying NetCo/InfraCo network layer.
