# Test Plan Requirement Checklist

## Purpose

This checklist defines the rules that must be followed when creating or
reviewing a Test Plan using the `test_plan_template.md`.

The Test Plan must contain enough information for a QA team to
understand **what will be tested, what will not be tested, how testing
will be performed, what is required to start testing, what defines
completion, and what risks or dependencies exist**.

------------------------------------------------------------------------

# 1. Mandatory Information

The following information must be captured whenever it is available.

## 1.1 Project Information

-   [ ] Project / Product name
-   [ ] Release / Version
-   [ ] Test Plan version
-   [ ] Prepared by
-   [ ] Date
-   [ ] Reviewer
-   [ ] Document status

### Rule

Do not invent project information.

If information is unavailable, use:

`[Not Provided]`

or

`[To Be Confirmed]`

Do not guess names, versions, dates, environments, or tools.

------------------------------------------------------------------------

# 2. Test Objectives

The Test Plan must clearly explain **why testing is being performed**.

Capture objectives such as:

-   Functional validation
-   Business workflow validation
-   Integration validation
-   Regression validation
-   Defect prevention
-   Release confidence
-   Non-functional validation where applicable

### Rule

Objectives must be specific to the project.

Avoid generic statements that do not explain the purpose of testing for
the release.

------------------------------------------------------------------------

# 3. Scope

Scope is mandatory.

## 3.1 In Scope

Clearly identify:

-   Features
-   Modules
-   User journeys
-   APIs
-   Integrations
-   Data flows
-   Platforms
-   Supported browsers/devices
-   Business processes
-   Relevant non-functional areas

### Rule

Every major requirement or feature included in the release should have a
corresponding scope statement.

Do not assume that an entire application is in scope just because the
release affects one module.

------------------------------------------------------------------------

## 3.2 Out of Scope

The Test Plan must explicitly identify functionality that will **not**
be tested.

Examples:

-   Features not included in the release
-   Unsupported platforms
-   Third-party functionality outside team control
-   Performance testing when not part of the release
-   Security testing when handled by a separate team
-   Legacy modules unaffected by the change
-   Known areas excluded by business decision

For every significant exclusion, capture the reason where possible.

### Rule

Never silently omit an area that could reasonably be expected to be
tested.

If an area is intentionally excluded, state it explicitly.

If scope cannot be determined from the requirements, mark it:

`[Scope Confirmation Required]`

------------------------------------------------------------------------

# 4. Requirements Coverage

The Test Plan must establish traceability between requirements and
testing.

Capture:

-   Requirement ID
-   Requirement description
-   Related test scenarios / test cases
-   Priority
-   Coverage status

### Rule

Every testable requirement should map to one or more test scenarios.

Flag requirements that:

-   Have no test coverage
-   Are ambiguous
-   Are incomplete
-   Have conflicting acceptance criteria
-   Cannot currently be tested

Do not create fake requirement IDs.

------------------------------------------------------------------------

# 5. Test Approach

The Test Plan must explain **how the application will be tested**.

Consider:

-   Functional testing
-   Integration testing
-   System testing
-   Regression testing
-   Smoke testing
-   Sanity testing
-   API testing
-   UI testing
-   Database testing
-   Performance testing
-   Security testing
-   Compatibility testing
-   Accessibility testing
-   UAT

### Rule

Only include testing types that are relevant to the project.

Do not automatically claim that every testing type will be performed.

For each applicable testing type, explain its purpose where useful.

------------------------------------------------------------------------

# 6. Test Design Techniques

Select appropriate techniques based on the requirements.

Possible techniques:

-   Equivalence Partitioning
-   Boundary Value Analysis
-   Decision Tables
-   State Transition Testing
-   Error Guessing
-   Pairwise Testing
-   Risk-Based Testing
-   Positive / Negative testing

### Rule

Testing techniques should be derived from the nature of the requirement.

For example:

-   Numeric limits → Boundary Value Analysis
-   Multiple business conditions → Decision Tables
-   Workflow/state changes → State Transition Testing
-   Multiple combinations → Pairwise Testing

Do not list techniques merely to make the Test Plan appear
comprehensive.

------------------------------------------------------------------------

# 7. Test Scenarios

Scenarios must describe the important business and technical behaviors
that need validation.

Capture:

