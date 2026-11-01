# Stage 9 activities and evidence

Common UG and PG record. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage09/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Use the Stage 9 handout and Overview/revision 2 baseline. Keep responses concise and link accessible artefacts; do not paste entire logs or private peer ratings.

Group: Group Exception 1
Members and responsibilities: Carrie Sullivan - completion of all activities except independent review
Stage 8 integrated SHA, command, working directory and actual result:
- Integrated Stage 8 SHA: ae08d6bfaeb5d5eafd00e5cba084dd4f8e59fd2c
- Test command: python -m pytest -q
- Working directory: project/
- Actual result: 41 passed in 0.07s

## A. Tutorial activities

### A1 Session state classification

| Information            | Required session/domain or transient state? | Requirement or reason                                                                |
|------------------------|---------------------------------------------|--------------------------------------------------------------------------------------|
| Patient identity       | Required session/domain state               | Needed to identify registered patients and link appointments to the correct patient. |
| Appointment history    | Required session/domain state               | Must remain available during the session, including cancelled appointments.          |
| Temporary menu choice  | Transient interaction state                 | Only needed to determine the current menu operation.                                 |
| Practitioner specialty | Required session/domain state               | Part of the practitioner's registered information.                                   |
| Debug print output     | Transient interaction/debug state           | Diagnostic output is not part of the application's stored domain data.               |
| Appointment status     | Required session/domain state               | Records whether an appointment is scheduled, cancelled or completed.                 |

What is intentionally lost on exit? All in-memory session data is intentionally lost when the program exits. This includes registered patients, practitioners, appointments and appointment history. The application does not provide persistent storage in Stage 9.

### A2 Interface and domain data plan

Plan before AI. This replaces schema/key design; no database tables are required.

| Function or component | Explicit inputs and types                                                                       | Outputs                            | Responsibility and validation                                                                                                                                            | Domain source / existing constraint                                                                                                                                                                                                                                 |
|-----------------------|-------------------------------------------------------------------------------------------------|------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| appointment_sort_key  | appointment: Appointment                                                                        | tuple[datetime, str]               | Return (date_time, appointment_id) for deterministic ascending sorting.                                                                                                  | Uses read-only Appointment.date_time and Appointment.appointment_id properties.                                                                                                                                                                                     |
| select_appointments   | appointments: list[Appointment], practitioner_id: str, status: AppointmentStatus \| None = None | list[Appointment]                  | Filter by practitioner ID and, if supplied, status. Return a new list sorted by the named key. Do not mutate the source list or appointment objects.                     | Uses appointment.practitioner.practitioner_id, appointment.status, and the three AppointmentStatus values. It does not validate practitioner registration.                                                                                                          |
| Service listing       | practitioner_id: str, status: AppointmentStatus \| None = None                                  | list[Appointment]                  | Validate the practitioner and supplied status; obtain a fresh list from data_store.list_appointments() and pass it to select_appointments.                               | Uses find_practitioner(), to trim and reject blank IDs, and list_appointments(), to return a new list containing the stored appointment objects.                                                                                                                    |
| Console               | User-entered menu choices and values as str                                                     | Displays results and messages only | Prompt, parse, call services, display results and recover from expected ValueError and LookupError. Convert status text to AppointmentStatus before calling the service. | Uses the existing Patient, Practitioner and Appointment constructors and service operations. Patient and practitioner IDs/names and specialty are validated; appointments require actual participant objects, a valid status and a minute-precision local datetime. |

Relate patient ID/name, practitioner ID/name/specialty, and appointment ID/actual participants/date_time/status to the existing contracts: Patient stores a validated patient_id and name; patient_id is read-only. Practitioner stores a validated, read-only practitioner_id, name and specialty. Appointment stores a validated, read-only appointment_id, references to the actual registered Patient and Practitioner objects, a validated date_time, and an AppointmentStatus (SCHEDULED, CANCELLED or COMPLETED). The data store checks that appointment participants are the exact registered objects, not just objects with matching IDs. Its lookup methods use IDs, and its listing methods return new lists containing the stored objects.

### A3 Responsibility violations

