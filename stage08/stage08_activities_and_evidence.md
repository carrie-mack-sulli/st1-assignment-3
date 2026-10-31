# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: Group Exception 1
Members and UG/PG cohorts: Carrie Sullivan
Record owner / contribution links for each member: N/A - approved individual completion arrangement

Use concise results and accessible artefact links rather than copying entire logs. Keep human-first entries before consulting GitHub Copilot. Link shared evidence once; do not repeat it across sections. No entries below are specimen answers or claimed results.

## A. Tutorial activities

### A.1 Classify all five statements
For each, choose symptom, evidence or hypothesis/opinion, and explain your reason. These are discussion statements, not confirmed diagnoses.
- Appointment disappears after cancellation.
  - Response and reason: Symptom; because it is describing that an appointment has disappeared after it has been cancelled, but it is not known why.
- The data-store removal path is probably being called.
  - Response and reason: Hypothesis/opinion; because it sounds like an opinion based on something that has been observed.
- The failing test shows store.find_appointment('A1') returns None.
  - Response and reason: Evidence; because a specified output has been returned to state what the failure is.
- The service layer is badly designed.
  - Response and reason: Hypothesis/opinion; the statement is a judgement about the quality of the design. It doesn't identify a specific problem or identify improvements.
- Traceback points to smartcare/services.py line 42 in the example.
  - Response and reason: Evidence; a traceback shows the code location where an exception was raised, allowing investigation of an issue.
The example line number is illustrative; inspect the actual line in your run. The removal hypothesis must be tested against the current project, which has no public delete operation.

### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason: [complete]
- Record expected behaviour: When an appointment is cancelled, its status should change to CANCELLED. The appointment should remain in the data store, retain its history and still be retrievable. Cancelling it should not remove the appointment record.
- Observed behaviour: After an appointment is booked and cancelled, the cancellation operation returns the original appointment and its status changes to CANCELLED. However, a second call to appointment_service.find_appointment("A1") raises LookupError: Appointment not found instead of returning the retained appointment. A subsequent cancellation attempt also raises LookupError instead of ValueError, as expected
- Minimal reproduction: Register a patient and practitioner, book appointment A1, cancel it, then call appointment_service.find_appointment("A1"). The test test_cancel_appointment_changes_status_and_retains_same_object reproduces the problem. The traceback points to smartcare/services.py, line 140.
- A hypothesis and evidence to inspect: My initial hypothesis is that the data-store lookup method is not retrieving cancelled appointments. I will review find_appointment in smartcare/data_store.py, the service lookup method in smartcare/services.py, and the relevant test assertions to identify why the appointment cannot be retrieved. I will also check if the appointment remains in the underlying store rather than assuming it has been deleted.
- Requirement to justify the expectation: FR-06 and FR-07 require the cancellation behaviour and retention of appointment history. AC-05.2 protects that retained history. Therefore, cancellation should change the appointment's status without deleting the appointment record.
Keep the initial hypothesis even if later evidence disproves it.

### A.3 Test defect or product defect
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Response and reason: 
FR-07 requires appointment history to be retained. Cancellation should change the appointment status to CANCELLED while keeping the appointment record in the data store and available for retrieval. A test that expects deletion contradicts the requirement and would encourage incorrect behaviour.

A test expecting appointments with different practitioners at the same date and time to conflict also contradicts AC-04.2. That acceptance criterion allows different practitioners to have appointments at the same time. The test should be changed to expect the booking to succeed.

Tests must be checked against the requirements before treating a failure as a product defect. A failing test can contain an incorrect expectation.

### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Response and reason:
| Code smell | Small refactoring |
|---|---|
| Duplicate status strings | Use the existing appointment status enum consistently. |
| Direct collection manipulation | Use the existing SmartCareDataStore methods rather than accessing or changing its internal collection directly. |
| Printing inside the service | Remove presentation/debug output from the service; return results or raise the appropriate exception. |
| Repeated validation | Extract a small helper for genuinely repeated validation, keeping the same rules. |
| Four nested conditionals | Use guard clauses or extract small methods to make the decision paths easier to follow. |
| A long method doing several jobs | Extract focused methods for distinct responsibilities without introducing another architecture. |

