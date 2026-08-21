UI wireframe/mockup. Appears in the "Description" section immediately after the actor/pre-conditions/description table, illustrating the screen-by-screen flow a customer and Helpdesk Agent step through when a customer reports a problem via IVR.

Seven mocked-up screens, connected by blue arrows showing the flow order:

1. **IVR Menu** — a numbered list: "1. Last Bill Payment", "2. Check Unbilled Usage", "3. Report a Problem" (highlighted/selected), "4. Other services".
2. **Connecting to the Agent** — text: "Please wait while we connect you to a customer care agent....".
3. **Agent Incoming interaction** — shows `Interaction Id: SOMEID1234`, `Channel: IVR`, `Request Type: Problem Report`, with **Accept** (green) and **Reject** (blue) buttons.
4. **Customer Identification** — input fields "Customer Id/ Phone number", "Name", "DOB/Email", with **Validate** (green) and **Clear** (blue) buttons.
5. **Customer Profile** — read-only fields `Name: John Doe`, `Customer ID: CUST1234`, `Status: Active`, with three placeholder action buttons underneath.
6. **Report Problem** — fields `Type: Incident`, `Severity: Critical`, `Product Service: Mobile Plan 1234XXX`, a free-text `Description:` box, with **Submit** (green) and **Cancel** (blue) buttons.
7. **Customer Notification** — confirmation text: "You ticket number is **TT-123456XYZ**. You Issue will be resolved in Next XX Hours".

Flow: IVR Menu → Connecting to the Agent → Agent Incoming interaction → (on Accept) Customer Identification → Customer Profile → Report Problem; Customer Identification also links directly down to Customer Notification (the ticket-confirmation screen shown to the customer once the identification step completes and a ticket number is available).