| Conceptual case                 | Violation                                                                                                                     | Correct boundary and reason                                                                                                                                                                   |
|---------------------------------|-------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Appointment.cancel reads input  | The domain object handles console interaction, mixing business rules with user-interface code.                                | The console should ask for confirmation. The service should coordinate the cancellation, and Appointment.cancel() should enforce the rule that only a scheduled appointment can be cancelled. |
| Service prints/reads the menu   | The service handles user interaction instead of focusing on application operations.                                           | The console should display the menu, read the user's choice and call the appropriate service method. The service should coordinate the requested operation without printing or prompting.     |
| Query sorts its source in place | The query changes the caller's list, creating an unintended side effect and potentially affecting other code using that list. | The query should return a new sorted list, for example using sorted(), and leave the original list unchanged.                                                                                 |
| Store prints Appointment saved  | The data store mixes data management with presentation by displaying a user-facing message.                                   | The store should manage and retrieve stored objects. The console should display the success message after the service completes the operation.                                                |

### A4 Sorting comparison

For `appointments.sort(key=appointment_sort_key)` and `result = sorted(appointments, key=appointment_sort_key)`, predict source order, return value and result identity. Give a meaningful mutation check:
| Expression | Source list after operation | Return value | Result identity |
|---|---|---|---|
| appointments.sort(key=appointment_sort_key) | The original list is reordered in place. | None | No separate result list is created; appointments is the same list object. |
|result = sorted(appointments, key=appointment_sort_key) | The original list remains in its existing order. | A new sorted list. | result is appointments is False, but the elements in both lists can be references to the same Appointment objects. |

Meaningful mutation check:
Make a copy of the original list order before running the query, then check that the original list still has the same objects in the same order. Also compare relevant appointment fields before and after to check objects themselves were not changed.

Score-example prediction and explanation of passing the named key:
- Example: [("Chen", 5), ("Ali", 8), ("Bea", 8)]
- Explanation: The records are ordered by score first, then alphabetically by name when scores are equal. Passing key=appointment_sort_key gives the sorting function the key function to call for each item. It is different from calling the function yourself inside the argument: key=appointment_sort_key().

### A5 Exit question

Explain cancellation versus deletion, and checks for same-session lookup, all-status listing and SCHEDULED-only exclusion:
Cancellation and deletion are different operations. Cancellation changes the status of an existing appointment from SCHEDULED to CANCELLED. The appointment remains stored, so its history can still be accessed. Deletion removes the appointment record, which would lose the history.

The checks should confirm that:
- Same-session lookup: After cancelling an appointment, searching for its ID still returns the same appointment object, with status CANCELLED.
- All-status listing: Listing appointments for the practitioner without a status filter includes the cancelled appointment as well as scheduled and completed appointments.
- SCHEDULED-only exclusion: Listing with AppointmentStatus.SCHEDULED excludes the cancelled appointment, while leaving it available through lookup and an unfiltered listing.

## B. Human design and contracts

Complete before GitHub Copilot. Record any interface/integrity decision and its reasoning: Retain the existing domain and data-store interfaces and build the Stage 9 functionality around them. Query functions will receive data explicitly and will not access the data store, prompt users or modify appointment records. Services will coordinate operations and validate requests, while the console will handle user input, display and recovery from expected errors. Appointment cancellation will update the existing appointment's status rather than delete the record. Existing domain validation and registered-object identity checks will remain in place.

| Requirement                       | Input / session data                                                     | Operation and responsible component                                                                            | Expected result or error                                                                                                   | Test / evidence                                                                        |
|-----------------------------------|--------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|
| QRY-01: Practitioner filtering    | Appointment list and practitioner ID                                     | select_appointments() filters by practitioner ID.                                                              | Only appointments belonging to the requested practitioner are returned.                                                    | Test two practitioners and confirm their appointments are kept separate.               |
| QRY-02: Status filtering          | Appointment list and optional AppointmentStatus                          | Query filters by status when supplied; None includes all statuses.                                             | Correct status results or an empty list when there are no matches.                                                         | Test all three statuses and the default unfiltered result.                             |
| QRY-03: Deterministic sorting     | Matching appointments                                                    | appointment_sort_key() supplies date/time and appointment ID as the sorting key; query returns sorted results. | Ascending date/time order, with appointment ID breaking ties.                                                              | Test different dates and equal date/time values; confirm source order is unchanged.    |
| QRY-04: Service validation        | Practitioner ID and optional status                                      | Appointment service checks the practitioner and status before calling the query.                               | Unknown practitioner raises LookupError; invalid ID or status raises ValueError.                                           | Test known, unknown and invalid inputs separately.                                     |
| FP-01: Explicit inputs and purity | Appointment list, practitioner ID and optional status                    | Query uses only its arguments and returns a result without accessing global state or performing I/O.           | Same inputs produce the same result without changing application state.                                                    | Repeat calls and inspect the query implementation for hidden state, printing or input. |
| FP-02: No source mutation         | Original appointment list and its objects                                | Query creates and returns a new sorted list.                                                                   | Original list order and appointment fields remain unchanged.                                                               | Compare original list order and relevant fields before and after the query.            |
| FP-03: Named sorting key          | Appointment object                                                       | appointment_sort_key() returns (date_time, appointment_id) and is passed to sorting.                           | Consistent and reusable sorting behaviour.                                                                                 | Test the key directly and confirm the query uses it.                                   |
| UI-01: Normal menu workflow       | Patients, practitioners and appointments in one session                  | Console calls registration, booking, finding, cancellation and listing services.                               | Menu continues operating; cancellation remains visible in history and frees the scheduled slot.                            | Record a successful menu demonstration and its output.                                 |
| UI-02: Invalid menu inputs        | Unknown choices, IDs, duplicate records, invalid dates and statuses      | Console handles expected errors and returns to the menu.                                                       | Clear error messages; application continues without unintended state changes.                                              | Record invalid-input demonstrations followed by successful operations.                 |
| FR-01–09: Functional requirements | User-entered IDs, names, specialty, appointment details and menu choices | Console dispatches each supported operation to the appropriate service and displays the result.                | Registration, lookup, booking, cancellation and practitioner appointment listing work according to the existing contracts. | Use the relevant service and workflow tests, plus console evidence.                    |