Proposed changes:
| Proposed change | Classification | Reason |
|---|---|---|
| Rename appt to appointment | Refactoring | Improves readability without changing behaviour. |
| Extract a repeated conflict helper | Refactoring | Removes duplication while preserving the existing conflict rules. |
| Add rescheduling | Feature | Introduces new functionality that was not previously required. |
| Restore retained cancellation lookup | Repair | Corrects behaviour so cancelled appointments remain retrievable as required. |
| Replace a magic status string with the existing Enum | Refactoring | Uses the existing status representation without changing the intended state. |

Behaviour to remain unchanged:
Refactoring must not alter the required appointment rules or externally observable behaviour. In particular:
- Same-practitioner appointments at the same exact date and time must be rejected when the existing appointment is scheduled (AC-04.1).
- Different practitioners must still be allowed to have appointments at the same time (AC-04.2).
- Cancellation must change the status to CANCELLED, retain the appointment record and allow its history to be retrieved (FR-06, FR-07 and AC-05.2).
- Existing service and data-store responsibilities must remain.
The refactoring should make the code easier to understand and maintain, not add new rules or functionality.

### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason:
- Actual failure selected: test_cancel_appointment_changes_status_and_retains_same_object
- Exception/assertion: The test raises LookupError: Appointment not found.
- Expected behaviour: After cancellation, the original appointment should remain retrievable through find_appointment("A1").
- Observed behaviour: Cancellation returns the original appointment and changes its status to CANCELLED, but the subsequent service lookup raises LookupError.
- Test location: project/tests/test_services.py, line 157, where the test checks that the original appointment can still be retrieved.
- Application call path: The test calls appointment_service.find_appointment("A1"), which calls the data-store lookup method. The service raises LookupError when the data store returns no appointment.
- Supporting requirements: FR-06 and FR-07 require the cancellation behaviour and retention of appointment history. AC-05.2 protects that retained history.

Three plausible causes:
| Rank | Possible cause | Check to distinguish it |
|---|---|---|
| 1 | The data-store lookup method excludes appointments with CANCELLED status. | Inspect find_appointment in smartcare/data_store.py and check whether it filters by status. |
| 2 | The cancellation process removes the appointment from the data store. | Inspect the cancellation method and check whether the appointment remains in the store's underlying collection after cancellation. |
| 3 | The service lookup method incorrectly handles the result returned by the data store. | Inspect find_appointment in smartcare/services.py and compare its handling of existing, cancelled and missing appointments. |

Why a traceback alone does not establish the cause:
A traceback shows where an exception occurred and the sequence of calls that led to it. It does not identify the original cause. In this example, the LookupError showss that the service could not retrieve the appointment, but it does not prove whether the appointment was removed, filtered out by the data store or mishandled. Inspection of the relevant code and testing the competing hypotheses is required before deciding on a repair.

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason:
Failure shows a symptom, not necessarily its underlying cause. Making changes before investigating can lead to incorrect fixes, introduce new defects or change behaviour that is already correct.

The expected and observed behaviour should first be understood, then reproduce the failure, inspect the traceback and relevant code, and record possible causes. Each hypothesis should then be checked against evidence before making the smallest repair.

This ensures the actual cause is addressed, satisfies the requirements and does not introduce unnecessary changes.


Classification responses (1–5, each with reason): Please refer to A.1
Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: Please refer to A.2
Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks: Please refer to A.5

## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline: Ready
- Baseline test command / working directory / observed result / evidence: Stage 7: 39 passed
- Clean preparation SHA if a record-only commit followed Stage 7: 12d4b6a75318b63ea27ce42ba3654abd3dfa8f60
- Branch and preparer / how teammates obtained this branch: debug/stage8; Carrie Sullivan
- Downloaded tool version, source SHA256 and --check outcome: Version 1.1; SHA256 b4a1993e878c59a9df5e9055320702b2d318c5b6055bb1693a3afc25cd8fd375; check passed
- --apply and --verify output summaries / artefact references: Both passed; exactly two expected diagnostic failures verified. [stage08_screenShot_evidence.md](stage08_screenShots/stage08_screenShot_evidence.md)
- Bounded diff inspected and recovery location (not committed): Preparation changes inspected; recovery metadata in .stage8_faults, not committed
- Prepared faulty-state commit SHA: 15f46ee
- Preparation or recovery issues and resolution, if any: Initial full-path command failed due to spaces in the path; rerunning from the utility's directory succeeded
- Initial prepared full-suite command / result / key failures: 39 collected; 35 passed, 4 failed

## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: A booking for the same practitioner at the same exact datetime is accepted when it should be rejected.
- Expected behaviour and requirement: Reject a second scheduled appointment for the same practitioner and exact datetime, as required by FR-05 / AC-04.1. A different practitioner at that time must still be allowed under AC-04.2.
- Minimal synthetic reproduction steps:
Complete. The focused regression test attempts to book two appointments for the same practitioner at the same date and time. It reproduced the defect because the second booking did not raise ValueError.
- Meaningful failing test path/name and exact relevant failure: [stage08_screenShot_evidence.md](stage08_screenShots/stage08_screenShot_evidence.md)
  - Test: project/tests/test_regressions.py::test_f8_01_same_practitioner_conflict_and_different_practitioner_allowed
  - Command: python -m pytest -q tests/test_regressions.py
  - Working directory: project/
  - Observed: AssertionError because the second booking did not raise the expected ValueError. conflict_error was None.
  - Result: F8-01 reproduced.
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence:
The root cause is in SmartCareDataStore.has_practitioner_conflict() in project/smartcare/data_store.py.
The practitioner comparison uses != instead of ==. This means the conflict check matches appointments belonging to a different practitioner rather than the same practitioner. As a result, a second scheduled appointment for the same practitioner and exact datetime is not rejected.
The focused regression test reproduced this behaviour: the second booking did not raise the expected ValueError.
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: After cancellation, service lookup raises LookupError instead of returning the appointment.
- Expected behaviour and requirement: Cancellation changes the appointment status to CANCELLED, retains the appointment record and allows it to be retrieved, as required by FR-06/07, BR-07 and AC-05.2.
- Minimal synthetic reproduction steps:
Complete. The focused regression test books A1, cancels it, confirms the appointment is still listed with CANCELLED status, then checks lookup. The defect reproduced because data_store.find_appointment("A1") returned None.
- Meaningful failing test path/name and exact relevant failure: [stage08_screenShot_evidence.md](stage08_screenShots/stage08_screenShot_evidence.md)
  - Test: project/tests/test_regressions.py::test_f8_02_cancelled_appointment_remains_stored_and_retrievable
  - Command: python -m pytest -q tests/test_regressions.py
  - Working directory: project/
  - Observed: data_store.find_appointment("A1") returned None instead of the original appointment object. The appointment was still present in list_appointments() and had status CANCELLED.
  - Result: F8-02 reproduced.
- Human hypothesis and intended checks: see E, F8-02.
- Supported root cause and inspected code/runtime evidence:
The root cause is in SmartCareDataStore.find_appointment() in project/smartcare/data_store.py.
The lookup condition explicitly excludes appointments whose status value is "cancelled". However, list_appointments() returns all stored appointments, including cancelled ones.
The focused regression test confirmed that the appointment remained in the appointment list and had status CANCELLED, but find_appointment("A1") returned None instead of the original appointment object. The lookup filter therefore contradicts the retained-history requirement.
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.
[stage08_screenShot_evidence.md](stage08_screenShots/stage08_screenShot_evidence.md)

### F8-01 human entry
Likely cause and why plausible: The practitioner conflict check in SmartCareDataStore.has_practitioner_conflict() may be comparing practitioner IDs using the wrong equality condition. This is plausible because the focused regression test shows that a second appointment for the same practitioner and exact date/time is accepted instead of raising ValueError. A reversed comparison could cause the store to identify appointments for different practitioners as conflicts while missing appointments for the same practitioner.
Evidence intended to inspect / competing explanation / discriminating check: Inspect SmartCareDataStore.has_practitioner_conflict() to check the practitioner ID comparison, date/time comparison, scheduled-status condition and appointment exclusion condition. A competing explanation is that AppointmentService.book_appointment() does not call the conflict checker correctly, or does not act on its result. Inspect the booking method to confirm that it passes the registered practitioner's ID and requested date/time, and raises ValueError when the checker returns True. Also compare two cases: same practitioner at the same time should be rejected; different practitioners at the same time should be allowed. The service method does call the checker and handles a True result, which points towards the store predicate.
Member and saved sequence/time or commit showing this preceded consultation: Carrie Sullivan [insert commit ref]