-   Scenario ID
-   Scenario description
-   Priority
-   Test type
-   Expected result

Scenarios should include, where applicable:

-   Positive flows
-   Negative flows
-   Boundary conditions
-   Validation rules
-   Error handling
-   Authorization
-   Authentication
-   Integration behavior
-   Data validation
-   Business rules
-   Failure/recovery scenarios

### Rule

Do not limit scenarios to the happy path.

Critical negative and boundary scenarios must be considered.

------------------------------------------------------------------------

# 8. Test Environment

Capture the environment required to execute testing.

Where applicable include:

-   Environment name
-   Application URL
-   Application version
-   Database
-   Operating system
-   Browser/client
-   API gateway
-   External systems
-   Test infrastructure

### Rule

Do not invent environment details.

If the requirement document does not specify the environment, use:

`[Environment Details Required]`

------------------------------------------------------------------------

# 9. Test Data

Identify the data required to execute testing.

Consider:

-   Valid data
-   Invalid data
-   Boundary data
-   Empty/null data
-   Duplicate data
-   Large-volume data
-   Role-specific data
-   Date/time-related data
-   API request/response data
-   Sensitive data requirements

Capture:

-   Data type
-   Description
-   Source
-   Owner

### Rule

If production data is required, explicitly identify:

-   Whether production data is allowed
-   Masking/anonymization requirements
-   Data privacy constraints

Never assume sensitive production data can be used.

------------------------------------------------------------------------

# 10. Automation Strategy

Identify which tests should be automated and which should remain manual.

Automation candidates may include:

-   Regression tests
-   Smoke tests
-   Stable workflows
-   API tests
-   Data-driven tests
-   Repetitive validation

Manual candidates may include:

-   Exploratory testing
-   Usability testing
-   Visual validation
-   Frequently changing functionality
-   Tests requiring human judgment

### Rule

Do not claim automation coverage without evidence.

If an automation framework/tool is unknown, mark it:

`[Automation Tool To Be Confirmed]`

------------------------------------------------------------------------

# 11. Entry Criteria

Clearly define conditions that must be satisfied before testing starts.

Consider:

-   Requirements available
-   Build deployed
-   Environment available
-   Test data available
-   Dependencies available
-   Test cases reviewed
-   Access configured
-   Critical environment issues resolved

### Rule

Entry criteria should be measurable wherever possible.

Avoid vague statements such as:

`Environment should be ready.`

Prefer:

`QA build is successfully deployed and accessible to the QA team.`

------------------------------------------------------------------------

# 12. Exit Criteria

Define objective conditions for completing testing.

Consider:

-   Planned test cases executed
-   Critical scenarios passed
-   Critical/Blocker defects resolved
-   Regression completed
-   Required coverage achieved
-   Test results reviewed
-   Stakeholder approval obtained

### Rule

Exit criteria must not imply that testing is complete simply because the
planned execution period has ended.

If known defects remain, document:

-   Severity
-   Business impact
-   Workaround
-   Approval / exception

------------------------------------------------------------------------

# 13. Defect Management

Define:

-   Defect management tool
-   Severity levels
-   Defect workflow
-   Retesting process
-   Reopen criteria
-   Defect reporting expectations

### Rule

Do not invent the organization's defect tool.

If unknown:

`[Defect Management Tool To Be Confirmed]`

------------------------------------------------------------------------

# 14. Risk Management

Identify testing risks that could affect quality, schedule, or coverage.

Consider:

-   Environment instability
-   Requirement changes
-   Test data availability
-   External dependencies
-   Resource availability
-   Build instability
-   Third-party service failures
-   Automation instability
-   Incomplete requirements

For each important risk capture:

-   Risk
-   Impact
-   Probability
-   Mitigation

### Rule

High-impact risks must have a mitigation or contingency where possible.

------------------------------------------------------------------------

# 15. Dependencies

Identify dependencies on:

-   Development teams
-   Product owners
-   Business teams
-   DevOps
-   Infrastructure
-   Databases
-   External APIs
-   Third-party systems
-   Test data providers
-   Other applications

### Rule

Do not assume dependencies are available.

Clearly mark dependencies that must be confirmed before testing.

------------------------------------------------------------------------

# 16. Roles and Responsibilities

Define who is responsible for:

