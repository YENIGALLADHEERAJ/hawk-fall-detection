# Phase 1B held-out regression evaluation — 2026-10-27

The exact five original clips, labels and hashes are unchanged. These subjects were held out initially,
but their failures now informed engineering changes. These are regression results, not unseen-test accuracy.
Original results are preserved in `evaluation/phase1b/original-results.json`; A is a fresh instrumented baseline.
All runs use actual OpenCV 5 YOLOX CPU inference at 640 input and 5 sampled frames/video-second.
A–D consumed identical sampled detections (asserted from every diagnostic record).

## Controlled ablation

| Variant | Fall recall | Non-fall FP clips | False candidates | Final dismissed | Review events | FPS | p50 / p95 ms | CPU % of one core |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A: Original baseline | 0/2 (0%) | 1/3 (33.3%) | 1 | 1 | 0 | 1.10 | 702.1 / 2022.2 | 186.5 |
| B: Tracking only | 0/2 (0%) | 1/3 (33.3%) | 1 | 1 | 0 | 1.24 | 548.1 / 1508.2 | 189.2 |
| C: Temporal only | 0/2 (0%) | 0/3 (0.0%) | 0 | 0 | 0 | 0.97 | 816.7 / 2252.8 | 186.1 |
| D: Tracking + temporal | 2/2 (100%) | 0/3 (0.0%) | 0 | 0 | 0 | 0.92 | 697.1 / 2327.2 | 190.3 |
| E: Initial D + low-confidence continuation (rejected) | 2/2 (100%) | 0/3 (0.0%) | 0 | 0 | 0 | 1.13 | 572.7 / 1945.3 | 186.1 |

FPS is total processed frames / total replay wall time. Percentiles pool measured per-frame latencies.
Inference, motion, evidence/debug encoding and diagnostic I/O are included. Model setup is excluded from replay time.
Runs were sequential, not repeated/randomized; CPU scheduling/thermal variation prevents causal speedup claims.
No configuration sustains the requested live 5 FPS. Memory API measurements are retained in ablation.json;
Windows peak memory is process-lifetime, not an independent per-clip peak.

## Per-clip results

