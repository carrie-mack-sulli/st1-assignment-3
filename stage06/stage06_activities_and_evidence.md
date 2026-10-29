# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: Group Exception 1
- Members, GitHub usernames and cohorts: Carrie Sullivan
- Repository URL: (https://github.com/carrie-mack-sulli/st1-assignment-3)
- Original Starting SHA:0db72f2
- Repository restructuring: After the original Starting SHA, the folders were restructured to bring the starter files under the repository root. This change was committed separately.
- Assignment work commencement SHA: 9a1f7eb — 'Move SmartCare starter files to repository root'
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
- Actual issue link: [[response]](https://github.com/carrie-mack-sulli/st1-assignment-3/issues/1)

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
- Actual issue link: [[response]](https://github.com/carrie-mack-sulli/st1-assignment-3/issues/2)

## B Commit quality

| Original example | Strong or Weak | Reason                                                                                                                       |
|---|----------------|------------------------------------------------------------------------------------------------------------------------------|
| changes | Weak           | Message does not explain what was changed or why. A reviewer cannot easily understand the purpose of the commit.             |
| final version | Weak           | Feature or fix is not identified. “final version” does not explain the specific change, its purpose or why it was conducted. |
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
- Additional questions if useful: [response]

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
| (https://github.com/carrie-mack-sulli/st1-assignment-3/issues/1) | FR-02 Patient Search — implement PatientService.find_patient(patient_id) | carrie-mack-sulli | Returns the same stored patient object for a matching trimmed ID; raises ValueError for blank input and LookupError for a valid but unknown ID; matching is case-sensitive.| Open       |
| (https://github.com/carrie-mack-sulli/st1-assignment-3/issues/2) | FR-06 Appointment Cancellation and FR-07 retained history — implement AppointmentService.cancel_appointment(appointment_id). | carrie-mack-sulli | Cancels only scheduled appointments, returns the same object, retains the appointment record, raises LookupError for an unknown ID and ValueError for disallowed cancellation states. | Open |
| (https://github.com/carrie-mack-sulli/st1-assignment-3/issues/3) | Supporting Stage 6 target — implement PractitionerService.find_practitioner(practitioner_id). | carrie-mack-sulli | Returns the same stored practitioner object for a matching trimmed ID; raises ValueError for blank input and LookupError for a valid but unknown ID; matching is case-sensitive. | Open |

## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.

- PR link and title: [response]
- Linked issue and requirement: [response]
- Feature branch: [response]
- Changed behaviour: [response]
- Meaningful commits: [links]
- Test command, directory and observed result: [response]
- Another-member reviewer: [response]
- Human observations recorded before Copilot: [link and time]
- Requirement, responsibilities, test assertions and unrelated-scope checks: [response]
- Key feedback: [response]
- Author response/change and verification: [response]
- Reviewer recheck and approval: [link]
- Merge outcome and SHA: [response]
- Significant Copilot assistance: [summary or none]
- Linked issue closure: [response]
- Each member updated main: [member and confirmation]
- Integrated verification after merge: [command, directory, result and code SHA]

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: [response]
- Prompt/purpose and relevant issue/diff: [response]
- Summary of output: [response]
- Human check against actual code, requirements and tests: [response]
- Decision — Accept / Modify / Reject: [select]
- Reason: [response]
- Verification/evidence: [link and result]

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: [response]
- Copilot noticed: [response]
- Overlap: [response]
- What did the human reviewer notice that Copilot did not: [response]
- What did Copilot identify that the human reviewer initially missed: [response]
- Unsupported or incorrect Copilot suggestion: [response or none identified with explanation]
- Human judgement accepted, modified or rejected, and why: [response]
- Which evidence justified merge approval: [response]

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: [response]
- Implementation: [work and evidence]
- Testing: [work and evidence]
- Review: [work and evidence]
- Issue refinement: [work and evidence]
- Design and responsibility discussion: [work and evidence]
- Debugging or integration: [work and evidence]
- Documentation or team support: [work and evidence]

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

[response]

## L Stage 6 formative questions

1. What is version control?

[response]

2. Why is a feature branch useful?

[response]

3. What makes a commit a good engineering commit?

[response]

4. What is a pull request?

[response]

5. What is the purpose of code review?

[response]

6. What does a Git diff show?

[response]

7. What is a Definition of Done?

[response]

8. What is the appropriate role of GitHub Copilot in pull-request review?

[response]

9. Why should individual contribution not be judged only by commit count?

[response]

10. What is the Stage 6 engineering rule?

[response]

## M Completion and handover

- Starting SHA: [response]
- Final Stage 6 code SHA: [response]
- Test command: [response]
- Working directory: [response]
- Observed result: [response]
- PR and another-member reviewer: [links]
- Unresolved issue or none: [response]
- Stage 7 handover status: [ready for tutor checkpoint / unresolved work]
- Final submitted SHA if later than tested SHA: [response and evidence-only difference]

- [ ] Three Stage 6 service targets completed and checked.
- [ ] Original supplied tests retained and passing.
- [ ] At least two focused issues link requirements and acceptance criteria.
- [ ] Feature work reviewed by another member using the actual diff.
- [ ] Human-first review and required Copilot comparison recorded.
- [ ] Feedback resolved and approval recorded before merge.
- [ ] Everyone pulled main and integrated checks passed.
- [ ] Required activities, quiz responses and contribution notes completed.
- [ ] Only synthetic data included; confidential peer material kept out.
- [ ] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.

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