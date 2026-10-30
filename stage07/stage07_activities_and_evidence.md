# Stage 7 Testing and Verification Record

Group/tutorial: Group Exception 1  Members/cohorts: Carrie Sullivan
Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.
Use the same project/. Link actual evidence; keep responses concise. Blank fields are for your group. Copy rows only as needed.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage07/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions.

## A Tutorial Activities

### Activity 1 Requirement to test

For each requirement, propose one positive test, one negative test and the key assertion.

| Requirement                         | Positive test                                                                                                                                   | Negative test                                                                                                                                                                                    | Key assertion                                                                                                                                                                                                            |
|-------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FR-01 Register patient              | Register a patient with a unique ID and valid details. Verify the patient is stored and can be retrieved with details intact.                   | Try to register a patient using an ID that already exists. Expect ValueError and verify the original patient record has not been changed.                                                        | Positive: data_store.find_patient(patient_id) is patient (or verify the stored fields). Negative: pytest.raises(ValueError) and the original record is not changed.                                                      |
| FR-05 Prevent practitioner conflict | Book two appointments at the same time with two different registered practitioners. Both appointments should be stored with ‘Scheduled’ status. | Try to book a second appointment for the same practitioner at the same date/time as an existing ‘Scheduled’ appointment. Expect ValueError and verify the original booking has not been changed. | Positive: both bookings are retrievable and ‘Scheduled’. Negative: pytest.raises(ValueError) and the original appointment is not changed.                                                                                |
| FR-06 Cancel appointment            | Cancel an existing ‘Scheduled’ appointment. Verify its status changes to ‘Cancelled’.                                                           | Try to cancel the same appointment a second time. Expect ValueError and verify its status stays as ‘Cancelled’.                                                                                  | Positive: appointment.status == AppointmentStatus.CANCELLED. Negative: pytest.raises(ValueError) and the status remains ‘Cancelled’.                                                                                     |
| FR-07 Retain cancelled history      | Cancel an appointment, then retrieve it using its ID from the shared data store. Verify it is still available with its cancelled status.        | Try to cancel an already-cancelled appointment again, then verify the appointment remains retrievable in the cancelled history.                                                                  | Positive: data_store.find_appointment(appointment_id) is appointment and its status is ‘Cancelled’. Negative: repeated cancellation raises ValueError, while the original appointment remains retrievable and cancelled. |

### Activity 2 Strong or weak assertion

For each, select Strong for stated behaviour or Weak/unclear and explain why. State the behaviour and limits.

`assert True`
Judgement: Weak/unclear  Why: This assertion always passes, whether or not the behaviour is correct. This could be problematic.

`assert appointment is not None`
Judgement: Weak/unclear  Why: This assertion assumes that appointment refers to an object and not none; it does not prove the appointment has the correct information of ID, patient and practitioner, date/time, status or state.

`assert appointment.status == AppointmentStatus.CANCELLED`
Judgement: Strong for stated behaviour  Why: This assertion shows appointment status is CANCELLED. However, it does not prove that the appointment is still retrievable from the data store.

`assert len(results) > 0`
Judgement: Weak/unclear  Why: This assertion shows results are collected for an item, however which item is unknown. Patient, practitioner or appointment information is not determined, if the results are correct or if required records are returned.

`assert data_store.find_appointment('A1') is appointment`
Judgement: Strong for stated behaviour  Why: This assertion demonstrates that looking up appointment ID of A1 retrieves the required information. This supports requirement of retrieving appointments, however does not provide or confirm status.

### Activity 3 Boundary thinking