| Variant / clip | Candidate times (s) | Onset latency (s) | Dismissed | IDs | Dominant ID frames / sampled | No detection frames | FPS | p50 / p95 ms |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| A / holdout_s2_Fall_13 | none | — | 0 | 8 | 16/45 | 9 | 0.88 | 1192.4 / 2152.0 |
| A / holdout_s2_ADL_14 | none | — | 0 | 3 | 15/42 | 6 | 1.11 | 671.8 / 2351.6 |
| A / holdout_s3_Fall_16 | none | — | 0 | 5 | 10/31 | 16 | 0.91 | 1138.1 / 2073.1 |
| A / holdout_s3_ADL_13 | none | — | 0 | 1 | 30/33 | 3 | 1.83 | 443.1 / 1332.2 |
| A / holdout_s3_ADL_09 | 6.435 | — | 1 | 1 | 39/39 | 0 | 1.21 | 712.3 / 1548.6 |
| B / holdout_s2_Fall_13 | none | — | 0 | 5 | 34/45 | 9 | 1.00 | 1202.8 / 1571.7 |
| B / holdout_s2_ADL_14 | none | — | 0 | 2 | 21/42 | 6 | 1.80 | 423.4 / 1240.2 |
| B / holdout_s3_Fall_16 | none | — | 0 | 2 | 15/31 | 16 | 0.90 | 1203.6 / 1850.0 |
| B / holdout_s3_ADL_13 | none | — | 0 | 1 | 30/33 | 3 | 1.56 | 544.0 / 1303.8 |
| B / holdout_s3_ADL_09 | 6.435 | — | 1 | 1 | 39/39 | 0 | 1.33 | 539.9 / 1430.7 |
| C / holdout_s2_Fall_13 | none | — | 0 | 8 | 16/45 | 9 | 0.98 | 915.9 / 2117.6 |
| C / holdout_s2_ADL_14 | none | — | 0 | 3 | 15/42 | 6 | 1.23 | 608.1 / 1577.6 |
| C / holdout_s3_Fall_16 | none | — | 0 | 5 | 10/31 | 16 | 0.70 | 1429.4 / 2625.8 |
| C / holdout_s3_ADL_13 | none | — | 0 | 1 | 30/33 | 3 | 1.19 | 632.4 / 2044.8 |
| C / holdout_s3_ADL_09 | none | — | 0 | 1 | 39/39 | 0 | 0.88 | 847.5 / 2357.2 |
| D / holdout_s2_Fall_13 | 3.813 | 1.313 | 0 | 5 | 34/45 | 9 | 0.74 | 1346.9 / 2299.9 |
| D / holdout_s2_ADL_14 | none | — | 0 | 2 | 21/42 | 6 | 1.17 | 691.6 / 1830.5 |
| D / holdout_s3_Fall_16 | 3.007 | 1.207 | 0 | 2 | 15/31 | 16 | 0.67 | 1691.0 / 2525.2 |
| D / holdout_s3_ADL_13 | none | — | 0 | 1 | 30/33 | 3 | 1.40 | 585.5 / 1807.0 |
| D / holdout_s3_ADL_09 | none | — | 0 | 1 | 39/39 | 0 | 0.96 | 674.6 / 2471.6 |
| E / holdout_s2_Fall_13 | 3.813 | 1.313 | 0 | 5 | 39/45 | 3 | 0.89 | 1049.8 / 2458.7 |
| E / holdout_s2_ADL_14 | none | — | 0 | 2 | 21/42 | 5 | 1.46 | 492.0 / 1855.4 |
| E / holdout_s3_Fall_16 | 2.004 | 0.204 | 0 | 2 | 24/31 | 7 | 0.93 | 1005.1 / 2000.2 |
| E / holdout_s3_ADL_13 | none | — | 0 | 1 | 30/33 | 2 | 1.53 | 518.2 / 1137.0 |
| E / holdout_s3_ADL_09 | none | — | 0 | 1 | 39/39 | 0 | 1.15 | 614.4 / 1885.7 |

Dominant-ID coverage and distinct-ID counts are continuity proxies, not ground-truth IDF1/HOTA.
Extra detections may be false people or duplicate boxes. They must not be interpreted as true person counts.
Onset latency uses the unchanged publisher labels and video time, not wall-clock notification latency.
A dismissed false candidate still counts as a false candidate. Fall candidates and human-review events are separate.

## Development regression cross-check

A full initial combined run on the original development set detected 10/11 falls but introduced two false candidates
among 13 negatives: clip_06 (squat) and gmdcsa_ADL_13 (compact sitting). Both came from the optional compact-low branch,
without horizontal posture. That branch was removed; horizontal geometry remains necessary but is insufficient alone.
Replaying all 25 clips' recorded real detections and motion through the final temporal estimator gives 10/11 falls and 0/13 FP clips.
This is a temporal-only recorded-evidence regression, not a second full detector benchmark; it has no FPS claim.
The original initial run is in evaluation/phase1b/development/results.json; final replay provenance and hashes are in
evaluation/phase1b/development-final-replay.json. Both negative clips also have full-inference integration tests.

## Diagnosis and changes

Subject 2 Fall/13: track 1 reaches RAPID_DESCENT at 3.211 s. No detections occur at 3.412 and 3.612 s.
The next horizontal detection at 3.813 s receives a new ID: the 0.602 s observation gap exceeds the old 0.5 s expiry.
Subject 3 Fall/16: last upright track-1 observation is at 1.804 s; five intervening sampled frames have no detections.
The next horizontal person at 3.007 s receives a new ID after a 1.203 s gap. The fall transition is not directly observed.
Thus detector coverage, track expiry and temporal reset interact. Sampling is still 5 FPS; these are missing detections
at sampled instants, not skipped timeline rows. Denser inference has not been shown to recover the transition.
Candidate scoring and dismissal do not explain the false negatives: no candidate reached either stage.

