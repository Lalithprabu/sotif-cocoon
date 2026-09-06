# SOTIF Safety Cocoon — Requirements Traceability

This document defines the safety requirements implemented by the SOTIF 
Safety Cocoon and traces each one to its implementation and verification.

---

## REQ-SOTIF-001: Low-Confidence Rejection

**Statement:** The system shall reject any AI perception output whose 
confidence score is below 0.5.

**Rationale:** A low-confidence detection indicates the AI model itself 
is uncertain about what it perceived. Acting on uncertain perception 
data without a plausibility gate risks acting on a hallucinated or 
misclassified object.

**Implementation:** `ring2_plausibility.py`, function `check_plausibility()`, 
confidence threshold check.

**Verification:** `test_ring3.py`, test case "Single frame - bad detection, 
no history" and "Good then bad - should hold last good state".

---

## REQ-SOTIF-002: Distance Range Validation

**Statement:** The system shall reject any detection reporting a distance 
value that is negative or exceeds 200 meters.

**Rationale:** Negative distances are physically impossible and indicate 
a sensor/model fault. Distances beyond the sensor's realistic operating 
range indicate unreliable or corrupted data, not a genuine detection.

**Implementation:** `ring2_plausibility.py`, function `check_plausibility()`, 
distance range check.

**Verification:** Not yet covered by an automated test case. 
[Gap - to be addressed]

---

## REQ-SOTIF-003: Safe-State Fallback on Implausible Detection

**Statement:** When a detection is deemed implausible, the system shall 
fall back to the last known good detection if one exists, rather than 
passing the implausible detection downstream.

**Rationale:** Momentary AI perception faults (e.g. a single bad frame) 
should not cause abrupt, unsafe vehicle behavior. Holding the last known 
good state provides continuity while the fault condition is transient.

**Implementation:** `ring3_arbiter.py`, function `arbitrate()`, 
`DEGRADED_HOLD_LAST_GOOD` branch.

**Verification:** `test_ring3.py`, test case "Good then bad - should hold 
last good state".

---

## REQ-SOTIF-004: Safe Stop on No Valid History

**Statement:** When a detection is deemed implausible and no prior known 
good detection exists, the system shall request a full stop and driver 
takeover rather than acting on unverified data.

**Rationale:** With no trustworthy reference point, the system has no 
safe basis to continue autonomous operation, so it must default to the 
most conservative available action.

**Implementation:** `ring3_arbiter.py`, function `arbitrate()`, 
`SAFE_STOP_REQUEST_TAKEOVER` branch.

**Verification:** `test_ring3.py`, test case "Single frame - bad detection, 
no history".

---

## REQ-SOTIF-005: State Reset Capability

**Statement:** The system shall provide a mechanism to reset all persisted 
state to a known baseline (no prior good detection).

**Rationale:** Without a controlled reset mechanism, stale state could 
carry over between operational cycles or test executions, producing 
incorrect or misleading safety decisions.

**Implementation:** `ring3_arbiter.py`, function `reset_state()`.

**Verification:** `test_ring3.py`, `run_tests()` calls `reset_state()` 
before each independent test case.

---

## REQ-SOTIF-006: Motion Continuity Check

**Statement:** The system shall reject a detection if its reported distance 
changes by more than 5 meters compared to the immediately preceding accepted 
detection.

**Rationale:** A detection can appear individually plausible (valid confidence, 
valid distance range) while still being physically impossible in context — 
e.g. an object appearing to instantaneously jump position between frames. 
This indicates a perception fault (e.g. misassociation between frames, or 
a false detection) that single-frame checks cannot catch.

**Implementation:** `ring2_plausibility.py`, function `check_plausibility()`, 
distance jump check against `last_accepted_distance_m`.

**Verification:** `test_ring3.py`, test case "Good then implausible distance 
jump - should hold last good state".