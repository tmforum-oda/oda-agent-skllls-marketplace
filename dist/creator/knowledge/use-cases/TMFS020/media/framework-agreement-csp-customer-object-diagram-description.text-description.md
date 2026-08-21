Screenshot of explanatory narrative text (not a diagram), appearing immediately alongside `framework-agreement-csp-customer-object-diagram.png` (Figure A.14 - Illustration 03: FrameworkAgreement between CSP and Customer) in the Information View section, "3. A Framework Agreement definition between the CSP and its Customer". It is the paired prose walkthrough of that SID object diagram, reading as follows:

This illustration represents a Framework Agreement between Greenfield International Business (Greenfield IB) and one organization called Middle East Finance Systems (MEF Systems).

During DTW, a representative of Greenfield IB met a representative of MEF Systems. As their meeting was productive and could trigger sales, Greenfield IB created a Sales Lead for this potential customer. After some additional interactions, MEF Systems raised interest for some B2B offers and especially Greenfield IB SASE offer. A SalesOpportunity was created with one SalesOpportunityItem concerning SASE offer.

Before doing any business with MEF Systems, Greenfield IB process requires the signature of a FrameworkAgreement with MEF System. This first SalesOpportunity with MEF Systems triggers the creation of a FrameworkAgreement between Greenfield IB and MEF Systems. The SalesOpportunityItem related to SASE offer raised the creation of a FrameworkAgreementItem related to SASE ProductOfferingSpecification.

This Framework Agreement is produced by Greenfield IB based on its standard Sale FrameworkAgreementSpec.

This Framework Agreement is valid for 2 years from the 1st of October 2025. It is formalized through a Document that includes all elements.

This Framework Agreement is valid for Middle East area (AgreementLocationRole has associated "Middle East" Place).

In this example, the FrameworkAgreement has three FrameworkAgreementItems.

One concerns Ethic clauses (includes Greenfield IB code of ethics and commitment from all parties to respect this code).

A second FrameworkAgreementItem includes clauses related to payments (like payments by MEF Systems are performed latest 30 days end of the months after invoice reception).

The third FrameworkAgreementItem concerns Greenfield IB SASE Offer. This FrameworkAgreementItem is valid only until the 31st of August 2026 because the prices are guaranteed by Greenfield IB's supplier (Cloud Experts) only until this date.

This FrameworkAgreementItem is valid only for Middle East region (AgreementLocationRole / Place).

With this FrameworkAgreementItem, MEF Systems benefits from specific prices alteration (ProdOfferPriceAlteration) that impact the standard SASE offer price plan (ProductOfferingPrice).

This FrameworkAgreementItem allows MEF Systems to perform Create, Update and Cancel actions on SASE Offer. So, MEF Systems can place orders, update its installed base (existing ProductOfferingInstances and associated Products) and cancel existing ProductOfferingInstances.
