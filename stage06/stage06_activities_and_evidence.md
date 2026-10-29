# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: Group Exception 1
- Members, GitHub usernames and cohorts: Carrie Sullivan
- Repository URL: (https://github.com/carrie-mack-sulli/st1-assignment-3)
- Original Starting SHA:0db72f2
- Repository restructuring: After the original Starting SHA, the folders were restructured to bring the starter files under the repository root. This change was committed separately.
- Assignment work commencement SHA: 9a1f7eb ΓÇö 'Move SmartCare starter files to repository root'
- Feature branch: feature/FR-02-patient-search
- Feature branch created from: 9a1f7eb (main and origin/main pointed to this commit when the branch was created).

## A Requirement to issue activities

### FR-02 Patient Search

- Title: FR-02 Patient Search by patient ID
- Context: SmartCare needs to get registered patient records by patient_ID. The search is to return the existing patient object and identify invalid input of a valid ID that is not found.
- Requirement: Implement PatientService.find_patient(patient_id) so that it returns a registered patient using a trimmed, nonblank and case-sensitive ID. Invalid blank inputs are to raise ValueError; a valid but unknown ID must raise LookupError.
- Acceptance criteria:
1. When a registered patient's ID is provided, the service returns the associated stored Patient object.
2. Whitespace before and after is trimmed before searching.
3. A blank or whitespace-only ID raises ValueError.
4. A nonblank ID that does not match a registered patient raises LookupError.
5. Patient ID matching is case-sensitive.
6. Searching does not create, delete or replace stored patient records.
- Scope: Implement patient lookup method using the existing data store. Add focused tests for successful lookup, object identity, whitespace, blank and unknown IDs, case sensitivity, and preservation of stored records. Do not change registration or booking funationality.
- Definition of Done:
1. All acceptance criteria have related tests.
2. The service successfully returns the existing patient object when searched.
3. Invalid and unknown IDs show the specified exceptions.
4. Relevant automated tests pass and results are recorded.
5. Code and tests are committed to Git.
6. The commit reference and supporting evidence are recorded.
- Owner: carrie-mack-sulli - individual completion approved by Pranav.
- Actual issue link: (https://github.com/carrie-mack-sulli/st1-assignment-3/issues/1)

### FR-06 Appointment Cancellation with FR-07 retained history

- Title: FR-06 Appointment Cancellation with FR-07 retained history
- Context: SmartCare allows a scheduled appointment to be cancelled without deleting the record. Record retention retains appointment history. Cancellation will respect the appointment's existing domain state-transition rules.
- Requirement: Implement AppointmentService.cancel_appointment(appointment_id) so that it locates existing appointments, cancels through its domain operation, and returns the same appointment object. Only a scheduled appointment can be cancelled. An unknown ID must raise LookupError; an invalid cancellation state must raise ValueError.
- Acceptance criteria:
1. Cancelling an existing scheduled appointment changes its status to cancelled.
2. The service returns the same appointment object that was stored before cancellation.
3. The cancelled appointment remains retrievable from the data store and present in the appointment list.
4. Cancelling an unknown appointment ID raises LookupError without altering stored appointments.
5. Cancelling an already cancelled appointment raises ValueError and leaves status unchanged.
6. Cancelling a completed appointment raises ValueError and leaves status unchanged.
7. The service uses the appointment's domain cancellation operation rather than directly changing protected state or deleting the record.
- Scope: Implement the cancellation method using existing service, data-store and domain behaviour. Add focused tests for successful cancellation, history retention, returned object identity, unknown IDs, repeated cancellation and completed appointments. Do not implement appointment deletion or booking changes.
- Definition of Done:
1. All acceptance criteria have related tests.
2. Successful cancellation updates the status and retains the same stored appointment.
3. Invalid cancellation attempts raise the specified exceptions and preserve state.
4. Relevant automated tests pass and their results are recorded.
5. Code and tests are committed to Git.
6. The commit reference and supporting evidence are recorded.
- Owner: carrie-mack-sulli - individual completion approved by Pranav.
- Actual issue link: (https://github.com/carrie-mack-sulli/st1-assignment-3/issues/2)

## B Commit quality

| Original example | Strong or Weak | Reason                                                                                                                       |
|---|----------------|------------------------------------------------------------------------------------------------------------------------------|
| changes | Weak           | Message does not explain what was changed or why. A reviewer cannot easily understand the purpose of the commit.             |
| final version | Weak           | Feature or fix is not identified. ΓÇ£final versionΓÇ¥ does not explain the specific change, its purpose or why it was conducted. |
| Add patient search by ID | Strong         | This identifies the feature being added and how patients are to be searched. This provides a good overview of the change.    |
| fix stuff | Weak           | No information is provided on what has been changed.                                                                         |
| Prevent cancellation of completed appointments | Strong         | Explicity describes what the change is and expected behaviour.                                                               |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns: The PR includes more changes to the appointment cancellation requirement than is required or intended for this feature. Renaming patient fields and restructuring unrelated code makes it harder to identify which modifications are necessary for cancellation and increases the size of the change.
- Responsibility and architecture concerns: Unrelated patient-field changes could affect other parts of the application that depend on those fields. Restructuring unrelated code runs the risk of introducing regressions and makes it more difficult to relate problems to a specific change. The new dependency introduces an additional requirement that is not necessary for cancellation and could increase maintenance and compatibility costs.
- Testing and review concerns: Tests that pass doesn't show that the PR is appropriately scoped or that every behaviour has been validated. Reviewers must inspect the cancellation logic, patient-field changes, refactoring and dependency separately. Existing tests may not cover all affected code, integration points or regressions. The dependency also needs justification, appropriate compatibility and security consideration.
- Changes to remove or separate, with reasons: eep appointment cancellation implementation and its focused tests in the cancellation PR. Move unrelated patient-field renaming and unrelated restructuring into separate PRs; with its own purpose and tests, so these can be reviewed and reverted individually. Remove the new dependency from the cancellation PR unless it is necessary; if required, justify its use and review its maintenance, compatibility and security implications. Verify cancellation state transitions, error handling and retained appointment history, as well as relevant regression tests, before approving the PR.

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

- Missing evidence: Copilots review does not identify which tests were performed, what the results were or unintended impacts. Additionally, cross-reference against acceptance criteria was not mentioned nor was presevation of expected behaviour confirmed or evidence provided. Ultimately, no context of the testing is provided; which is required to holistically represent successful or failed testing.
- Follow-up review question 1: Which automated tests were run and what were the test outputs? List tests that were run.
- Follow-up review question 2: Of the acceptance criteria in the GitHub issue, show the test that provides evidance that it is satified. Which criteria were noy tested?
- Follow-up review question 3: What were the outputs when a blank ID or unknown ID is entered? What were the outputs of searching appointments that are cancelled or completed? Show exception handling tests.
- Follow-up review question 4: Does the cancellation feature retain the original appointment object in the data store and history? Which test results demonstrate this?
- Follow-up review question 5: Did changes modify patient fields or other services? List unintended scope changes and explain any risks associated with these.
- Additional questions if useful: N/A

## E Team workflow agreement

| Practice | Team agreement |
|---|---|
| Branch naming | Use descriptive feature branches in format of feature/FR-02-patient-search or feature/FR-06-appointment-cancellation. Use fix/ for a defect fix. Keep branch names lowercase and use hyphens.|
| Commit message convention | Use short, concise descriptions for each change, such as Add patient search by ID or Prevent cancellation of completed appointments. Avoid vague messages.|
| PR size | N/A - approved individual completion arrangement; this activity requires another group member.|
| Another-member review requirement | N/A - approved individual completion arrangement; this activity requires another group member. |
| Merge rule | N/A - approved individual completion arrangement; this activity requires another group member. |
| Significant Copilot disclosure rule | Disclose significant Copilot or other generative AI assistance in the required assignment evidence. Record purpose of the assistance, suggestions or output used, what was accepted, modified or rejected, and how the resulting code or claims were independently verified. Do not present AI output as human peer review. |

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status     |
|---|---|---|---|------------|
| (https://github.com/carrie-mack-sulli/st1-assignment-3/issues/1) | FR-02 Patient Search ΓÇö implement PatientService.find_patient(patient_id) | carrie-mack-sulli | Returns the same stored patient object for a matching trimmed ID; raises ValueError for blank input and LookupError for a valid but unknown ID; matching is case-sensitive.| Open       |
| (https://github.com/carrie-mack-sulli/st1-assignment-3/issues/2) | FR-06 Appointment Cancellation and FR-07 retained history ΓÇö implement AppointmentService.cancel_appointment(appointment_id). | carrie-mack-sulli | Cancels only scheduled appointments, returns the same object, retains the appointment record, raises LookupError for an unknown ID and ValueError for disallowed cancellation states. | Open |
| (https://github.com/carrie-mack-sulli/st1-assignment-3/issues/3) | Supporting Stage 6 target ΓÇö implement PractitionerService.find_practitioner(practitioner_id). | carrie-mack-sulli | Returns the same stored practitioner object for a matching trimmed ID; raises ValueError for blank input and LookupError for a valid but unknown ID; matching is case-sensitive. | Open |

## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.

- PR link and title: (https://github.com/carrie-mack-sulli/st1-assignment-3/pull/4) - Implement patient search and appointment cancellation
- Linked issue and requirement:
  - Patient search: #1 ΓÇö FR-02 Patient Search by patient ID
  - Appointment cancellation and retained history: #2 ΓÇö FR-06 Appointment Cancellation with FR-07 retained history
  - Supporting Stage 6 functionality: #3 ΓÇö Practitioner lookup by ID
- Feature branch: feature/FR-02-patient-search
- Changed behaviour:
  - Implement patient lookup by ID, including invalid and unknown ID exception handling.
  - Implement practitioner lookup by ID, including invalid and unknown ID exception handling.
  - Implement appointment cancellation through the transition method, retaining cancelled appointments in the store.
- Meaningful commits: (https://github.com/carrie-mack-sulli/st1-assignment-3/pull/4/changes/2077c5dad4cc0a43c831cf064b5b759b148960c0)
- Test command, directory and observed result:
  - Command: ..venv\Scripts\python.exe -m pytest
  - Working directory: project/
  - Result: 16 passed in 0.03 seconds.
- Another-member reviewer: N/A - approved individual completion arrangement; this activity requires another group member.
- Human observations recorded before Copilot: (https://github.com/carrie-mack-sulli/st1-assignment-3/pull/4#issuecomment-6482724902), 29 October 2026 09:50AM
- Requirement, responsibilities, test assertions and unrelated-scope checks:
  - Requirements and responsibilities
    - FR-02 - Find a patient by patient ID
    - FR-03 - Practitioner lookup as a supporting operation
    - FR-06 - Cancel only a SCHEDULED appointment
    - FR-07 - Retain cancelled appointments in current-session history
- Test assertions
  1.	Patient lookup returns the same stored patient object and allows a trimmed ID.
  2.	Blank patient IDs raise ValueError; unknown and case-mismatched IDs raise LookupError.
  3.	Practitioner lookup returns the same stored practitioner object and allows a trimmed ID.
  4.	Blank practitioner IDs raise ValueError; unknown and case-mismatched IDs raise LookupError.
  5.	Successful cancellation changes the status, returns the same appointment object, and preserves the appointment in the store.
  6.	Blank appointment IDs raise ValueError; unknown appointment IDs raise LookupError.
  7.	Repeated cancellation raises ValueError without changing the cancelled status or removing the stored appointment.
  8.	Cancelling a completed appointment raises ValueError without changing its status or removing the stored appointment.

- Test execution: Please refer to section in markdown titled Testing to view recorded testing and console verification outputs.
  - Unrelated-scope checks
    - The changes were limited to the Stage 6 service methods, the new service test file, and the Stage 6 evidence file.
    - Existing data-store and domain behaviour was reused.
    - Appointment cancellation uses the domain transition method and does not directly assign the appointment status or delete the record.
    - The Stage 9 list_practitioner_appointments placeholder has not been changed or updated at this stage.
    - FR-01 patient registration, FR-03 practitioner registration, FR-04 booking, and FR-05 practitioner-time conflict prevention were not identified as new implementations in this change.
    - FR-08 appointment lookup was not identified as a new implementation in this change.
    - FR-09 practitioner appointment listing was not implemented as part of this change.
    - FR-10 between-session persistence is retired and was

- Key feedback: N/A - approved individual completion arrangement; this activity requires another group member.
- Author response/change and verification: N/A - approved individual completion arrangement; this activity requires another group member.
- Reviewer recheck and approval: N/A - approved individual completion arrangement; this activity requires another group member.
- Merge outcome and SHA: b953cdc
- Significant Copilot assistance: Restricted to structuring my content into a logical and concise order.
- Linked issue closure:
  - https://github.com/carrie-mack-sulli/st1-assignment-3/issues/1
  - https://github.com/carrie-mack-sulli/st1-assignment-3/issues/2
  - https://github.com/carrie-mack-sulli/st1-assignment-3/issues/3
- Each member updated main: Carrie Sullivan conducted all activities in Stage06 except independant review.
- Integrated verification after merge: .\.venv\Scripts\python.exe -m pytest; directory: project/; result: 16 passed in 0.05s (8 service tests and 8 starter tests); code SHA: b953cdcdc9059b0c1624b55aff4266f883c3c642.

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: Carrie Sullivan asked Copilot to review PR
- Prompt/purpose and relevant issue/diff: Hi, please conduct a review of #4 pull request between main and feature/FR-02-patient-search. Please also check the relevant issues are linked, that PR corrolates to relevant requirements and confirm that testing is holistic for the implemented changes.
- Summary of output:
- Overall Review Conclusion
Your PR is well-structured, complete, and aligned with the stated requirements. The implementation is clean, the related issues are correctly referenced, and the testing is thorough across all functional and edge-case scenarios.

Final Verdict
This PR is ready for merge.
No blockers identified.
Only optional improvement: add “Closes #X” syntax for automatic issue closure.
- Human check against actual code, requirements and tests: Documentation of human check can be viewed at https://github.com/carrie-mack-sulli/st1-assignment-3/pull/4#issuecomment-6482724902. An observation of the Copilot response is that it confirma alignment to the requirements, however it has no visibility of them; demonstrating AIs willingness to please.
- Decision - Accept / Modify / Reject: None
- Reason: AI suggestions match my human review. No decision required.
- Verification/evidence: N/A

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: Implementation was as expected
- Copilot noticed: Large majority of implementation was as expected, with exception of Note: The PR does not use GitHub’s auto‑closing syntax (e.g., “Closes #1”), but the linkage is still clear and traceable.
- Overlap: All key areas of the review
- What did the human reviewer notice that Copilot did not: Effective connection to requirements.
- What did Copilot identify that the human reviewer initially missed: Nothing
- Unsupported or incorrect Copilot suggestion: Copilot highlighted a note rather than a suggestion; NNote: The PR does not use GitHub’s auto‑closing syntax (e.g., “Closes #1”), but the linkage is still clear and traceable. This was unsupported as I didn't feel it necessary to circle back and correct it.
- Human judgement accepted, modified or rejected, and why: Rejected, as noted in above dot point
- Which evidence justified merge approval: AI review matched my human review

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: Carrie Sullivan
- Implementation: All aspects of Stage06 demonstrated through individual completion of ST1-Assignment-3
- Testing: All documented testing for ST1-Assignment-3
- Review: N/A - approved individual completion arrangement; this activity requires another group member.
- Issue refinement: Supporting Stage 6 functionality: #3 ΓÇö Practitioner lookup by ID could have been updated to align with requirement FR-03 Register a practitioner with unique ID, name and specialty. Practitioner lookup is a supporting operation. However, I had closed the issue before considering this as an option.
- Design and responsibility discussion: N/A - approved individual completion arrangement; this activity requires another group member.
- Debugging or integration: N/A
- Documentation or team support: Carrie Sullivan demonstrated through all Stage06 content documented across files of .md, .py and GitHub.

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

A high commit count measures how many times changes have been made. This does not demonstrate quality of the changes. What should be sought is high quality changes with sufficient testing, documentation and no impact to other features.

## L Stage 6 formative questions

1. What is version control?

A history of changes to provide an audit trail of updates.

2. Why is a feature branch useful?

Because it allows an individual developer to work on a single feature, away from the core code.

3. What makes a commit a good engineering commit?

A good commit should be small and concise. This allows targeted implementation that is easy to track.

4. What is a pull request?

It is a change in one branch that is to be merged into another branch, once comparison is validated.

5. What is the purpose of code review?

To ensure accuracy that intended implementation is as expected. Having a second set of eyes is critical to all development work.

6. What does a Git diff show?

It shows the difference between 2 versions, allowing easy visibility and comparison of changes.

7. What is a Definition of Done?

A list of criteria that has been defined and agreed between developers and business, that is to be achieved for a feature to be considered complete.

8. What is the appropriate role of GitHub Copilot in pull-request review?

To assist a human review by checking changes are implemented correctly, alignment is made with requirements, identifying improvements and bugs.

9. Why should individual contribution not be judged only by commit count?

Because team members contribute in a variety of ways to ensure the shared goal is met and a quality outcome is achieved.

10. What is the Stage 6 engineering rule?

To implement the identified changes while retaining exiting domain rules.

## M Completion and handover

- Starting SHA: 9a1f7eb
- Final Stage 6 code SHA: 2077c5d
- Test command: .\.venv\Scripts\python.exe -m pytest
- Working directory: project/
- Observed result: 16 tests passed in 0.03 seconds.
- PR and another-member reviewer: (https://github.com/carrie-mack-sulli/st1-assignment-3/pull/4). Self and Copilot reviews conducted, no review performed by another team member as assignment is approved for individual completion.
- Unresolved issue or none: None
- Stage 7 handover status: ready for tutor checkpoint
- Final submitted SHA if later than tested SHA: b953cdc

- [Y ] Three Stage 6 service targets completed and checked.
- [Y ] Original supplied tests retained and passing.
- [Y ] At least two focused issues link requirements and acceptance criteria.
- [N/A ] Feature work reviewed by another member using the actual diff.
- [Y ] Human-first review and required Copilot comparison recorded.
- [N/A ] Feedback resolved and approval recorded before merge.
- [N/A ] Everyone pulled main and integrated checks passed.
- [Y ] Required activities, quiz responses and contribution notes completed.
- [Y ] Only synthetic data included; confidential peer material kept out.
- [Y ] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting.

## Testing

### Stage06 test verification
- Working directory: project/
- Command: .\.venv\Scripts\python.exe -m pytest
- Result: 16 tests passed in 0.03 seconds.
- Test breakdown: 8 tests in test_services.py and 8 supplied tests in test_starter.py.
- Verification: The Stage 6 service tests and supplied foundation tests passed. The supplied starter test file remains the same.
- Tested code SHA: To be recorded after the tested code is committed.

### Console demonstration verification
- Working directory: project/
- Command: .\.venv\Scripts\python.exe main.py
- Observed output: A1: P1 with DR1, 2026-10-01 09:00, scheduled
- Additional output: Session-only data: records are lost on exit.
- Result: The default console demo completed successfully with no error shown.
- Limitation: This verifies the default demo path only; it does not verify the interactive menu or persistent storage.

## References

### AI disclosure
1. I commenced the technical component of the assignment stage06 prior to completing the above activities. AI was used to determine steps for creating the first branch and switching to it without losing any work.
