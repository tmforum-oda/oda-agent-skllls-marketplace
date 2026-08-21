Architecture/component ("opening the box") diagram, appearing in the "Sequence diagrams" section under "4.A Step 1 Framework Agreement definition between the CSP and its Customer", in the table row "Customer Intent Management / SalesLead". It is the component-level companion to the sequence diagram `customer-intent-management-pattern-sequence.png`, showing the same step 1/2 messages as arrows between ODA-component hexagons rather than as a lifeline sequence.

Elements shown, all inside an "Organization" boundary box:
- A purple lifeline/activity bar on the left, annotated "AOF ???" and a yellow note "Translation (regardless language)".
- **TMF683 Party Interaction** labelled arrow "2", running from the lifeline into **TMFC023 Party Interaction Mgt** (hexagon).
- **TMFC036 Lead & Opportunity** (hexagon, top) connected to TMFC023 Party Interaction Mgt via arrow "2.d".
- **TMFC??? Party Request Mgt** (hexagon, top right) connected to TMFC023 Party Interaction Mgt via a two-way arrow labelled "2c alt B", with a yellow note "TBC: 2 components or enrichment of PartyInteraction Mgt capabilities?".
- A "???" labelled arrow (yellow, unresolved) between TMFC023 Party Interaction Mgt and a grey box labelled "AOF Customer Intent interpretation in IT Assets", itself annotated "2c alt A" and a yellow note "TBC: Component enrichment? Canvas / Intelligence Mgt asset? dedicated to Customer intent or shared?".
- From TMFC023 Party Interaction Mgt, arrow "2e" (labelled "regarding context") fans out to three hexagons at the bottom: **TMFC002 POCV**, **TMFC... Product Assurance Mgt**, and an unlabelled "..." hexagon, representing further possible downstream components.

The diagram captures the same open design questions as the sequence diagram it accompanies: whether customer intent is handled directly by Party Interaction Mgt or delegated to a (possibly new) Party Request Mgt component, and how/where the actual intent interpretation happens.
