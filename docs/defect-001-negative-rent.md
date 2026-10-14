# DEFECT-001: API accepts negative monthly rent

## Summary
The property creation endpoint accepts a negative monthly rent.

## Environment
- Application: QE Property API
- Endpoint: POST /api/properties
- Authentication: Valid local bearer token
- Test method: pytest / HTTP request

## Preconditions
The local API test client is available and a valid bearer token is supplied.

## Steps to reproduce
1. Send a POST request to /api/properties.
2. Include a valid property name.
3. Set monthly_rent to -1.
4. Observe the HTTP status and response body.

## Request
{
  "name": "Negative Rent Property",
  "monthly_rent": -1
}

## Expected result
HTTP 422 Unprocessable Entity. The API should reject rent values
less than or equal to zero.

## Actual result (initial buggy version)
HTTP 201 Created. The API accepts and stores a negative rent.

## Severity
Medium in this training scenario. The impact in a real system would
depend on downstream billing, reporting, and data-integrity behavior.

## Evidence
The automated regression test
test_create_property_rejects_negative_rent reproduces the issue.

## Root cause
The initial request model enforced the maximum rent but did not
enforce a positive minimum.

## Fix
Add a strict lower boundary to the request model.

## Regression coverage
- Zero rent is rejected.
- Negative rent is rejected.
- The smallest valid rent is accepted.
- The maximum valid rent is accepted.
- Rent above the maximum is rejected.

## Status
Resolved in the training version after the validation fix.