Design boundary or edge cases for blank identifiers, whitespace-only names, same-time practitioner bookings, cancelled appointments and invalid status transitions.
For each input/state, expected result and supporting contract: 
| Boundary / edge case | Input or state | Expected result | Contract supporting the expectation |
|---|---|---|---|
| 1. Identify blank or whitespace-only | Patient or appointment ID is "" or "   ". | Raise ValueError; do not store an invalid record. | Required identifiers must be non-blank. Whitespace validation is a revision 2 contract, and is not AC-01.2. |
| 2. Whitespace-only name	 | A required patient or practitioner name is "   ". | Raise ValueError; invalid data is rejected. | Required fields must contain valid, non-blank values. |
| 3. Practitioner booking at the same time | Try booking the same practitioner at 10:00 when they already have a SCHEDULED appointment at that time. | Raise ValueError; original appointment remains the same. A different practitioner at 10:00 is allowed. | FR-05 / AC-04.1 and AC-04.2: same-practitioner conflicts are rejected, but different practitioners may share the same time. |
| 4. Cancelled appointment and rebooking | Cancel a SCHEDULED appointment, retrieve it by ID, then book the practitioner at the same time with a new appointment ID. | The cancelled appointment remains retrievable with status CANCELLED, and the new booking is allowed if otherwise valid. | FR-06 / FR-07; AC-05.1 / AC-05.2: cancellation changes status and retains history; the cancelled booking no longer occupies the slot. |
| 5. Invalid cancellation transition | Try to cancel an appointment already CANCELLED, or one with status COMPLETED. | Raise ValueError; the appointment's status remains the same. | AC-05.3 covers repeated cancellation; the cancellation guard rejects invalid status transitions. |

### Activity 4 Critique GitHub Copilot tests

GitHub Copilot generates five tests, all of which pass. Two only assert that objects are not None, one asserts True, and two assume SMS notifications exist. Identify what is wrong and rewrite the test intentions.

| Candidate                          | What is wrong                                                                                                           | Rewritten test intention                                                                                                                                               |
|------------------------------------|-------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1. Asserts an object is not None   | Weak. It only proves an object was returned or created, not that it contains the expected data or was stored correctly.	 | Register a patient with valid, unique details and verify the patient can be retrieved from the shared data store with the correct ID and details.                      |
| 2. Asserts an object is not None   | Weak. Object may exist but have wrong appointment details, status, or participants.                                     | Book an appointment for registered participants and verify the stored appointment has the expected ID, patient, practitioner, date/time and SCHEDULED status.          |
| 3. Asserts True	                    | Weak/unclear. It always passes and does not test application behaviour.                                                 | Try to book the same practitioner at the exact time as an existing SCHEDULED appointment; check that ValueError is raised and the original appointment is not changed. |
| 4. Assumes SMS notifications exist | Unsupported assumption. SMS notifications are not part of the stated application contract.                              | Cancel a SCHEDULED appointment and verify its status becomes CANCELLED and it continues to be retrievable by ID.                                                       |
| 5. Assumes SMS notifications exist | Unsupported assumption. It tests an unrequired notification feature instead of an established requirement.              | Try to cancel an already CANCELLED appointment and verify ValueError is raised and its status remains CANCELLED.                                                       |

### Tutorial exit question

Why can 100% code coverage coexist with poor software verification?
This can occur because code coverage looks at executed code and not if tests correctly verify behaviour.

## B Requirement to Test Traceability Matrix

Assign TEST IDs before implementation or generation. Use canonical AC IDs with their actual meaning; quote supporting revision 2 contracts when no canonical AC is assigned. Blank-ID validation is not AC-01.2. Identify supplied versus student-authored evidence.