B retains unmatched track identities for up to 1.5 s, caps velocity prediction at 0.25 s, gates area changes,
and rejects ambiguous gap reattachment. It emits only actual detections. It does not fabricate/interpolate boxes.
B alone cannot overcome the original temporal reset. C alone cannot recover history across changed track IDs.
D combines retention with a bounded sequence rule: an observed upright reference, net downward center displacement
(at least 0.18 reference heights), average downward speed (at least 0.15 heights/s), height loss and horizontal geometry.
The window remains 1.5 s; observed endpoints may support a candidate when intermediate states are unavailable.
This is explicitly weaker evidence than observing the entire descent, and does not prove a fall during occlusion.
Missing or low-confidence observations reset stationarity. Recovery requires observed upward movement and upright geometry.

Subject 3 ADL/09 is getting up from the floor, including a crouched/bent pose. At 5.430 s box jitter gives a downward
velocity spike (~62.9 px/s); at 6.435 s the box becomes wide, although its center is moving upward (~−6.1 px/s).
The old recent-descent latch combines these unrelated cues into a candidate, dismissed at 6.837 s.
The new net-displacement rule rejects that sequence. No filename, subject, onset or label enters the perception modules.

E, when present, lowers the detection score floor to 0.15 only for association to existing tracks;
new identities still require 0.30. High-confidence matches are assigned first. Low-confidence boxes cannot establish immobility.
E uses the initial temporal variant, before the development-squat correction. It is a detector exploration, not the selected default.
Its earlier Subject 3 alert uses a confidence-0.276 box roughly 482x203 pixels wide over much of the room.
More raw detections therefore do not establish better localization; the earlier latency is not trusted evidence of an earlier observed fall.
The final temporal rule removes the initial compact-low branch after a development squat triggered it.
Horizontal geometry alone is still insufficient: net descent, speed, height loss and bounded upright history are also required.

## Evidence artifacts

Each run includes diagnostics.jsonl, timeline.csv, state-transitions.json, final-decision.json, original/annotated frames,
trajectory overlays and a real debug.avi. Timelines include dimensions, center, area, displacement, velocity, flow, state and reasons.