-   Test planning
-   Test case creation
-   Test execution
-   Automation
-   Defect management
-   Environment support
-   Requirement clarification
-   Business acceptance
-   Release approval

### Rule

If actual names are unavailable, use role names instead of inventing
people.

------------------------------------------------------------------------

# 17. Schedule

Capture testing activities such as:

-   Test planning
-   Test design
-   Test data preparation
-   Environment preparation
-   Test execution
-   Defect fixing/retesting
-   Regression
-   UAT
-   Final sign-off

### Rule

Do not invent dates.

Use:

`[Date To Be Confirmed]`

when dates are not provided.

------------------------------------------------------------------------

# 18. Regression Strategy

The Test Plan must explain how regression scope will be selected.

Consider:

-   Changed functionality
-   Impacted modules
-   Dependent functionality
-   Critical business workflows
-   Historical defect areas
-   Production incidents
-   High-risk areas

Regression may be divided into:

1.  Smoke
2.  Critical regression
3.  Full regression

### Rule

Regression scope should be risk-based.

Do not automatically state that the entire application will undergo full
regression unless the requirements or project context support it.

------------------------------------------------------------------------

# 19. Non-Functional Testing

Determine whether the release requires:

-   Performance testing
-   Load testing
-   Stress testing
-   Security testing
-   Accessibility testing
-   Compatibility testing
-   Reliability testing
-   Scalability testing

### Rule

If non-functional testing is not mentioned, do not automatically mark it
as required.

Instead record:

`Not specified - confirmation required`

when the area could materially affect release risk.

------------------------------------------------------------------------

# 20. AI-Assisted Testing

Where AI is used, capture applicable activities such as:

-   Requirement analysis
-   Test scenario generation
-   Test case generation
-   API test generation
-   Test data generation
-   Defect analysis
-   Regression test selection
-   Test optimization
-   Test result analysis

### Rule

AI-generated artifacts must be reviewed by a qualified QA engineer
before being treated as approved test assets.

AI output must not be considered automatically correct.

------------------------------------------------------------------------

# 21. Assumptions

Capture assumptions that influence the Test Plan.

Examples:

-   Required APIs will be available.
-   Test environment will remain available during execution.
-   Required test accounts will be provided.
-   External dependencies will be operational.

### Rule

Do not present assumptions as confirmed facts.

Clearly distinguish:

`Assumption`

from

`Confirmed Information`.

------------------------------------------------------------------------

# 22. Constraints

Capture known limitations such as:

-   Limited test environment availability
-   Limited test data
-   Limited testing time
-   Resource constraints
-   Dependency restrictions
-   Unsupported browsers/devices
-   Restricted production access

### Rule

Important constraints must be reflected in the risk assessment.

------------------------------------------------------------------------

# 23. Deliverables

Identify the testing artifacts that will be produced.

Possible deliverables:

-   Test Plan
-   Test Scenarios
-   Test Cases
-   Automation scripts
-   Test data
-   Defect reports
-   Execution reports
-   Regression report
-   Traceability matrix
-   Test summary report
-   Sign-off

### Rule

Only list deliverables that are actually expected for the project.

------------------------------------------------------------------------

# 24. Approval and Sign-off

Capture the required approval roles.

Possible roles:

-   QA Lead
-   Product Owner
-   Business Owner
-   Project Manager
-   Release Manager

### Rule

Do not invent approval names.

Use role names if individual names are unavailable.

------------------------------------------------------------------------

# 25. Information Quality Rules

The Test Plan must follow these rules.

## Never Invent Information

Do not fabricate:

-   Requirements
-   Requirement IDs
-   Features
-   Dates
-   Names
-   URLs
-   Environments
-   Tools
-   Defect IDs
-   Test case IDs
-   Metrics
-   Dependencies
-   Business rules

Use `[Not Provided]` or `[To Be Confirmed]`.

------------------------------------------------------------------------

## Separate Facts From Assumptions

Clearly distinguish:

-   Confirmed requirement
-   Assumption
-   Open question
-   Recommendation

Do not convert assumptions into facts.

------------------------------------------------------------------------

## Identify Missing Information

If critical information is missing, explicitly flag it.

Use:

`[MISSING INFORMATION]`

for information that is required to create a reliable Test Plan.

Use:

`[TO BE CONFIRMED]`

for information that is expected but has not yet been finalized.

------------------------------------------------------------------------

