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

Response and reason:
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
- Smallest justified fix / diff / why other behaviour is preserved: The smallest justified fix was to correct the practitioner ID comparison in SmartCareDataStore.has_practitioner_conflict(). The original condition used !=, which incorrectly identified appointments for different practitioners as conflicts while failing to detect appointments for the same practitioner. I changed the comparison to ==.
This preserves the existing conflict-checking structure, date/time comparison, scheduled-status condition and appointment exclusion condition. It ensures that a second scheduled appointment for the same practitioner at the same date and time is rejected, while appointments for different practitioners at the same time remain allowed. No service or domain behaviour needed to be changed.
- Repair SHA / focused verification result: Repair commit: cc00eb4 — Repair Stage 8 appointment defects.
The focused regression tests were run using python -m pytest -v tests/test_regressions.py from project/. After both repairs, the result was 2 passed in 0.03s.
The affected existing tests were also run alongside the regression tests. All four focused tests passed, confirming that same-practitioner conflicts were rejected and different practitioners could still be booked at the same time.

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
- Smallest justified fix / diff / why other behaviour is preserved: The smallest justified fix was to remove the cancelled-status exclusion from SmartCareDataStore.find_appointment(). Previously, the lookup returned an appointment only when its ID matched and its status was not cancelled. I changed the condition so that it matches the appointment ID regardless of status.
This preserves the existing appointment record and allows cancelled appointments to remain retrievable for history. It does not change the cancellation operation, appointment status, booking rules or behaviour for unknown appointment IDs. The repair keeps the existing data-store and service boundaries.
- Repair SHA / focused verification result: Repair commit: cc00eb4 — Repair Stage 8 appointment defects.
The focused regression tests were run using python -m pytest -v tests/test_regressions.py from project/. After both repairs, the result was 2 passed in 0.03s.
The affected existing tests were also run alongside the regression tests. All four focused tests passed, confirming that cancelled appointments remained retrievable and that cancellation did not prevent a replacement booking.

## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.
[stage08_screenShot_evidence.md](stage08_screenShots/stage08_screenShot_evidence.md)

### F8-01 human entry
Likely cause and why plausible: The practitioner conflict check in SmartCareDataStore.has_practitioner_conflict() may be comparing practitioner IDs using the wrong equality condition. This is plausible because the focused regression test shows that a second appointment for the same practitioner and exact date/time is accepted instead of raising ValueError. A reversed comparison could cause the store to identify appointments for different practitioners as conflicts while missing appointments for the same practitioner.
Evidence intended to inspect / competing explanation / discriminating check: Inspect SmartCareDataStore.has_practitioner_conflict() to check the practitioner ID comparison, date/time comparison, scheduled-status condition and appointment exclusion condition. A competing explanation is that AppointmentService.book_appointment() does not call the conflict checker correctly, or does not act on its result. Inspect the booking method to confirm that it passes the registered practitioner's ID and requested date/time, and raises ValueError when the checker returns True. Also compare two cases: same practitioner at the same time should be rejected; different practitioners at the same time should be allowed. The service method does call the checker and handles a True result, which points towards the store predicate.
Member and saved sequence/time or commit showing this preceded consultation: Carrie Sullivan - Commit SHA 9e143d1

### F8-02 human entry
Likely cause and why plausible: The appointment lookup in SmartCareDataStore.find_appointment() may be filtering out appointments with CANCELLED status. This is plausible because the focused regression test confirms that cancellation changes the appointment's status and that the appointment remains in the list, but an individual lookup returns None. This suggests the appointment may still be stored but excluded by the lookup condition.
Evidence intended to inspect / competing explanation / discriminating check: Inspect SmartCareDataStore.find_appointment() to determine whether its lookup condition excludes cancelled appointments. A competing explanation is that cancellation removes the appointment from the underlying store, or that AppointmentService.find_appointment() mishandles a result returned by the store. Compare the appointment list and direct store lookup after cancellation, then inspect the service method to confirm how it handles a None result. Also inspect AppointmentService.cancel_appointment() to confirm that it uses the domain cancellation method and does not remove the appointment. The service methods retain the appointment object and delegate lookup to the store, which points towards the store lookup condition.
Member and saved sequence/time or commit showing this preceded consultation: Carrie Sullivan - Commit SHA 9e143d1