| Requirement                       | Acceptance criterion                                                   | Test ID  | Test type | Test name / location                                                 | Expected behaviour                                                                                                                                           | Result / observed status                                                                                 | Supplied or student-authored                 |
|-----------------------------------|------------------------------------------------------------------------|----------|-----------|----------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|----------------------------------------------|
| FR-01 — Patient registration      | AC-01.1                                                                | TEST -01 | Domain    | Patient required-field validation — test_domain.py                   | Valid patient details and an unused ID produce a valid patient object. This is partial domain evidence only; it does not prove storage through registration. | Partially run. Student authored portion to be run                                                        | Partial supplied / partial student authored  |
| FR-01 — Patient registration      | AC-01.1	                                                                | TEST -02 | Service   | Register and store patient — test_services.py                        | Register a valid patient with an unused ID and verify the patient is stored and retrievable with the expected details.                                       | Planned - not yet run                                                                                    | Student authored                             |
| FR-01 — Patient registration      | AC-01.2                                                                | TEST -03 | Service   | Reject duplicate patient ID — test_services.py                       | Register a patient using an existing patient ID; expect ValueError and verify the original record is unchanged.                                              | Covered. Confirms duplicate patient registration is rejected and the original is preserved.              | Supplied                                     |
| FR-02 — Patient lookup            | AC-02.1, AC-02.2                                                       | TEST -04 | Service   | Find known and unknown patients — test_services.py                   | A known patient is returned; an unknown valid patient ID reports absence according to the public service contract.                                           | Planned - not yet run                                                                                    | Student authored                             |
| FR-03 — Practitioner registration | Supporting registration contract; no canonical AC specified            | TEST -14 | Service   | Register and store practitioner — test_services.py                   | Register a practitioner with a unique ID, valid name and specialty. Verify the practitioner is stored and retrievable with the expected details.             | Planned - not yet run                                                                                    | Student authored                             |
| FR-03 — Practitioner registration | Supporting duplicate-ID validation contract; no canonical AC specified | TEST -15 | Service   | Service	Reject duplicate practitioner ID — test_services.py           | Attempt to register a practitioner using an existing practitioner ID. Expect ValueError and verify the original practitioner remains unchanged.              | Covered by supplied test; student-authored evidence not yet run                                          | Supplied / planned student-authored evidence |
| FR-03 — Practitioner lookup       | Supporting lookup operation; no canonical AC specified                 | TEST -16 | Service   | Find known and unknown practitioners — test_services.py              | A known practitioner is returned; a valid but unknown practitioner ID raises LookupError.                                                                    | Covered by supplied Stage 6 tests; student-authored evidence not yet run                                 | Supplied / planned student-authored evidence |
| FR-04 — Appointment booking       | AC-03.1                                                                | TEST -05 | Domain    | Appointment construction and initial status — test_domain.py         | A valid appointment object can be constructed with its expected details and initial SCHEDULED status. This is partial domain evidence, not proof of storage. | Planned - not yet run                                                                                    | Student authored                             |
| FR-04 — Appointment booking       | AC-03.1                                                                | TEST -06 | Service   | Book and retrieve appointment — test_services.py                     | With registered participants, a unique ID and a free time, booking stores a SCHEDULED appointment retrievable by ID.                                         | Planned - not yet run                                                                                    | Student authored                             |
| FR-05 — Practitioner conflict     | AC-04.1                                                                | TEST -07 | Service   | Reject same-practitioner time conflict — test_services.py            | A second SCHEDULED booking for the same practitioner at the exact same date/time raises ValueError; the original booking remains unchanged.                  | Covered. Checks both same-practitioner conflict rejection and a different practitioner at the same time. | Supplied                                     |
| FR-05 — Practitioner conflict     | AC-04.2                                                                | TEST -08 | Service   | Allow different practitioners at same time — test_services.py        | Two different registered practitioners can have SCHEDULED appointments at the exact same date/time.                                                          | Covered. Checks both same-practitioner conflict rejection and a different practitioner at the same time. | Supplied                                     |
| FR-06 — Cancellation              | AC-05.1                                                                | TEST -09 | Domain    | Cancel scheduled appointment — test_domain.py                        | Cancelling a SCHEDULED appointment changes its status to CANCELLED. This proves domain behaviour, not service-level history retention.                       | Partially run. Student authored portion to be run                                                        | Partial supplied / partial student authored  |
| FR-06 — Cancellation              | AC-05.1, AC-05.3                                                       | TEST -10 | Service   | Cancel appointment and reject repeat cancellation — test_services.py | Service cancellation changes status to CANCELLED; a repeated cancellation raises ValueError and leaves the status unchanged.                                 | Planned - not yet run                                                                                    | Student authored                             |
| FR-07 — Appointment history       | AC-05.2                                                                | TEST -11 | Service   | Retrieve cancelled appointment — test_services.py                    | After cancellation, the appointment remains retrievable by ID from the shared data store, with status CANCELLED.                                             | Planned - not yet run                                                                                    | Student authored                             |
| FR-08 — Appointment lookup        | AC-06.1                                                                | TEST -12 | Service   | Find appointment by ID — test_services.py                            | Looking up a known appointment ID returns the expected appointment.                                                                                          | Planned - not yet run                                                                                    | Student authored                             |

## C Test Design

Use descriptive test names such as test_cancel_changes_status() or test_blank_patient_id_is_rejected(). Explain what new evidence each case adds.

