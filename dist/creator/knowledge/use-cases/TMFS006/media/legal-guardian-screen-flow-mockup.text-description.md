# legal-guardian-screen-flow-mockup.png

**Type:** UI screen-flow wireframe/mockup (a chain of screen mockups
connected by red flow arrows), not a diagram of a formal notation.
**Source context:** `# Description` section, illustrating John's actions
to identify Bob, add Marie as legal guardian, and validate/attach the
supporting legal document.

**Screen Flow Part 1** — identity verification of the guardian: a
"Welcome John:" menu with a "Search Identity" action opens a search form
(First Name=Marie, Last Name=Curie, ID-Card=00865345) whose "Search"
button leads to a details screen showing Marie's full identity
(ID-Card Type=Passport, Email=marie.curie@Lambda.com) with a "Continue"
action.

**Screen Flow Part 2** — the legal-guardian configuration flow, numbered
Step1–Step6: Step1 "Welcome John:" menu (Manage LegalGuardian / Browse
Catalog / Manage Invoices) → Step2 "Search Customer" (First
Name=Bob, Last Name=Smith, Phone=+33 9 69 39 39 ....) → Step3 "Customer
Details" for Bob (Email=bob.smith@gmail.com, Date of Birth=7/7/2009,
Address=78 rue Olivier de Serres, 75015 Paris, Role=Customer, Activation
Date=23/07/2021) with a "Add Legal Guardian" action → Step4 "Find Legal
Guardian" (searches for Marie by First Name/Last Name/ID-Card/ID-Card
Type, with an "one contact method is mandatory" note) → Step5 "Legal
Guardian Details" for Marie, including an "Attach Legal Letter" field
and Judgement Date=10/10/2021, with a "Grant Legal Guardianship" action →
Step6 final "Customer Details" for Bob showing both roles side by side
(Role 1=Customer, Activation Date=23/07/2021; Role 2=Under Guardianship,
Activation Date=10/10/2021, End Date=10/10/2021, Legal Guardian=Marie
Curie) with an "End Guardnership" action to later terminate it.