Service-layer inspection:
Inspection of AppointmentService.book_appointment() confirmed that it calls SmartCareDataStore.has_practitioner_conflict() and raises ValueError when a conflict is reported. This indicates that F8-01 is likely in the data-store conflict predicate rather than the service call.

Inspection of AppointmentService.cancel_appointment() confirmed that it calls find_appointment(), invokes the domain cancellation method and returns the appointment object without removing it. AppointmentService.find_appointment() raises LookupError when the store returns None. This indicates that F8-02 is likely in the data-store lookup condition rather than the service layer.

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.
First prompt:
Hi, I've just merged Debug/stage08 and human-first hypothesis evidence. For the bugs can you please rank the three most likely causes. For each, identify
 the evidence I should inspect to distinguish it from
 the other possible causes.
Do not rewrite the entire application.
Do not invent requirements.
Treat all suggested explanations as hypotheses.
Second prompt:
Can you rank the 3 most likely cause for each bug
Third prompt:
Do you have any observable evidence for each of the bugs? Are the observable evidence numbers mapped to each of the causes. If not can you please corrolate cause to observable evidence.

### F8-01 Copilot review
Actual prompt / output reference and member: Please refer to F
1. Conflict check is not comparing exact datetime / Check the utility output, reproduction notes and failing test values to confirm the conflict occurs at exactly the same datetime, with no seconds or timezone differences. / E2 — Human‑first notes show the system allowed a second booking at the same datetime, E1 — Debugging utility confirms conflict detection is faulty, E3 — Reproducible symptom signature / wrong / reject with reason: The reproduction uses the exact same datetime for both appointments, and the data-store comparison uses equality. The available evidence does not support a datetime mismatch as the cause.
2. Conflict check is filtering by wrong appointment state / Check the utility output, reproduction notes and failing test status to confirm whether cancelled appointments incorrectly trigger conflicts or scheduled appointments fail to trigger them. / E1 — Debugging utility confirms conflict detection defect, E2 — Human‑first notes may show conflict detected when appointment was CANCELLED, E3 — Reproducible symptom signature / wrong / reject with reason: Inspection confirms that the scheduled-status condition is appropriate because only scheduled appointments should create conflicts. The defect is in the practitioner ID comparison, not the appointment-state filter.
3. Practitioner ID mismatch or incorrect filtering / Check the failing test's practitioner IDs, utility logs and reproduction notes to determine whether inconsistent ID formatting causes incorrect conflict detection. / E1 — Debugging utility confirms conflict detection defect, E3 — Reproducible symptom signature, E2 (conditionally) — If human‑first notes show conflict missed only when multiple practitioners exist / partly correct / modify with reason: The practitioner ID comparison is responsible for the defect, but there is no evidence of inconsistent ID formatting. Inspection of SmartCareDataStore.has_practitioner_conflict() confirms that the comparison uses != instead of ==, causing the conflict check to identify different practitioners rather than the same practitioner.
Final human conclusion and comparison with initial hypothesis: My human-first hypothesis was that the practitioner conflict detection method was incorrectly comparing practitioner IDs. Copilot identified several possible explanations; however, comparing these with the regression test results and source code, I rejected the datetime and appointment-state explanations. I modified Copilot's third suggestion because the evidence did not indicate inconsistent ID formatting. The actual cause was confirmed as an incorrect comparison operator (!= instead of ==) in SmartCareDataStore.has_practitioner_conflict(). My original hypothesis was supported, and the smallest justified repair is to correct the practitioner ID comparison while preserving the existing datetime and scheduled-status conditions.