- A holdout_s2_Fall_13: [timeline](../../data/evaluation/20261026T190751804069/holdout_s2_Fall_13/timeline.csv), [frames](../../data/evaluation/20261026T190751804069/holdout_s2_Fall_13/contact.jpg), [video](../../data/evaluation/20261026T190751804069/holdout_s2_Fall_13/debug.avi), [transitions](../../data/evaluation/20261026T190751804069/holdout_s2_Fall_13/state-transitions.json), [decision](../../data/evaluation/20261026T190751804069/holdout_s2_Fall_13/final-decision.json).
- A holdout_s2_ADL_14: [timeline](../../data/evaluation/20261026T190751804069/holdout_s2_ADL_14/timeline.csv), [frames](../../data/evaluation/20261026T190751804069/holdout_s2_ADL_14/contact.jpg), [video](../../data/evaluation/20261026T190751804069/holdout_s2_ADL_14/debug.avi), [transitions](../../data/evaluation/20261026T190751804069/holdout_s2_ADL_14/state-transitions.json), [decision](../../data/evaluation/20261026T190751804069/holdout_s2_ADL_14/final-decision.json).
- A holdout_s3_Fall_16: [timeline](../../data/evaluation/20261026T190751804069/holdout_s3_Fall_16/timeline.csv), [frames](../../data/evaluation/20261026T190751804069/holdout_s3_Fall_16/contact.jpg), [video](../../data/evaluation/20261026T190751804069/holdout_s3_Fall_16/debug.avi), [transitions](../../data/evaluation/20261026T190751804069/holdout_s3_Fall_16/state-transitions.json), [decision](../../data/evaluation/20261026T190751804069/holdout_s3_Fall_16/final-decision.json).
- A holdout_s3_ADL_13: [timeline](../../data/evaluation/20261026T190751804069/holdout_s3_ADL_13/timeline.csv), [frames](../../data/evaluation/20261026T190751804069/holdout_s3_ADL_13/contact.jpg), [video](../../data/evaluation/20261026T190751804069/holdout_s3_ADL_13/debug.avi), [transitions](../../data/evaluation/20261026T190751804069/holdout_s3_ADL_13/state-transitions.json), [decision](../../data/evaluation/20261026T190751804069/holdout_s3_ADL_13/final-decision.json).
- A holdout_s3_ADL_09: [timeline](../../data/evaluation/20261026T190751804069/holdout_s3_ADL_09/timeline.csv), [frames](../../data/evaluation/20261026T190751804069/holdout_s3_ADL_09/contact.jpg), [video](../../data/evaluation/20261026T190751804069/holdout_s3_ADL_09/debug.avi), [transitions](../../data/evaluation/20261026T190751804069/holdout_s3_ADL_09/state-transitions.json), [decision](../../data/evaluation/20261026T190751804069/holdout_s3_ADL_09/final-decision.json).
- D holdout_s2_Fall_13: [timeline](../../data/evaluation/20261027T160513925666/holdout_s2_Fall_13/timeline.csv), [frames](../../data/evaluation/20261027T160513925666/holdout_s2_Fall_13/contact.jpg), [video](../../data/evaluation/20261027T160513925666/holdout_s2_Fall_13/debug.avi), [transitions](../../data/evaluation/20261027T160513925666/holdout_s2_Fall_13/state-transitions.json), [decision](../../data/evaluation/20261027T160513925666/holdout_s2_Fall_13/final-decision.json).
- D holdout_s2_ADL_14: [timeline](../../data/evaluation/20261027T160513925666/holdout_s2_ADL_14/timeline.csv), [frames](../../data/evaluation/20261027T160513925666/holdout_s2_ADL_14/contact.jpg), [video](../../data/evaluation/20261027T160513925666/holdout_s2_ADL_14/debug.avi), [transitions](../../data/evaluation/20261027T160513925666/holdout_s2_ADL_14/state-transitions.json), [decision](../../data/evaluation/20261027T160513925666/holdout_s2_ADL_14/final-decision.json).
- D holdout_s3_Fall_16: [timeline](../../data/evaluation/20261027T160513925666/holdout_s3_Fall_16/timeline.csv), [frames](../../data/evaluation/20261027T160513925666/holdout_s3_Fall_16/contact.jpg), [video](../../data/evaluation/20261027T160513925666/holdout_s3_Fall_16/debug.avi), [transitions](../../data/evaluation/20261027T160513925666/holdout_s3_Fall_16/state-transitions.json), [decision](../../data/evaluation/20261027T160513925666/holdout_s3_Fall_16/final-decision.json).
- D holdout_s3_ADL_13: [timeline](../../data/evaluation/20261027T160513925666/holdout_s3_ADL_13/timeline.csv), [frames](../../data/evaluation/20261027T160513925666/holdout_s3_ADL_13/contact.jpg), [video](../../data/evaluation/20261027T160513925666/holdout_s3_ADL_13/debug.avi), [transitions](../../data/evaluation/20261027T160513925666/holdout_s3_ADL_13/state-transitions.json), [decision](../../data/evaluation/20261027T160513925666/holdout_s3_ADL_13/final-decision.json).
- D holdout_s3_ADL_09: [timeline](../../data/evaluation/20261027T160513925666/holdout_s3_ADL_09/timeline.csv), [frames](../../data/evaluation/20261027T160513925666/holdout_s3_ADL_09/contact.jpg), [video](../../data/evaluation/20261027T160513925666/holdout_s3_ADL_09/debug.avi), [transitions](../../data/evaluation/20261027T160513925666/holdout_s3_ADL_09/state-transitions.json), [decision](../../data/evaluation/20261027T160513925666/holdout_s3_ADL_09/final-decision.json).

## Known failures and gate

The small reused set cannot establish generalization. Detection misses, duplicate boxes, occlusion ambiguity,
seated/foreshortened falls, real multi-person crossings, camera motion, natural fall/recovery and physical-camera tests remain unresolved.
Long gaps are intentionally not bridged; identity preservation is not proof that an unobserved motion was a fall.
**INCOMPLETE — perception still needs work.** Do not begin Phase 2.
Highest-priority next fix: improve real person-detection coverage during descent/prone poses, then evaluate on fresh untouched subjects.
See docs/phase-1-report.md for the test outcome and selected operating configuration.
