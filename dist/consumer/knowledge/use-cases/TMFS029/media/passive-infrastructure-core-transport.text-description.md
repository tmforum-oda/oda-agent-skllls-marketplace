Physical infrastructure block diagram (Figure 3.5.3, "Exemplar passive Infrastructure - Core transport"), titled "Passive Infrastructure — Core Transport", showing the physical cabling path of a core DWDM transport span between two Central Offices.

Left to right:

- A **"CO"** box (left) labelled **"(DWDM)"** contains two device icons **"NE-1"** / **"NE-2"** (each "WDM", ports "A1"/"A2"), stacked with "...", connecting via "Cable (single fiber)" lines into an **"ODF"** box with an "X" splice point.
- From the ODF, a "Cable" (broken into three "Cable Segment"s, with two "Joint box" splices) runs to a central cross-shaped **"FDT?"** splice/cross-connect point, from which a second "Cable" (two further "Cable Segment"s, one "Joint box") continues on to a second **"ODF"** box (right).
- The second ODF connects via "Cable (single fiber)" lines to two device icons **"NE-3"** / **"NE-4"** (each "WDM", ports "A3"/"A1"), inside a second **"CO"** box labelled **"(DWDM)"**.
- A green dashed double-headed arrow labelled **"Span"** runs along the bottom between the two CO boxes, indicating the overall DWDM transport span distance.

This diagram illustrates the physical passive fibre plant — cable segments, joint boxes, and a central cross-connect — carrying a DWDM core transport span between two Central Offices, complementing the access-network diagram (`passive-infrastructure-access-ftth-fttr.png`). An editorial note in the surrounding text states that UML models and term descriptions for these entities are still to be added, based on an mTOP contribution.