### F8-02 Copilot review
Actual prompt / output reference and member: Please refer to F
1. Cancelled appointment history lookup / Check the failing test output, human-first notes and utility signature to confirm whether cancelled appointments are missing from lookup results. / E2 — Human‑first notes: “Cancelled appointment not found”, E1 — Debugging utility confirms missing cancelled appointments, E3 — Reproducible symptom signature / correct / accept with reason: The regression test confirms that the cancelled appointment remains in the appointment list but cannot be retrieved through find_appointment("A1"). The human-first notes and debugging utility evidence support the missing cancelled-appointment lookup symptom.
2. Lookup filters out CANCELLED appointments / Check the failing test output, utility logs and human-first notes to determine whether lookup returns scheduled appointments but incorrectly excludes cancelled ones. / E1 — Debugging utility confirms lookup defect, E2 — Human‑first notes: lookup returns only scheduled appointments, E3 — Reproducible symptom signature / correct / accept with reason: Inspection of SmartCareDataStore.find_appointment() confirms that its lookup condition excludes appointments with CANCELLED status. The regression test also confirms that the appointment remains in the list but individual lookup returns None. This supports the hypothesis that cancelled appointments are incorrectly filtered out.
3. Cancellation transition not applied correctly / Check the failing test output, utility logs and reproduction notes to confirm whether cancellation correctly changes the appointment status to CANCELLED or leaves it SCHEDULED. / E2 — Human‑first notes: cancellation appears to succeed but lookup returns SCHEDULED, E1 — Debugging utility confirms defect, E3 — Reproducible symptom signature / wrong / reject with reason: The regression test confirms that cancellation successfully changes the appointment status to CANCELLED and that the appointment remains stored. The cancellation method uses the domain cancellation method correctly. The failure occurs because the data-store lookup excludes cancelled appointments, not because the cancellation transition is incorrect.
Final human conclusion and comparison with initial hypothesis: My human-first hypothesis was that cancelled appointments were being excluded from the data-store lookup even though they remained stored. Copilot identified the missing cancelled-appointment lookup symptom and correctly identified the filtering condition as a likely cause. I accepted these two suggestions because they were supported by the regression test results and source-code inspection. I rejected the suggestion that the cancellation transition was not being applied correctly because the test confirmed that the appointment status changed to CANCELLED and the same appointment object was retained. Inspection of SmartCareDataStore.find_appointment() confirmed that cancelled appointments were explicitly excluded by its lookup condition. My original hypothesis was supported, and the smallest justified repair is to remove the cancelled-status exclusion while preserving appointment ID validation and the existing service-layer behaviour.

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | 15f46ee | python -m pytest -v tests/test_regressions.py from project/ | Failed: same-practitioner booking was incorrectly accepted; tests/test_regressions.py, line 70 |
| F8-01 after repair | SmartCareDataStore.has_practitioner_conflict(): changed practitioner ID comparison from != to == | python -m pytest -v tests/test_regressions.py from project/ | PASSED; F8-01 passed. F8-02 remained failed. Output: 1 passed, 1 failed in 0.06s. |
| F8-02 before repair | 15f46ee | python -m pytest -v tests/test_regressions.py from project/ | Failed: cancelled appointment remained in the store but find_appointment("A1") returned None; tests/test_regressions.py, line 113 |
| F8-02 after repair | SmartCareDataStore.find_appointment(): removed the cancelled-status exclusion from the matching condition | python -m pytest -v tests/test_regressions.py from project/ | PASSED; both regression tests passed. Output: 2 passed in 0.03s. |
| Full suite after both repairs, before refactor | data_store.py: changed practitioner comparison from != to ==; removed cancelled-status exclusion from find_appointment() | python -m pytest -v from project/ | 41 passed, 0 failed in 0.06s. Full output from this test run. |
[stage08_screenShot_evidence.md](stage08_screenShots/stage08_screenShot_evidence.md)

Explain how the assertions detect each relevant incorrect result and protect previous behaviour: The F8-01 regression asserts that a second appointment for the same practitioner and datetime raises ValueError, while a different practitioner can book the same datetime. The F8-02 regression asserts that cancellation changes the appointment status to CANCELLED while retaining the same appointment object in the data store and making it retrievable. Together, these assertions protect conflict handling, different-practitioner booking, cancellation status and appointment history.
Unrelated failures investigated / resolution: Not applicable. The four failures in the prepared Stage 8 suite were attributable to the two identified defects. Both have been addressed, and the full suite now passes.

## H. Refactoring decision and before/after verification

Smell and exact location: Magic string used for appointment status comparison in project/smartcare/data_store.py, inside SmartCareDataStore.has_practitioner_conflict().
Small proposed structural change / why justified: Replace appointment.status.value == "scheduled" with appointment.status is AppointmentStatus.SCHEDULED. The existing AppointmentStatus enum is already imported and defines the scheduled state. Using the enum directly avoids repeating a string literal and makes the comparison consistent with the domain model. ![stage08_H_bf.png](stage08_screenShots/stage08_H_bf.png)
External behaviour to preserve / relevant tests:
- Same practitioner and same datetime must be treated as a conflict.
- Different practitioners may have appointments at the same datetime.
- Only scheduled appointments block a booking.
- The excluded appointment ID must still be ignored.
- Appointment records, statuses and object identities must remain unchanged.
- Relevant tests:
  - tests/test_regressions.py
  - tests/test_starter.py::test_conflict_rule_and_different_practitioner
  - tests/test_services.py::test_cancelled_appointment_does_not_block_slot
