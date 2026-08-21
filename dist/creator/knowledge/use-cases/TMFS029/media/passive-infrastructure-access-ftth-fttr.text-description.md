Physical infrastructure block diagram (Figure 3.5.2, "Passive Infrastructure Access network"), titled "Passive Infrastructure — Access (FTTH/FTTR)", showing the physical cabling path of a PON access network end to end, labelled along the top as the "PON Optical Path".

Left to right:

- A **"CO" (Central Office)** box contains two **"NE-1"** / **"NE-2"** device icons (each labelled "WDM" with a red "A1"/"A2" port), stacked with a "..." indicating more, all grouped as **"(OLT)"**. Each NE connects via a "Cable (single fiber)" line to a yellow connector on an **"ODF"** (Optical Distribution Frame) box, from which a "Feeder cable" (with "X" splice point and two "Joint box" splices along three "Cable Segment"s) runs out to a **"Splitter" / "FDT"** (Fibre Distribution Terminal) box.
- From the FDT, a "Distribution cable" runs to a second **"Splitter" / "FDT"** box.
- From that FDT, a further "Distribution cable" runs to an **"FAT"** (Fibre Access Terminal) box.
- From the FAT, a "Drop cable" runs to an **"ATB"** (Access Terminal Box) device icon, which fans out via three "Drop cable" connections to three end-customer connectors: **ONU 1, ONU 2, ONU 3**.

This diagram illustrates the physical passive fibre plant — cable segments, joint boxes, splitters, and distribution/drop cabling — between the OLT in the Central Office and the end-customer ONUs in an FTTH/FTTR access deployment, corresponding to the "Fibre Transport Service" and "Line plant Mngt System & Inventory" boxes referenced elsewhere in the layered service model diagrams. An editorial note in the surrounding text states that UML models describing these entities are still to be added, based on an mTOP contribution.