### F8-02 human entry
Likely cause and why plausible: The appointment lookup in SmartCareDataStore.find_appointment() may be filtering out appointments with CANCELLED status. This is plausible because the focused regression test confirms that cancellation changes the appointment's status and that the appointment remains in the list, but an individual lookup returns None. This suggests the appointment may still be stored but excluded by the lookup condition.
Evidence intended to inspect / competing explanation / discriminating check: Inspect SmartCareDataStore.find_appointment() to determine whether its lookup condition excludes cancelled appointments. A competing explanation is that cancellation removes the appointment from the underlying store, or that AppointmentService.find_appointment() mishandles a result returned by the store. Compare the appointment list and direct store lookup after cancellation, then inspect the service method to confirm how it handles a None result. Also inspect AppointmentService.cancel_appointment() to confirm that it uses the domain cancellation method and does not remove the appointment. The service methods retain the appointment object and delegate lookup to the store, which points towards the store lookup condition.
Member and saved sequence/time or commit showing this preceded consultation: Carrie Sullivan [insert commit ref]

Service-layer inspection:
Inspection of AppointmentService.book_appointment() confirmed that it calls SmartCareDataStore.has_practitioner_conflict() and raises ValueError when a conflict is reported. This indicates that F8-01 is likely in the data-store conflict predicate rather than the service call.

Inspection of AppointmentService.cancel_appointment() confirmed that it calls find_appointment(), invokes the domain cancellation method and returns the appointment object without removing it. AppointmentService.find_appointment() raises LookupError when the store returns None. This indicates that F8-02 is likely in the data-store lookup condition rather than the service layer.

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review
Actual prompt / output reference and member: [complete]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

### F8-02 Copilot review
Actual prompt / output reference and member: [complete]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | [complete] | [complete] | [complete] |
| F8-01 after repair | [complete] | [complete] | [complete] |
| F8-02 before repair | [complete] | [complete] | [complete] |
| F8-02 after repair | [complete] | [complete] | [complete] |
| Full suite after both repairs, before refactor | [complete] | [complete] | [complete] |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour: [complete]
Unrelated failures investigated / resolution: [complete or not applicable with reason]

## H. Refactoring decision and before/after verification

Smell and exact location: [complete]
Small proposed structural change / why justified: [complete before editing]
External behaviour to preserve / relevant tests: [complete]
Before result: see G, full passing suite.
Actual change / diff / separate refactor SHA: [complete]
Focused and full after-refactor commands / working directory / results / evidence: [complete]
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: [complete]

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: [complete]
Branch / prepared, repair and refactor checkpoints: [link B/C/D/H]
PR link and another member's reviewer identity: [complete]
Key human feedback, difference from Copilot findings and response/outcome: [complete]
Actual review approval / merge evidence: [complete]
Integrated code SHA and team pull/retest command / working directory / result: [complete]
Evidence-only later SHA / explanation if different: [complete or not applicable]
Each member's substantive contribution and artefact: [complete]

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? [complete; report honestly if none and discuss the least-supported real suggestion]
2. What evidence changed your group's view? [complete]
3. How did regression tests protect the refactoring? [complete]

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: [complete]

2. Where should expected behaviour come from during debugging?

Response: [complete]

3. What is a debugging hypothesis?

Response: [complete]

4. What is a regression test and why is it retained?

Response: [complete]

5. What is meant by root cause?

Response: [complete]

6. What is refactoring?

Response: [complete]

7. What is a swallowed exception?

Response: [complete]

8. What is a code smell?

Response: [complete]

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: [complete]

10. What is the Stage 8 engineering rule?

Response: [complete]

## L. Completion and handover

- [ ] Existing project, earlier tests and stage records preserved.
- [ ] Passing Stage 7 SHA and safe preparation details recorded.
- [ ] Both defects reproduced with meaningful failing tests.
- [ ] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [ ] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [ ] One genuine refactor verified under passing before/after tests.
- [ ] Human PR review, feedback resolution and integrated retest recorded.
- [ ] Tutorial, three reflections and ten formative responses complete.
- [ ] Local recovery metadata excluded from submitted source.
- [ ] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: [complete]
Unresolved issues or incomplete checks / owner / next action: [complete]
Handover note: [complete]