# 26. Requirement Ambiguity Rules

If a requirement is ambiguous:

1.  Identify the ambiguity.
2.  Explain why it affects testing.
3.  Do not invent the missing behavior.
4.  Add it to the assumptions/open-items section.
5.  Recommend clarification from the Product Owner/Business Analyst.

Example:

> Requirement states that a user can "edit an order" but does not
> specify whether editing is allowed after shipment.

Correct action:

`[CLARIFICATION REQUIRED] Define whether shipped orders can be edited.`

------------------------------------------------------------------------

# 27. Requirement Completeness Checklist

Before finalizing the Test Plan, verify:

-   [ ] Each requirement has a clear description.
-   [ ] Acceptance criteria are available where applicable.
-   [ ] Business rules are identified.
-   [ ] User roles are identified.
-   [ ] Inputs and expected outputs are identified.
-   [ ] Error scenarios are identifiable.
-   [ ] Dependencies are identified.
-   [ ] Integration points are identified.
-   [ ] Data requirements are identified.
-   [ ] Non-functional requirements are identified.
-   [ ] Requirements excluded from testing are explicitly identified.

------------------------------------------------------------------------

# 28. Final Test Plan Quality Gate

The Test Plan should NOT be considered complete if any of the following
are true:

-   [ ] Scope is unclear.
-   [ ] Out-of-scope areas are not identified.
-   [ ] Critical requirements have no test coverage.
-   [ ] Critical dependencies are unknown.
-   [ ] Test environment is undefined.
-   [ ] Required test data is undefined.
-   [ ] Entry criteria are missing.
-   [ ] Exit criteria are missing.
-   [ ] Critical risks have no mitigation.
-   [ ] Major assumptions are undocumented.
-   [ ] Important requirement ambiguities are unresolved or flagged.
-   [ ] The Test Plan contains fabricated information.
-   [ ] The testing approach does not align with the requirements.

------------------------------------------------------------------------

# 29. AI Agent Instructions

When an AI agent generates a Test Plan using this checklist:

1.  Read and analyze the available requirements first.
2.  Identify all features, modules, workflows, integrations, and
    business rules.
3.  Determine the testing scope from the requirements.
4.  Explicitly identify out-of-scope areas.
5.  Build traceability between requirements and test scenarios.
6.  Identify positive, negative, boundary, and error scenarios.
7.  Identify applicable testing types.
8.  Identify required test data and environments.
9.  Identify dependencies, assumptions, risks, and constraints.
10. Flag missing information rather than guessing.
11. Do not fabricate IDs, dates, names, tools, environments, or
    requirements.
12. Ensure entry and exit criteria are measurable.
13. Review the Test Plan against this checklist before finalizing it.
14. Clearly distinguish confirmed information from assumptions and
    recommendations.
15. If critical information is missing, highlight it as
    `[MISSING INFORMATION]`.
16. Do not mark a requirement as covered unless the Test Plan contains
    corresponding test coverage.
17. Do not mark an area as out of scope unless there is a valid basis
    for excluding it.
18. Keep the Test Plan consistent with the supplied requirements and
    project context.

------------------------------------------------------------------------

# 30. Final Validation

Before delivering the Test Plan, the agent must answer:

  Validation Question                                    Result
  ------------------------------------------------------ -------------
  Is the test scope clearly defined?                     PASS / FAIL
  Is out-of-scope functionality explicitly identified?   PASS / FAIL
  Are all known requirements covered?                    PASS / FAIL
  Are missing requirements identified?                   PASS / FAIL
  Are positive and negative scenarios considered?        PASS / FAIL
  Are dependencies identified?                           PASS / FAIL
  Are test data requirements identified?                 PASS / FAIL
  Is the test environment defined?                       PASS / FAIL
  Are entry criteria defined?                            PASS / FAIL
  Are exit criteria defined?                             PASS / FAIL
  Are risks and mitigations identified?                  PASS / FAIL
  Are assumptions clearly separated from facts?          PASS / FAIL
  Is regression scope defined?                           PASS / FAIL
  Are non-functional requirements addressed?             PASS / FAIL
  Does the Test Plan contain any invented information?   YES / NO
  Is stakeholder clarification required?                 YES / NO

The Test Plan should only be considered **Ready for Review** after this
validation has been completed.
