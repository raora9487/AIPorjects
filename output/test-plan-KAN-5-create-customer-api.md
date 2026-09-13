# Test Plan — KAN-5: Create Customer API

> Status: **DRAFT — pending human review.** Not approved until a QA owner signs off.

## 1. Scope & Objectives
- **In scope:**
  - `POST /api/v1/customers` — create a new customer via REST API
  - Authentication via `Authorization: Bearer <access_token>`
  - Request validation (mandatory fields, email format, phone format)
  - Duplicate-email handling
  - Success response contract (customerId + customer object)
  - Error response handling (400 / 401 / 409 / 500)
  - Non-functional: HTTPS, response time < 2s for 95% of requests, no sensitive data in logs, JSON only
- **Out of scope** (per ticket):
  - Updating an existing customer
  - Deleting a customer
  - Customer authentication/registration
  - Sending email notifications after customer creation
- **Objective:** Verify that a valid authenticated request creates a customer and returns `201` with a unique `customerId`, and that every invalid/unauthorized/conflicting request is rejected with the correct status code, without leaking sensitive details. "Tested" = the API contract in AC1–AC8 holds for this endpoint only; downstream consumption of the created customer is not verified here.

## 2. Gaps & Questions for the author
| # | Area | Finding (⚠️/❌) | Question to author |
|---|------|----------------|--------------------|
| 1 | Phone format | ⚠️ AC6 says "required length" but no exact length or format (min/max digits, country code, leading `+`, spaces/dashes). | What is the exact allowed phone format? (e.g. 10 digits, no `+`) |
| 2 | Mandatory fields | ⚠️ AC2 lists firstName, lastName, email. Is `phone` mandatory? Sample body includes it but AC2 omits it. | Is `phone` required or optional? What if it is absent? |
| 3 | dateOfBirth | ⚠️ Present in sample request, but no validation rule stated. | Is `dateOfBirth` mandatory? Is a past-date / age validation required? What format (YYYY-MM-DD)? |
| 4 | Field length/format | ⚠️ No max lengths or character rules for firstName/lastName (spaces? digits? Unicode?). | Are there length limits or character restrictions on name fields? |
| 5 | Duplicate email | ⚠️ AC4 says 409 when email exists. Case sensitivity? Trim? "Already exists" vs "soft-deleted/inactive"? | Is duplicate detection case-insensitive? Are whitespace-trimmed emails treated equal? |
| 6 | Error body | ❌ No contract for error responses (only "appropriate validation message" in AC3/AC6). | What is the error response schema (e.g. `{code, message, fieldErrors}`)? |
| 7 | Roles/permissions | ⚠️ "Valid authenticated request" — is any authenticated user allowed, or a specific role/scope? | Which token scopes/roles may create customers? |
| 8 | Token scheme | ⚠️ AC5 covers missing/invalid token. What about expired token, revoked token, malformed header? | Expected status for expired vs malformed `Authorization` header (401 vs 400)? |
| 9 | Idempotency / duplicates | ❌ No retry/idempotency key mentioned. | Can a client retry safely, or may a retry create duplicate customers? |
| 10 | Status field | ⚠️ Response includes `"status": "ACTIVE"` — is this always ACTIVE at creation? | Is status always ACTIVE, or configurable in the request? |
| 11 | createdAt | ⚠️ Format in response is `2026-09-06T10:30:00Z`. | Is createdAt server-generated UTC ISO-8601? |
| 12 | 500 handling | ⚠️ AC8 says no sensitive details. Is there a standard error envelope? | What does the 500 body look like? Any error-tracking/correlation ID? |
| 13 | NFR — "under normal load" | ⚠️ Perf target has no defined load profile. | What load profile defines "normal load" for the 95% < 2s target? |
| 14 | Logging | ⚠️ "Sensitive info not written to logs" — but which fields are sensitive (email? phone? DOB? full body?). | What is the sensitive-fields list and the audit requirement (if any)? |
| 15 | Environment/version | ❌ No test environment, API version, or build identified. | Which environment/version should this be tested against? |
| 16 | Linked issues/data | ❌ No linked issues, fix version, or downstream consumer identified. | Which downstream system consumes this and is it available in test? |