| Test ID | Requirement                               | Acceptance criterion                                                             | Positive / Negative / Boundary   | Test intention                                                                                                                                            | Observable result expected                                                                                                                        | Added evidence beyond supplied tests                                                                                                                                                                                                                                         |
|---------|-------------------------------------------|----------------------------------------------------------------------------------|----------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| TEST-01 | FR-01 — Patient registration              | AC-01.1 (partial domain evidence)                                                | Positive and Negative            | Verify that a patient can be constructed with valid required details and that a blank patient ID is rejected.                                             | Valid details are retained by the Patient object; a blank or whitespace-only patient ID raises ValueError.                                        | Adds student-authored domain-level checks of valid patient construction and required-field validation. Supplied tests already check a whitespace-only patient ID, so this overlaps with existing evidence. It does not prove registration or storage.                        |
| TEST-05 | FR-04 — Appointment booking               | AC-03.1 (partial domain evidence)                                                | Positive                         | Verify that an appointment can be constructed using valid patient and practitioner objects and a valid date/time, and that its initial status is correct. | The appointment retains the expected ID, participants and date/time, and its status is AppointmentStatus.SCHEDULED.                               | Adds student-authored checks of appointment details and initial status. The supplied starter test already checks a valid booking and scheduled status through the workflow, so the domain test adds focused construction-level evidence rather than proving service booking. |
| TEST-09 | FR-06 — Cancellation                      | AC-05.1 (partial domain evidence)                                                | Positive                         | Verify that cancelling a scheduled appointment changes its domain status.                                                                                 | Calling cancel() changes the appointment status from AppointmentStatus.SCHEDULED to AppointmentStatus.CANCELLED.                                  | Adds a focused student-authored domain test of the status transition. The supplied starter test already checks domain cancellation, so this is overlapping evidence rather than entirely new behaviour.                                                                      |
| TEST-02 | FR-01 — Patient registration              | AC-01.1                                                                          | Positive                         | Register a patient with valid required details and an unused ID.                                                                                          | The patient is stored and can be retrieved with the expected details.                                                                             | Adds student-authored evidence of registration and storage, beyond domain construction alone.                                                                                                                                                                                |
| TEST-04 | FR-02 — Patient lookup                    | AC-02.1, AC-02.2                                                                 | Positive and Negative            | Look up a registered patient and then look up a valid but unknown patient ID.                                                                             | The known patient is returned; the unknown ID raises LookupError at the service boundary.                                                         | Adds explicit student-authored service lookup evidence for known and unknown patients.                                                                                                                                                                                       |
| TEST-06 | FR-04 — Appointment booking               | AC-03.1                                                                          | Positive                         | Register a patient and practitioner, then book an appointment using their IDs, a unique appointment ID and a valid date/time.                             | The service returns or stores the appointment with the registered participants, expected date/time and SCHEDULED status; lookup retrieves it.     | Adds student-authored end-to-end service evidence for booking and retrieval.                                                                                                                                                                                                 |
| TEST-07 | FR-05 — Practitioner conflict             | AC-04.1                                                                          | Negative / Boundary              | Book a second appointment for the same practitioner at the exact same date/time while the first remains SCHEDULED.                                        | The second booking raises ValueError; the original appointment remains unchanged and retrievable.                                                 | Supplied starter test already checks conflict rejection. Additional assertions could verify state preservation.                                                                                                                                                              |
| TEST-10 | FR-06 — Cancellation                      | AC-05.1, AC-05.3                                                                 | Positive and Negative / Boundary | Cancel a scheduled appointment through the service, then attempt to cancel it again.                                                                      | The first cancellation returns the same appointment and changes its status to CANCELLED; the second raises ValueError without changing its state. | Adds explicit service-level cancellation evidence; supplied tests already cover domain cancellation and repeated-cancellation.                                                                                                                                               |
| TEST-11 | FR-07 — Appointment history               | AC-05.2                                                                          | Positive                         | Cancel an appointment and retrieve it by ID and from the store's appointment listing.                                                                     | The same appointment remains available with status CANCELLED.                                                                                     | Adds focused evidence of history retention at the service boundary and through the shared store.                                                                                                                                                                             |
| TEST-12 | FR-08 — Appointment lookup                | AC-06.1                                                                          | Positive                         | Look up a known appointment ID through the service.                                                                                                       | The expected appointment is returned.                                                                                                             | Adds explicit student-authored appointment lookup evidence.                                                                                                                                                                                                                  |
| TEST-13 | FR-05 / FR-06 — Conflict and cancellation | Supporting contract: a cancelled booking does not occupy the practitioner's slot | Positive / Boundary              | Cancel a scheduled appointment, then book a new appointment for the same practitioner and exact date/time using a different appointment ID.               | The new appointment is accepted and SCHEDULED; the cancelled appointment remains CANCELLED and retrievable.                                       | Adds a focused test of slot reuse after cancellation.                                                                                                                                                                                                                        |
| TEST-14 | FR-03 — Practitioner registration         | Supporting registration contract; no canonical AC specified                      | Positive                         | Verify that a practitioner can be registered with a unique ID, valid name and specialty.                                                                  | The practitioner is stored and can be retrieved by ID with the expected ID, name and specialty.                                                   | Adds student-authored evidence of the successful practitioner registration workflow. The supplied tests cover duplicate registration and lookup, but do not explicitly verify successful registration with all required details.                                             |

## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome. Use the specific current exception with pytest.raises where needed.

| Test ID | Arrange                                                                                                                                                   | Act                                                                                                                             | Assert                                                                                                                                                   | Why meaningful / why assertion proves criterion                                                                                                                |
|---------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| TEST-01 | Create a Patient using a valid patient ID and name. Also prepare a patient with a blank or whitespace-only ID.                                            | Construct both Patient objects, using pytest.raises(ValueError) for the invalid one.                                            | The valid patient retains the expected ID and name. The invalid construction raises ValueError.                                                          | Confirms required patient details are accepted and a blank patient ID is rejected. This is domain-level evidence only, not proof of registration or storage.   |
| TEST-05 | Create valid Patient and Practitioner objects and a valid minute-precision datetime.                                                                      | Construct an Appointment with a unique appointment ID and objects.                                                              | The appointment retains the expected ID, patient, practitioner and date/time; its status is AppointmentStatus.SCHEDULED.                                 | Confirms that a valid appointment can be constructed with the expected details and initial status.                                                             |
| TEST-09 | Create a valid appointment in its default scheduled state.                                                                                                | Call appointment.cancel().                                                                                                      | The appointment status is AppointmentStatus.CANCELLED.                                                                                                   | Verifies the domain cancellation operation changes the status from scheduled to cancelled.                                                                     |
| TEST-02 | Create a fresh SmartCareDataStore and the three services using that same store. Create a patient with a unique ID and valid details.                      | Register the patient using PatientService.                                                                                      | The patient can be retrieved by ID and the returned object has the expected details.                                                                     | Proves registration stores the patient and makes it retrievable, rather than only constructing a patient object.                                               |
| TEST-04 | Create a fresh shared store and services. Register a valid patient. Prepare a valid but unknown patient ID.                                               | Look up the registered patient, then look up the unknown ID.                                                                    | The known lookup returns the registered patient. The unknown lookup raises LookupError.                                                                  | Demonstrates both successful patient lookup and the service's handling of a valid ID that is not found.                                                        |
| TEST-06 | Create a fresh shared store and services. Register a real patient and practitioner. Prepare a unique appointment ID and valid date/time.                  | Call book_appointment(appointment_id, patient_id, practitioner_id, date_time), then look up the appointment by ID.              | The appointment is stored and retrievable. It contains the registered patient and practitioner objects, expected date/time and SCHEDULED status.         | Verifies the service resolves registered participants and successfully books and stores the appointment.                                                       |
| TEST-07 | Create a fresh shared store and services. Register a patient and practitioner. Book a first appointment for that practitioner at a particular date/time.  | Attempt to book a second appointment with a different appointment ID but the same practitioner and exact date/time.             | The second booking raises ValueError. The original appointment remains unchanged and retrievable.                                                        | Proves that an existing scheduled appointment prevents another booking for the same practitioner at the exact same time, without damaging the original record. |
| TEST-10 | Create a fresh shared store and services. Register participants and book a scheduled appointment.                                                         | Cancel the appointment through AppointmentService, then attempt to cancel it again.                                             | The first cancellation returns the same appointment and changes its status to CANCELLED. The second raises ValueError, and the status remains CANCELLED. | Verifies service-level cancellation, the returned object and protection against repeated cancellation.                                                         |
| TEST-11 | Create a fresh shared store and services. Register participants, book an appointment and cancel it.                                                       | Retrieve the cancelled appointment by ID and obtain the appointment listing from the store.                                     | The appointment is still retrievable and appears in the listing with CANCELLED status.                                                                   | Demonstrates that cancellation does not delete the appointment and that its history remains available during the session.                                      |
| TEST-12 | Create a fresh shared store and services. Register participants and book an appointment with a unique ID.                                                 | Look up the appointment using its ID through AppointmentService.                                                                | The returned appointment is the expected appointment, with the correct ID and details.                                                                   | Confirms the service can retrieve a known appointment by ID.                                                                                                   |
| TEST-13 | Create a fresh shared store and services. Register a patient and practitioner. Book an appointment for that practitioner at a particular date/time.       | Cancel the first appointment, then book a second appointment with a different ID for the same practitioner and exact date/time. | The second booking succeeds and has SCHEDULED status. The first appointment remains retrievable with CANCELLED status.                                   | Proves a cancelled booking no longer occupies the practitioner's time slot while its history is retained.                                                      |
| TEST-14 | Create a fresh SmartCareDataStore and all three services using that same store. Prepare a practitioner with a unique ID, valid name and specialty.        | Register the practitioner using PractitionerService.                                                                            | Retrieve the practitioner by ID and verify the returned object has the expected ID, name and specialty.                                                  | Demonstrates that practitioner registration stores a valid practitioner and makes the correct record retrievable.                                              |
| TEST-15 | Create a fresh shared store and services. Register a practitioner with a unique ID. Prepare another practitioner using the same ID but different details. | Attempt to register the second practitioner.                                                                                    | ValueError is raised and the original practitioner remains retrievable with its original details.                                                        | Proves duplicate practitioner IDs are rejected without overwriting the existing record.                                                                        |
| TEST-16 | Create a fresh shared store and services. Register a practitioner and prepare a valid but unknown practitioner ID.                                        | Look up the known practitioner, then look up the unknown ID.                                                                    | The known practitioner is returned; the unknown ID raises LookupError.                                                                                   | Demonstrates successful practitioner lookup and the service's handling of a valid but unknown ID.                                                              |

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID | Behaviour                                                             | Test file/function                                                                   | Result                |
|---------|-----------------------------------------------------------------------|--------------------------------------------------------------------------------------|-----------------------|
| TEST-01 | Reject blank patient ID and accept valid patient details              | test_domain.py — test_blank_patient_id_is_rejected, test_patient_stores_valid_fields | Planned — not yet run |
| TEST-05 | Construct a valid appointment and verify initial SCHEDULED status     | test_domain.py — test_appointment_starts_scheduled_and_stores_valid_fields           | Planned — not yet run |
| TEST-09 | Cancel a scheduled appointment and verify status changes to CANCELLED | test_domain.py — test_cancel_changes_status                                          | Planned — not yet run |

## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID | Behaviour                                                | Test file/function                                                           | Result                                  |
|---------|----------------------------------------------------------|------------------------------------------------------------------------------|-----------------------------------------|
| TEST-02 | Register and retrieve a patient                          | test_services.py — test_register_and_store_patient                           | Planned — not yet run                   |
| TEST-03 | Reject duplicate patient ID without overwriting original | test_starter.py — test_duplicate_patient_preserves_original (supplied)       | Supplied test — regression run pending  |
| TEST-04 | Find known patient and reject unknown patient ID         | test_services.py — supplied patient lookup tests                             | Supplied tests — regression run pending |
| TEST-06 | Book and retrieve a valid appointment                    | test_services.py — test_book_and_retrieve_appointment                        | Planned — not yet run                   |
| TEST-07 | Reject same-practitioner, exact-time conflict            | test_starter.py — test_conflict_rule_and_different_practitioner (supplied)   | Supplied test — regression run pending  |
| TEST-10 | Cancel appointment and reject repeated cancellation      | test_services.py — test_cancel_appointment_changes_status_and_rejects_repeat | Planned — not yet run                   |
| TEST-11 | Retain and retrieve cancelled appointment                | test_services.py — test_cancelled_appointment_remains_retrievable            | Planned — not yet run                   |
| TEST-12 | Find appointment by ID                                   | test_services.py — test_find_appointment_by_id                               | Planned — not yet run                   |
| TEST-13 | Rebook a cancelled practitioner's time slot              | test_services.py — test_cancelled_appointment_does_not_block_slot            | Planned — not yet run                   |
| TEST-14 | Register and retrieve a practitioner                     | test_services.py — test_register_and_store_practitioner                      | Planned — not yet run                   |

## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour                              | Boundary/invalid input                                                                                               | Expected result                                                                                                                                                            | Test ID                                                                  |
|----------------------------------------|----------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------|
| Patient required-field validation      | Blank or whitespace-only patient ID                                                                                  | ValueError is raised and no patient is created. Checks that required identifiers cannot be blank.                                                                          | TEST-01                                                                  |
| Patient required-field validation      | Blank or whitespace-only patient name                                                                                | ValueError is raised and no patient is created. Checks that required patient details cannot be omitted.                                                                    | TEST-01                                                                  |
| Duplicate patient registration         | Register another patient using an existing patient ID                                                                | ValueError is raised and the original patient record remains unchanged. Checks that duplicate IDs cannot overwrite records.                                                | TEST-03                                                                  |
| Patient lookup                         | Blank or whitespace-only patient ID                                                                                  | ValueError is raised. Checks that invalid lookup input is distinguished from a missing record.                                                                             | TEST-04                                                                  |
| Patient lookup                         | Valid but unknown patient ID                                                                                         | LookupError is raised. Checks that an absent patient is reported correctly.                                                                                                | TEST-04                                                                  |
| Practitioner required-field validation | Blank or whitespace-only practitioner ID, name or specialty                                                          | ValueError is raised. Checks that all required practitioner details are validated.                                                                                         | TEST-14                                                                  |
| Duplicate practitioner registration    | Register another practitioner using an existing practitioner ID                                                      | ValueError is raised and the original practitioner remains unchanged. Checks that duplicate IDs cannot overwrite records.                                                  | TEST-15                                                                  |
| Practitioner lookup                    | Blank or whitespace-only practitioner ID                                                                             | ValueError is raised. Checks invalid lookup input handling.                                                                                                                | TEST-16                                                                  |
| Practitioner lookup                    | Valid but unknown practitioner ID                                                                                    | LookupError is raised. Checks that an absent practitioner is distinguished from invalid input.                                                                             | TEST-16                                                                  |
| Appointment construction               | Blank or whitespace-only appointment ID                                                                              | ValueError is raised. Checks that appointments require a valid identifier.                                                                                                 | TEST-05                                                                  |
| Appointment construction               | Patient or practitioner argument is not the required domain object                                                   | ValueError is raised. Checks that invalid participant objects cannot be used.                                                                                              | TEST-05                                                                  |
| Appointment construction               | Date/time is not a datetime, has seconds or microseconds, or is timezone-aware                                       | ValueError is raised. Checks the local, naive, minute-precision date/time contract.                                                                                        | TEST-05                                                                  |
| Appointment construction               | Status is not a valid AppointmentStatus value                                                                        | ValueError is raised. Checks that invalid appointment states cannot be constructed.                                                                                        | TEST-05                                                                  |
| Appointment booking                    | Patient or practitioner ID refers to an unregistered participant                                                     | Booking is rejected and no appointment is stored. Checks that only registered participants can be booked.                                                                  | TEST-06                                                                  |
| Duplicate appointment registration     | Book another appointment using an existing appointment ID                                                            | ValueError is raised and the original appointment remains unchanged. Checks that duplicate appointment IDs cannot overwrite records.                                       | Supporting supplied test — test_duplicate_appointment_preserves_original |
| Practitioner conflict                  | Same practitioner, exact same date/time, existing appointment still SCHEDULED                                        | ValueError is raised and the original appointment remains unchanged. Checks the precise conflict condition.                                                                | TEST-07                                                                  |
| Practitioner conflict                  | Different practitioner at the exact same date/time                                                                   | Both appointments are accepted and remain SCHEDULED. Checks that the conflict rule does not incorrectly block another practitioner.                                        | TEST-08                                                                  |
| Appointment cancellation               | Appointment is already CANCELLED                                                                                     | ValueError is raised and the appointment remains CANCELLED and retrievable. Checks that repeated cancellation is prevented.                                                | TEST-10                                                                  |
| Appointment cancellation               | Appointment has COMPLETED status                                                                                     | ValueError is raised and the appointment remains COMPLETED. Checks the cancellation status guard.                                                                          | TEST-10                                                                  |
| Appointment lookup                     | Valid but unknown appointment ID                                                                                     | LookupError is raised. Checks that a missing appointment is reported correctly.                                                                                            | TEST-12                                                                  |
| Cancelled appointment slot reuse       | First appointment is cancelled; a new appointment uses the same practitioner and exact date/time with a different ID | New booking succeeds with SCHEDULED status; original appointment remains CANCELLED and retrievable. Checks that cancelled bookings no longer occupy a practitioner's slot. | TEST-13                                                                  |