Before result: see G, full passing suite.
Actual change / diff / separate refactor SHA:
  - Actual change: In project/smartcare/data_store.py, inside SmartCareDataStore.has_practitioner_conflict(), replaced appointment.status.value == "scheduled" with appointment.status is AppointmentStatus.SCHEDULED
  - Diff: One-line change to preserve bahviour. The method still checks the practitioner ID, appointment datetime, excluded appointment ID and scheduled status.
  - Separate refactor SHA: 5785856 — Refactor appointment status comparison.
Focused and full after-refactor commands / working directory / results / evidence:
  - Focused command: python -m pytest -v tests/test_regressions.py tests/test_starter.py::test_conflict_rule_and_different_practitioner tests/test_services.py::test_cancelled_appointment_does_not_block_slot
  - Full-after suite command: python -m pytest -v
  - Working directory: project/
  - Results: 41 passed in 0.08s, 0 failed.
  - Evidence: ![stage08_H_af1.png](stage08_screenShots/stage08_H_af1.png) and ![stage08_H_af2.png](stage08_screenShots/stage08_H_af2.png)
Result — accepted / behaviour-preservation conclusion: No regression was detected by the focused or full test suites.

## I. Git, human review and integration

Issues for both defects / refactor scope and owners:
- F8-01: Same-practitioner appointment conflict was not detected because the practitioner ID comparison used != instead of ==. Repair owner: individual student.
- F8-02: Cancelled appointments were retained in the data store but excluded from find_appointment(). Repair owner: individual student.
- Refactor: Replaced the scheduled-status string comparison with AppointmentStatus.SCHEDULED in SmartCareDataStore.has_practitioner_conflict(). Refactor owner: individual student.
Branch / prepared, repair and refactor checkpoints:
- Branch: debug/stage8
- Prepared faulty-state checkpoint: 15f46ee — Prepare Stage08 debugging.
- Preparation record-only checkpoint: 12d4b6a — .gitignore preparation.
- Stage 8 documentation checkpoint: 9e143d1 — documentation and evidence.
- Repair checkpoint: cc00eb4 — Repair Stage 8 appointment defects.
- Refactor checkpoint: 5785856 — Refactor appointment status comparison.
PR links and another member's reviewer identity:
Before repair and refactor:
- Source branch: debug/stage8
- PR scope: Stage 8 debugging work, including the human-first hypothesis evidence for Activity 8.
- PR/merge link: https://github.com/carrie-mack-sulli/st1-assignment-3/pull/8
- Reviewer: N/A - approved individual completion arrangement; this activity requires another group member.
Key human feedback, difference from Copilot findings and response/outcome: N/A - approved individual completion arrangement; this activity requires another group member.
Actual review approval / merge evidence: PR #8 was merged into main for the earlier Stage 8 investigation and human-first hypothesis work. N/A - approved individual completion arrangement; this activity requires another group member.
Integrated code SHA and team pull/retest command / working directory / result:
- Integrated team code SHA: 237e9bce031d9f58b354da6586c57c75e5738c4e
- Local full-suite verification: python -m pytest -v
- Working directory: project/
- Result after refactor: 41 passed in 0.06s.
Evidence-only later SHA / explanation if different: Not applicable
Each member's substantive contribution and artefact:
- Carrie Sullivan: Prepared and ran the Stage 8 debugging utility, documented the two defects, inspected the relevant service and data-store code, wrote regression tests, repaired both defects, performed the enum refactor, ran focused and full test suites, and prepared the Stage 8 evidence record.
- Artefacts: project/smartcare/data_store.py, project/tests/test_regressions.py, Stage 8 activity and evidence record, and the relevant Git checkpoints.

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? Copilot suggested that the F8-01 conflict problem may be datetime exactness or appointment-status filtering. However, available evidence did not determine either as the cause. Inspection of SmartCareDataStore.has_practitioner_conflict() showed that the practitioner ID comparison used != instead of ==. The regression test confirmed that correcting this comparison resolved the conflict defect. This meant, the datetime and status suggestions were not adopted because they were unsupported.
2. What evidence changed your group's view? The most useful evidence was recreating the failures, investigating the relevant data-store methods and writing focused regression tests.
For F8-01, the test demonstrated that a second appointment for the same practitioner and datetime was incorrectly accepted, while the source inspection identified the reversed practitioner ID comparison.
For F8-02, inspection showed that cancellation correctly changed the appointment status and retained the object in the store. However, find_appointment() excluded cancelled appointments from its lookup. The regression test confirmed that the appointment remained stored but could not be retrieved. This changed the diagnosis from possible record deletion or failed cancellation to an incorrect lookup filter.
After the two repairs, both regression tests passed, and the full suite reported 41 passed.
3. How did regression tests protect the refactoring? Regression tests established expected behaviour before the refactoring and provided checks afterwards. They protected the same-practitioner conflict rule, allowed bookings for different practitioners at the same datetime, and ensured cancelled appointments remained stored and retrievable.
The refactoring only replaced a string-based scheduled-status comparison with the existing AppointmentStatus.SCHEDULED enum member. The four focused tests passed after the change, followed by the full suite with 41 passed and no failures. Comparing the pre-refactor and post-refactor results showed that the tested behaviour remained unchanged.

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: An engineer should first reproduce the problem, examine the error message and traceback, and inspect the relevant code and tests. They should identify the expected and actual behaviour, investigate the likely cause, and gather evidence for a diagnosis. They should then choose the smallest justified change, add or update regression tests, and verify that the fix resolves the failure without causing new problems.