Cover QRY-01–04, FP-01–03, UI-01–02 and relevant FR-01–09. Explain:
- empty versus unknown versus invalid:
  - Empty result: A known practitioner with no appointments, or no appointments matching a valid filter, should receive an empty list. This is a valid result, not an error.
  - Unknown practitioner: A correctly formatted practitioner ID that does not identify a registered practitioner should raise LookupError.
  - Invalid input: A blank or malformed ID, or a status that is not a valid AppointmentStatus, should raise ValueError.
- enum conversion: The console receives status as text. It should convert valid text to an AppointmentStatus value before calling the service. The service should accept an enum value or None, not interpret arbitrary strings as valid statuses. A blank status in the listing menu means no filter (None), so all statuses are included.
- actual object identity: When booking an appointment, the appointment must reference the actual registered Patient and Practitioner objects returned by the data store. The data store checks object identity when adding an appointment, protecting the relationships between stored records.
- error handling and unchanged state on rejection: Expected ValueError and LookupError exceptions should be handled by the console with understandable messages, allowing the user to return to the menu. The application should not silently ignore errors or use a broad exception handler to hide unexpected defects.
If a registration or booking is rejected because of an invalid ID, duplicate ID, unknown participant or practitioner conflict, the existing records must remain unchanged. A rejected booking must not reserve its appointment ID or leave a partial appointment in the store.

## C. Implementation and query verification

| Requirement / test ID | Code location                                    | Case and meaningful assertion                                                                             | Actual result                     | Evidence link                                                         |
|-----------------------|--------------------------------------------------|-----------------------------------------------------------------------------------------------------------|-----------------------------------|-----------------------------------------------------------------------|
| QRY-01                | smartcare/queries.py / tests/test_queries.py     | Appointments from two practitioners are separated correctly.                                              | Passed                            | ![stage09_C_veri.png](stage09_screenShots/stage09_C_veri.png)         |
| QRY-02                | smartcare/queries.py / tests/test_queries.py     | Test SCHEDULED, CANCELLED, COMPLETED and None (all statuses).                                             | Passed for all four filter cases. | ![stage09_C_veri.png](stage09_screenShots/stage09_C_veri.png)         |
| QRY-02                | tests/test_queries.py                            | No matching appointments returns an empty list.                                                           | Passed                            | ![stage09_C_veri.png](stage09_screenShots/stage09_C_veri.png)         |
| QRY-03                | smartcare/queries.py / tests/test_queries.py     | Appointments are sorted by date/time, then appointment ID for equal times.                                | Passed                            | ![stage09_C_veri.png](stage09_screenShots/stage09_C_veri.png)         |
| FP-01                 | smartcare/queries.py / tests/test_queries.py     | Repeated calls with identical inputs return consistent results.                                           | Passed                            | ![stage09_C_veri.png](stage09_screenShots/stage09_C_veri.png)         |
| FP-02                 | smartcare/queries.py / tests/test_queries.py     | Empty, already-sorted and unsorted inputs return fresh lists.                                             | Passed                            | ![stage09_C_veri_add.png](stage09_screenShots/stage09_C_veri_add.png) |
| FP-02                 | test/test_queries.py                             | Original list order and appointment fields remain unchanged.                                              | Passed                            | ![stage09_C_veri.png](stage09_screenShots/stage09_C_veri.png)         |
| FP-03                 | smartcare/queries.py / tests/test_queries.py     | Test appointment_sort_key() directly and confirm the query uses it.                                       | Passed                            | ![stage09_C_veri.png](stage09_screenShots/stage09_C_veri.png)         |
| QRY-04                | smartcare/queries.py / tests/test_queries.py     | Known practitioner with no appointments returns an empty list.                                            | Passed                            | ![stage09_C_veri.png](stage09_screenShots/stage09_C_veri.png)         |
| QRY-04                | smartcare/queries.py / tests/test_queries.py     | Unknown practitioner raises LookupError.                                                                  | Passed                            | ![stage09_C_veri.png](stage09_screenShots/stage09_C_veri.png)         |
| QRY-04                | smartcare/queries.py / tests/test_queries.py     | Blank practitioner ID and invalid status raise ValueError.                                                | Passed                            | ![stage09_C_veri.png](stage09_screenShots/stage09_C_veri.png)         |
| History               | tests/test_services.py / tests/test_workflows.py | Cancelled appointment remains findable and appears in all-status listing, but not scheduled-only listing. | Passed                            | ![stage09_C_veri.png](stage09_screenShots/stage09_C_veri.png)         |
One small post improvement made to FR-02 after initial implementation. Additional check is for empty-list freshness. Result was 66 passed in 0.06s.