## 3. Test Scenarios
| ID | Priority | Type (pos/neg/boundary) | Scenario | Maps to (AC / gap) |
|----|----------|-------------------------|----------|--------------------|
| TS-1 | P0 | positive | Valid request with all fields → `201 Created`, body has `customerId`, echo of fields, `status: ACTIVE`, `createdAt` UTC ISO-8601 | AC1, AC7 |
| TS-2 | P0 | positive | Customer created with a unique `customerId` on each call | AC1 |
| TS-3 | P0 | boundary | Minimal valid request — only mandatory fields (first, last, email); confirm 201 (depends on Q2: phone/DOB optional?) | AC1, Q2/Q3 |
| TS-4 | P0 | negative | Missing `firstName` → `400` | AC2 |
| TS-5 | P0 | negative | Missing `lastName` → `400` | AC2 |
| TS-6 | P0 | negative | Missing `email` → `400` | AC2 |
| TS-7 | P0 | negative | Empty-string / whitespace-only mandatory field → `400` | AC2, Q4 |
| TS-8 | P0 | negative | Invalid email format (e.g. `not-an-email`) → `400` with validation message | AC3 |
| TS-9 | P0 | negative | Well-formed but rejected edge emails (`a@b`, missing TLD) → behavior recorded | AC3, Q6 |
| TS-10 | P1 | boundary | Email case variations against an existing customer (e.g. `RAJESH.RAO@EXAMPLE.COM`) → duplicate or not, per Q5 | AC4, Q5 |
| TS-11 | P0 | negative | Duplicate email of an existing customer → `409 Conflict` | AC4 |
| TS-12 | P0 | negative | Missing `Authorization` header → `401` | AC5 |
| TS-13 | P0 | negative | Invalid/expired token → `401` | AC5, Q8 |
| TS-14 | P2 | negative | Malformed `Authorization` header (not Bearer, garbage) → expected status per contract | AC5, Q8 |
| TS-15 | P0 | negative | Phone with non-numeric characters (e.g. `123-456-7890`) → `400` | AC6, Q1 |
| TS-16 | P0 | boundary | Phone at/around the required length limit → `400`/`201` per format rule | AC6, Q1 |
| TS-17 | P2 | negative | `dateOfBirth` invalid date, future date, wrong format → behavior recorded | Q3 |
| TS-18 | P1 | positive | Response Content-Type is `application/json`; body matches AC7 schema | AC7 |
| TS-19 | P1 | negative | Unexpected server error → `500` with no stack trace / no sensitive data in body | AC8 |
| TS-20 | P1 | negative | Non-JSON body / malformed JSON → expected error (400) without server crash | Q6, NFR-JSON |
| TS-21 | P1 | boundary | Empty JSON body `{}` → `400` listing missing mandatory fields | AC2 |
| TS-22 | P2 | negative | Oversized payload / extra unknown fields → behavior recorded | Q4/Q6 |
| TS-23 | P2 | positive | Repeated identical valid requests → duplicates or idempotent per contract | Q9 |
| TS-24 | P1 | negative | HTTPS enforced; plain HTTP request rejected/redirected | NFR |
| TS-25 | P1 | security | Submit request and confirm logs contain no email/phone/DOB/full-body values | NFR, Q14 |
| TS-26 | P2 | performance | Smoke: response time < 2s for p95 under agreed load profile | NFR, Q13 |
| TS-27 | P1 | negative | Request with a valid token but no required permission/scope (if roles exist) → 403 or 401 per contract | AC5, Q7 |

## 4. Test Data & Environment
- **Data:**
  - Valid: `{"firstName":"Rajesh","lastName":"Rao","email":"rajesh.rao@example.com","phone":"9876543210","dateOfBirth":"1990-05-15"}` (from ticket)
  - Invalid emails: `not-an-email`, `a@b`, `user@.com`, `user@domain..com`
  - Phones: `9876543210`, `123-456-7890`, `98765`, `+919876543210` (per Q1)
  - Edge: empty strings, whitespace, `{}`, malformed JSON, oversized body, unknown extra fields
  - Duplicate: pre-seed a customer with `rajesh.rao@example.com` (and case variant for TS-10)
- **Environment / flags:**
  - `[Environment Details Required]` — no test environment/version in ticket. HTTPS base URL only.
- **Roles / permissions:**
  - Valid Bearer token (scope TBD — Q7)
  - Missing token, invalid token, expired/revoked token (Q8)
  - No role/permission-scope matrix confirmed yet (Q7)

## 5. Risks & Assumptions
- **Assumptions made:**
  - `phone` and `dateOfBirth` are treated as optional until the author confirms otherwise (AC2 lists only first/last/email).
  - Error responses follow a consistent JSON structure (unconfirmed).
  - Response `createdAt` is server-generated UTC ISO-8601.
  - HTTP→HTTPS is enforced at the gateway or API layer.
- **Risks:**
  - High: phone format and mandatory-field ambiguity (Q1/Q2) can produce false pass/fail in validation tests.
  - High: undefined error-body contract makes negative tests assertions weak until Q6 is answered.
  - Medium: duplicate-email semantics (case/trim, Q5) affect AC4 tests.
  - Medium: no test environment identified blocks execution readiness.
  - Medium: 500-body / log-content assertions depend on the sensitive-fields definition (Q14).

## 6. Entry / Exit criteria
- **Entry:**
  - KAN-5 code merged and deployed to the identified test environment.
  - Test environment URL and API version confirmed (currently `[Environment Details Required]`).
  - At least one valid Bearer token for a permitted test user.
  - Ability to reset/cleanse customer data between runs (to re-test duplicate email).
  - Gaps Q1–Q4, Q6, Q7 answered or explicitly deferred by the author.
- **Exit:**
  - TS-1, TS-4…TS-13, TS-15, TS-19 (P0 set) executed and passed.
  - All `409`/`400`/`401` negative cases verified against the confirmed contract.
  - Critical/Blocker defects fixed and re-tested; remaining defects documented with severity + business impact.
  - Performance smoke (TS-26) executed; result recorded against the 95% < 2s target.
  - QA owner sign-off obtained on this plan and on execution results.

---
## HUMAN REVIEW GATE
- **I assumed:** phone/DOB are optional; error body is structured JSON; createdAt is server UTC; HTTPS is gateway-enforced.
- **I could not confirm:** exact phone format/length (Q1); mandatory-ness of phone (Q2) and dateOfBirth (Q3); name length limits (Q4); duplicate-email case/trim semantics (Q5); error-response schema (Q6); token scope/roles (Q7/Q8); idempotency (Q9); test environment (Q15); downstream consumer (Q16).
- **Open questions blocking sign-off:** Q1, Q2, Q3, Q6, Q7, and Q15 — these change test assertions and environment setup. The rest can be recorded as assumptions.
- ▶ **Approve, or edit, before I write test cases / automation.**