2. Where should expected behaviour come from during debugging?

Response: Documented requirements, acceptance criteria, specifications and agreed business rules, determine expected behaviour. Existing tests and design documentation can also clarify intended behaviour. Engineers should use these sources as evidence rather than assuming that the current code or a failing test is correct.

3. What is a debugging hypothesis?

Response: A debugging hypothesis is a possible explanation for why a failure is occurring. It is based on available evidence and can be tested through further investigation, such as reproducing the problem, inspecting the code or running targeted tests. A hypothesis is not a confirmed cause until evidence supports it.

4. What is a regression test and why is it retained?

Response: A regression test checks previously fixed or working functionality to ensure it continues to behave as expected after code changes. It is retained so that future changes do not reintroduce an existing defect or break established behaviour.

5. What is meant by root cause?

Response: The underlying problem for causing a defect or failure. It is the specific problem in the code or system that produces the observed symptoms.

6. What is refactoring?

Response: It's the process of improving the internal structure, readability or maintainability of existing code without changing its external behaviour.

7. What is a swallowed exception?

Response: A swallowed exception occurs when a program catches an error but does not properly handle it, report it or pass it on. This can hide underlying problems and make debugging difficult because the program may continue running without showing that something is wrong.

8. What is a code smell?

Response: A code smell is a sign that code isn't quite right and could be improved. It may be difficult to read, understand or maintain. Examples include repeated code, long methods and complicated conditions.

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: GitHub Copilot's debugging suggestions should be treated as possible explanations, not confirmed facts. Engineers should check them against the code, requirements and test results before deciding whether to accept or reject them.

10. What is the Stage 8 engineering rule?

Response: Investigate before changing code.

## L. Completion and handover

- [x] Existing project, earlier tests and stage records preserved.
- [x] Passing Stage 7 SHA and safe preparation details recorded.
- [x] Both defects reproduced with meaningful failing tests.
- [x] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [x] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [x] One genuine refactor verified under passing before/after tests.
- [x] Human PR review, feedback resolution and integrated retest recorded.
- [x] Tutorial, three reflections and ten formative responses complete.
- [x] Local recovery metadata excluded from submitted source.
- [x] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: 237e9bce031d9f58b354da6586c57c75e5738c4e.
Unresolved issues or incomplete checks / owner / next action: No known unresolved Stage 8 defects. The full test suite passed with 41 tests and no failures. Independent peer review was not applicable under the approved individual completion arrangement. Carrie Sullivan: proceed to Stage 9 using the integrated main branch.
Handover note: Stage 8 is complete. Both appointment defects were reproduced, investigated and repaired. Focused regression tests and the full test suite passed. A small refactor was completed and verified without changing external behaviour. PR #9 was merged into main, and the integrated code passed all 41 tests. The Stage 8 activity record and screenshot evidence have been committed. The project is ready for Stage 9 using the integrated main branch.