Include practitioner isolation, every enum status/default all, equal-time ID tie-break, named-key reuse, repeated calls, empty/already-sorted fresh lists, unchanged source order/fields, known-empty/unknown/invalid service cases and retained history.

Purity explanation from code inspection, including absence of hidden state and I/O: The appointment query functions receive all required information through explicit parameters, including the appointment collection, practitioner ID and optional status. They do not access global variables, the data store or hidden application state. They do not prompt for input, print output or perform file or database operations. The appointment_sort_key() function returns a tuple containing the appointment date/time and appointment ID, providing a consistent tie-break when appointments have the same time. The select_appointments() function uses this named key with sorted() to return a new list rather than modifying the supplied list. It filters appointments by practitioner and, when a status is supplied, by the requested AppointmentStatus. A None status includes all statuses. The functions only read appointment properties and do not modify the original list or appointment objects. Repeated calls with the same inputs therefore produce consistent results.
What the tests do and do not establish: The tests establish that appointments are correctly separated by practitioner and filtered using each of the three appointment statuses, with None returning all statuses. They verify that appointments are ordered by date/time and that appointment ID is used to break equal-time ties. They also test appointment_sort_key() directly and confirm that the query reuses the named function. Repeated-call tests establish consistent results for identical inputs. Empty, already-sorted and unsorted input tests verify that new lists are returned, while source-list and appointment-field checks verify that the original data remains unchanged.
The service tests establish that a known practitioner with no matching appointments receives an empty list, an unknown practitioner raises LookupError, and blank practitioner IDs or invalid status values raise ValueError. The history and workflow tests establish that cancellation changes the appointment status without deleting the record: the cancelled appointment remains findable and appears in an all-status listing, but is excluded from a scheduled-only listing.
The tests provide evidence for the specific cases covered, but do not prove that the application is free from every possible defect. Code inspection is also needed to identify hidden dependencies, input/output operations and unintended side effects. Separate console testing is needed to establish that the interactive menu handles actual user input and recovers from expected errors.

## D. Integrated console and workflow evidence

