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


---

## REQ-SOTIF-007: Persistent Decision Logging

**Statement:** The system shall record every frame-level safety decision to 
a persistent, timestamped log file, distinguishing normal operation from 
degraded or safe-stop events by severity level.

**Rationale:** Runtime safety decisions must be auditable after the fact — 
for incident investigation, regulatory review, or engineering analysis — 
not just visible transiently during execution.

**Implementation:** `logger_config.py` (logging configuration), used by 
`main_integration_test.py` via `logger.info()` for normal operation and 
`logger.warning()` for degraded/safe-stop events.

**Verification:** Manual inspection of `sotif_cocoon.log` after running 
`main_integration_test.py`, confirming timestamped INFO/WARNING entries 
matching each frame's Ring3 status. [Note: not yet covered by an automated 
test — see Known Gaps.]

---


---

## REQ-SOTIF-008: Real AI Model Validation

**Statement:** The system shall demonstrate correct plausibility rejection 
and safe-state arbitration when interfacing with a genuine pretrained 
object-detection model (YOLOv8n), including under deliberately degraded 
sensing conditions.

**Rationale:** Rule-based checks validated against synthetic/hand-crafted 
data do not prove the architecture holds up against real AI model output, 
which has genuine statistical uncertainty and failure modes that synthetic 
test data cannot fully represent.

**Implementation:** `ring1_perception_real.py` (real YOLO-based perception), 
`main_integration_real.py` (real-data integration pipeline), 
`create_degraded_image.py` (deliberate degradation to provoke low-confidence 
detection).

**Verification:** Manual run of `main_integration_real.py` against 
`images/bus.jpg` (clean image, confirmed NORMAL_OPERATION) and 
`images/bus_degraded.jpg` (degraded image, confirmed model misclassification 
with confidence 0.29, correctly rejected by Ring2, correctly triggering 
SAFE_STOP_REQUEST_TAKEOVER via Ring3). [Note: manual verification only, 
not yet an automated test - see Known Gaps.]

**Update (post REQ-SOTIF-009):** Following introduction of the temporal 
trust score, single-frame real AI validation now correctly reports 
SAFE_STOP_REQUEST_TAKEOVER rather than NORMAL_OPERATION, since trust has 
not yet accumulated. A 3-frame repeated-image sequence was used to confirm 
NORMAL_OPERATION is still reachable once sustained plausible detections 
occur (see `main_integration_real.py`, `run_real_pipeline_sequence()`).

---
---

## REQ-SOTIF-009: Temporal Trust Score with Hysteresis

**Statement:** The system shall maintain a temporal trust score for perception 
output, incrementing on plausible detections and decrementing more sharply on 
implausible detections, such that recovery to NORMAL_OPERATION requires 
sustained plausible detections rather than a single good frame.

**Rationale:** Instantaneous recovery on a single good frame after a fault 
sequence risks reacting to a transient fluke rather than genuine sensor/model 
recovery. This mirrors hysteresis and debounce filtering techniques used in 
automotive sensor signal processing, where rapid state oscillation (e.g. a 
warning light flickering near a threshold) is explicitly avoided by requiring 
sustained evidence before switching state.

**Implementation:** `ring3_arbiter.py`, trust score logic in `arbitrate()`.

**Verification:** `test_ring3.py`, new test cases covering: (a) single good 
frame after a fault sequence does not immediately restore NORMAL_OPERATION, 
(b) sustained good frames do eventually restore it.

---

---

## REQ-SOTIF-010: Fault Injection Validation on Real Video

**Statement:** The system shall demonstrate correct hysteresis-based 
degradation and recovery when a genuine transient sensing fault (simulated 
via localized blur/downscaling) is injected into a contiguous segment of 
an otherwise clean, self-recorded real-world video sequence.

**Rationale:** Static image tests (REQ-SOTIF-008) validate single-frame 
model behavior, but do not exercise the temporal trust-score logic 
(REQ-SOTIF-009) against a real, continuous sequence. This test closes 
that gap using genuinely original footage with a deliberately controlled, 
reproducible fault window.

**Implementation:** `create_video_frames.py` (frame extraction), 
`inject_fault_into_sequence.py` (deliberate fault injection into frames 
20-29 of a 52-frame sequence), `create_annotated_demo.py` (visual 
demonstration with on-screen Ring2/Ring3 status overlay).

**Verification:** Manual review of `images/cocoon_demo_with_fault.mp4`, 
confirming NORMAL_OPERATION during clean frames, degradation to 
SAFE_STOP_REQUEST_TAKEOVER/DEGRADED_HOLD_LAST_GOOD during the injected 
fault window (frames 20-29), and recovery to NORMAL_OPERATION once 
sustained clean frames resume. [Note: manual verification only, not yet 
an automated test - see Known Gaps.]

---

## Known Gaps

- REQ-SOTIF-007 (logging) is currently verified by manual inspection only, 
  not an automated test.
- REQ-SOTIF-008 (real AI model validation) is currently verified by manual 
  run and inspection only, not an automated test.
- REQ-SOTIF-010 (fault injection on real video) is currently verified by 
  manual video review only, not an automated test.