## H GitHub Copilot Test Design

Select ONE real acceptance criterion. Complete human-first fields before using Copilot. Do not require an accepted generated test.

Requirement: FR-05 - Reject another SCHEDULED booking for the same practitioner at exactly the same datetime. PG rescheduling reuses this rule.
Acceptance criterion: AC-04.1 (Supporting criterion - A practitioner cannot have two scheduled appointments at the same date and time)
Behaviour to test: Attempt to book two appointments with the same practitioner at exactly the same date and time.
Human-first test idea/categories: Valid booking; conflicting booking rejected; different practitioner at the same time accepted; original appointment remains unchanged after rejection.
Prompt and purpose: [complete or link]

For each significant candidate, copy this entry as needed:
- Copilot test idea/candidate: [complete]
- What it claims to verify: [complete]
- Requirement trace: [complete]
- Assertion quality: [complete]
- Human critique: [complete]
- Decision: [Accept / Modify / Reject]
- Reason: [complete]
- Final test reference if accepted/modified: [link or not retained]
- Actual verification result: [complete; do not claim an unrun test passed]

Before accepting: traces to a requirement/criterion; can fail for the right reason; assertion checks required behaviour; no invented business rule; no unnecessary private implementation dependence. Reject/modify weak assertions, invented requirements, excessive mocking, duplicates, wrong exceptions, obsolete architecture and unnecessary dependencies.

## I Weak Copilot Test Reflection

Which Copilot-generated test looked convincing but was weak? [response]
Why was it weak? [response]
How did you strengthen it? [response]
Accepted / modified / rejected test decisions and evidence: [link actual decisions in H]

## J Regression Run

Run python -m pytest from project/. Retain all accumulated tests. Record the tested SHA accurately.

| Command | Working directory | Code SHA | Passed | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation |
|---|---|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

Individual test runs and changed-order independence evidence: [commands, results, links]
Optional tutor-led demonstration notes: [optional; leave blank if not used]
A meaningful test should detect a relevant incorrect result. Students do not have to perform the demonstration or submit failure/restoration evidence for assessment. The tutor restores the example and reruns its tests. This is not a Stage 8 fault activity.
Requirement → test → failure/observation → diagnosis → change → verification: [concise links where applicable]

## K What the Suite Still Does Not Prove

What does your test suite still not prove? [response]
Coverage if used: [result or not used]
Which uncovered areas matter, and why does coverage percentage alone not establish correctness? [response]
Optional fixtures/parametrisation used and why, if any: [response or not used]

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow; no commit/PR count, conflict or individual test quota is imposed.

| Issue/task | Branch | PR | Reviewer | Key feedback | Outcome |
|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

| Member | Actual contribution | Evidence link |
|---|---|---|
| [complete] | [complete] | [complete] |

## N Formative Questions

1. What question does verification answer?
[response]

2. What question does validation answer?
[response]

3. What is a unit test?
[response]

4. What is a pytest fixture?
[response]

5. What is parametrisation in pytest?
[response]

6. What is regression testing?
[response]

7. What does code coverage tell us, and what does it not prove?
[response]

8. What makes an assertion weak?
[response]

9. What is the appropriate role of GitHub Copilot as a test assistant?
[response]

10. What is the Stage 7 engineering rule?
[response]

## O Stage Completion

Tested Stage 7 main SHA: [complete]
Full-suite result: [complete]
Unresolved defects and effect on baseline: [complete or none]
Clean working tree and integration evidence: [complete]
Stage 8 handover status: [complete; no Stage 8 work assigned]
All tutorial/formative responses and traceability/Copilot decisions complete: [confirm]