| Scenario / acceptance ID     | Reproducible inputs / artefact                                                                                                                                                                                                                                                                                                                                                                         | Expected result                                                                                                                                                                                                                                                                                         | Observed result and state check                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Evidence link                                                            |
|------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------|
| UI-01 full menu workflow     | Interactive console session. Register patient P1 and practitioners D1 and D2. Find each registered record. Book A1 for P1 with D1 at 2026-10-01 09:00. Attempt another booking with D1 at the same time. Book A2 with D2 at the same time. Cancel A1, find A1, list D1 appointments with all statuses and then SCHEDULED only. Book A3 with D1 at the freed time. List D1 appointments again and exit. | Registration and retrieval succeed. The same-practitioner conflict is rejected. D2 can accept an appointment at the same time. A1 remains findable with CANCELLED status. All-status listing includes A1; scheduled-only listing excludes it. A3 can use the freed D1 time slot. Exit ends the session. | The interactive menu successfully completed the full workflow. Patient P1 and practitioners D1 and D2 were registered and retrieved. Appointment A1 was booked for D1. A second booking for D1 at the same time was rejected with a practitioner conflict error, while A2 for D2 at that time was accepted. A1 was cancelled and remained retrievable with status CANCELLED. Listing all statuses showed A1, while the scheduled-only listing returned no matching appointments. A3 was then successfully booked for D1 at the released time slot. The menu remained operational throughout the workflow. | [stage09_activities_and_evidence.md](stage09_activities_and_evidence.md) |
| UI-02 invalid-input recovery | Interactive console session. Try an unknown menu choice, blank and unknown IDs, duplicate registration, booking with unknown patient or practitioner, malformed and impossible dates, invalid listing status, unknown appointment and repeated cancellation. After each rejection, perform a valid operation.                                                                                          | Each invalid request produces a meaningful error without crashing or partially changing stored records. The menu remains available. A subsequent valid operation succeeds. Repeated cancellation is rejected without changing the already-cancelled appointment.                                        | The interactive menu handled invalid inputs without crashing. An unknown menu choice, blank patient ID, duplicate patient ID, unknown patient during booking, malformed date, impossible calendar date, invalid appointment status and unknown appointment lookup each produced an appropriate error message and returned control to the menu. A repeated cancellation of A1 was rejected because only scheduled appointments may be cancelled. The checks confirmed that expected input and lookup errors were handled at the console boundary.	                                                          | [stage09_activities_and_evidence.md](stage09_activities_and_evidence.md) |
| Automated service workflow   | project/tests/test_workflows.py; run python -m pytest -q from project/.                                                                                                                                                                                                                                                                                                                                | Booking, cancellation, retained history, scheduled-only filtering, freed-slot reuse, practitioner conflict rejection, different-practitioner bookings and rejection of unknown-patient booking are verified. Rejected bookings leave appointment records unchanged.                                     | Passed. Six workflow tests passed as part of the full suite: 66 passed in 0.06s.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | ![stage09_C_veri_add.png](stage09_screenShots/stage09_C_veri_add.png)    |

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.

## E. GitHub Copilot review and human decisions

Human design completed before AI: <!-- reference -->
Actual prompt/context supplied: <!-- paste or accessible reference -->
Actual response: <!-- accessible reference -->

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|
| | | | | | |

Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate: <!-- response -->

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail? <!-- response -->
2. Which Copilot suggestion did you reject as over-engineering, and why? <!-- response -->
3. How did you prove cancelled appointments remain retrievable and listable in the same session? <!-- response -->

## G. Ten formative answers

1. What makes select_appointments pure, and what side effect breaks purity? <!-- response -->
2. Which explicit inputs are needed, and why avoid a global store? <!-- response -->
3. How can a new list reuse Appointment objects safely? <!-- response -->
4. Why use a named key, and what breaks equal-time ties? <!-- response -->
5. How do default and explicit status filters differ? <!-- response -->
6. How do empty, unknown practitioner and invalid filter cases differ? <!-- response -->
7. Which console errors recover, and how is unchanged state checked? <!-- response -->
8. What is data integrity for registered participants, conflicts and history? <!-- response -->
9. What is Copilot's review role, and who verifies findings? <!-- response -->
10. How do pure functions and OOP responsibilities work together? <!-- response -->

## H. Review, completion and common handover

Issues and bounded branches: <!-- links -->
PR/diff and another-member human reviewer: <!-- actual links/name -->
Review responses and Copilot comparison: <!-- links -->
Integrated common Stage 9 SHA: <!-- complete -->
Full regression command, working directory, actual count/result and evidence: <!-- complete -->
README run instructions and scope/limitations: <!-- link -->
Unresolved issues and support/action: <!-- complete -->
UG common candidate / PG future branch plan: <!-- complete -->

- [ ] Query contracts, purity, new lists and named-key ordering verified.
- [ ] Service empty/unknown/invalid cases and cancellation history verified.
- [ ] Every console command and invalid-input recovery demonstrated.
- [ ] Query and workflow tests plus all previous tests pass; actual evidence linked.
- [ ] Human design, Copilot critique, review and integration recorded honestly.
- [ ] Reflections and ten formative responses completed.
- [ ] README updated; earlier code/tests/records preserved.
- [ ] Common SHA protected for UG Stage 12; PG Stage 10/11 work deferred until approved.

No persistence, rescheduling or assurance implementation is part of Stage 9. UG: 6→7→8→9→12. PG: 6→7→8→9→10→11→12. Mixed groups keep one repository and protect the common candidate.
