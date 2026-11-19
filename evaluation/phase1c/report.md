# HAWK Phase 1C fresh validation — 2026-10-28

**INCOMPLETE — perception still needs work**

**Highest-priority blocker: identity continuity through overlapping people.** The fresh pedestrian audit has 37 reference-associated ID changes; the pipeline cannot yet guarantee that fall/recovery evidence stays with its owner. The stricter association alternative worsened this metric and was rejected. No Phase 2 work was started.

## Fresh evaluation

15 fresh validation clips: 6 GMDCSA24 Subject 4 clips (new subject/room), 8 ASSIST-IoT reference activity videos, and one 10.2-second MOT17-09 extract (51 publisher frames at 5 Hz). Labels: 8 falls, 7 non-falls. The prior 30 clips are development/regression only. Eight Ursul Subject 04 / Location 2 archive members are reserved by metadata and remain **undownloaded, unopened and unrun**.

Sources and attribution: [GMDCSA24 v2.1](https://github.com/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/tree/v2.1) (MIT), [ASSIST-IoT multimodal dataset](https://github.com/ASSIST-IoT-SRIPAS/multimodal-fall-detection-dataset) (CC BY 4.0), [MOT17](https://motchallenge.net/data/MOT17/) (CC BY-NC-SA 3.0, local noncommercial research). Source URLs, hashes and labels are in `datasets/phase1c/validation.json`; preserved license material is in `third_party/` and `data/sources/mot-license.html`. No full multi-gigabyte archive was needed.

Coverage includes forward/jogging, sideways, backward/seated, faint-like vertical collapse, knees-to-forward fall, partial visibility, bending/crouching, intentional lying, standing up, walking away, near-camera pedestrians, crossing and overlap. ASSIST videos contain two views of the same demonstrator; these are not multi-person fall examples. Slow falls, systematic toward/away foreshortening, real immediate recovery, partial-recovery-then-immobility and a fall during multi-person crossing remain inadequately covered. Do not count unit-test boxes as real footage.

The first full validation run used the frozen Phase 1B decision thresholds (.3 detector confidence, 640 input, improved tracking/temporal logic). Subsequent experiments used this validation set; it is now seen validation, not an untouched final test. No threshold was lowered.

| Clip | Fall label | Candidate | Review requested | First candidate s | Publisher-onset latency s |
|---|---|---|---|---:|---:|
| fresh_gmd4_Fall_03 | True | True | False | 3.017 | 1.317 |
| fresh_gmd4_Fall_07 | True | True | False | 2.616 | 0.216 |
| fresh_gmd4_Fall_08 | True | False | False | — | unknown/not detected |
| fresh_gmd4_Fall_11 | True | True | False | 1.610 | 0.410 |
| fresh_gmd4_ADL_14 | False | False | False | — | unknown/not detected |
| fresh_gmd4_ADL_17 | False | False | False | — | unknown/not detected |
| fresh_assist_02_fall_backward | True | True | True | 3.200 | unknown/not detected |
| fresh_assist_04_forward_fall_jogging | True | True | True | 3.000 | unknown/not detected |
| fresh_assist_05_vertical_fall_faint | True | True | True | 3.400 | unknown/not detected |
| fresh_assist_07_fall_to_knees_forward | True | True | True | 2.000 | unknown/not detected |
| fresh_assist_01_walking_slowly | False | False | False | — | unknown/not detected |
| fresh_assist_12_sitting_laying_down_quickly | False | True | False | 2.800 | unknown/not detected |
| fresh_assist_13_bending_at_knees | False | False | False | — | unknown/not detected |
| fresh_assist_14_bending_wo_knees | False | False | False | — | unknown/not detected |
| fresh_mot17_09 | False | False | False | — | unknown/not detected |

## Localization

Independent sparse audit: 84 preselected raw snapshots, 83 visible-person instances (one empty frame). Boxes were drawn by one AI visual annotator before inference, approximately ±6 pixels on 320-pixel previews, without detector overlays. These are exploratory visible-body references, not expert-reviewed ground truth. ASSIST main-view ROIs exclude inset predictions from localization scoring, while inference still processes the full composite. The annotations and their SHA-256 are retained.

| Measure | Sparse GMD/ASSIST | MOT17 subset |
|---|---:|---:|
| Matched / reference instances | 78/83 | 342/397 |
| Recall IoU ≥ .50 | 0.9398 | 0.8615 |
| Recall IoU ≥ .75 | 0.8916 | 0.6826 |
| Mean IoU, matched only | 0.8787 | 0.8203 |
| ID changes | 3 | 37 |
| Reacquisition fragments after misses | 3 | 12 |
| Longest missed-sample span, seconds | 2.0000 | 1.4000 |
| Mean center error / reference height | 0.0423 | 0.0306 |
| Reference-relative center jitter | 0.0468 | 0.0316 |
| Reference-relative log-area change | 0.0841 | 0.1311 |

Sparse descent localization: **11/11**; ground/prone: **27/28**. MOT visibility ≥ .5: **284/301**; visibility below .5 but above zero: **58/96**. Only marked class-1 pedestrians with nonzero visibility are scored. Publisher boxes are clipped to the image, then scaled to processing coordinates. This is a local 5 Hz audit, not official MOTChallenge MOTA/IDF1/HOTA.

ID changes mean a reference identity receives a different associated tracker ID on successive matched observations, including after a gap. Fragmentation means matched → missed → matched. Dense MOT detections miss 55 reference instances; sparse snapshots miss 5. Per-identity missed counts and spans are in `baseline/localization.json`. Longest spans measure first-to-last missed sample (one miss has span zero); they are lower bounds, not exact continuous gaps. The sparse 2.0-second span cannot establish what happened between snapshots. Jitter is change in reference-relative center error, not real subject motion. Matched-only quality excludes misses and must be read with recall.

MOT unmatched predictions are not reported as false positives because ignored classes/regions were not scored for precision. Main-view sparse unmatched boxes are a diagnostic count, not a deployment false-positive rate. Overlapping reference boxes and sparse annotation uncertainty can affect these metrics.

## Failure attribution and fall detection

- **A — absent evidence:** GMD forward fall frame 72 (2.414 s) has no detection during the ground transition. Bending frames also have no usable person box.
- **B — association:** the partially visible GMD fall has an ID change despite matching all six sparse reference boxes; the MOT sequence has 37 ID changes and 12 reacquisition fragments. Matching all sparse boxes does not prove continuous tracking.
- **C — localization/spurious boxes:** three bending snapshots contain boxes elsewhere with zero overlap with the reference person. These are a missed person plus spurious localization, not evidence that the person was correctly detected.
- **D — temporal/geometry:** the seated backward fall matches all six references and retains track 1, but net drop reaches only .168 reference heights at 3.012 s; later descent averages about .134 heights/s. The frozen .18/.15 transition gates reject it. The intentional rapid lying clip satisfies fall-like geometry and triggers candidates at 2.8 s in both camera views.

**Fall recall 7/8 (87.5%); false-positive non-fall clips 1/7 (14.3%).** False candidates remain counted after dismissal. There are two false candidate packets in the one lying clip because of the composite views; no false human-review escalation. Three detected GMD falls have publisher-onset delays **0.216–1.317 s** (median 0.410 s). The four ASSIST event onset labels remain unknown, so no invented onset latency is reported. Review and fall-event detection are separate.

Lowering a threshold would not resolve intention ambiguity and could increase false positives. These results do not justify declaring localization stable or adopting pose estimation without a separate measured comparison.

## Recovery

Real ASSIST backward fall: candidate at **3.2 s**, review at **14.8 s**, observed recovery/dismissal on the same track at **17.8 s**. Raw sequence inspection shows prolonged lying followed by rising; this is delayed recovery, not immediate recovery. The other three ASSIST falls reach review at 7.2, 7.2 and 5.6 s. Intentional lying produces a false candidate, and one view later dismisses it at 7.8 s; the other view remains an unresolved candidate.

Immediate recovery and continuous immobility have existing unit regressions; new tests verify that partial movement resets the stationary clock without erasing the fall and that initial ground posture alone does not create a fall. Real immediate and partial recovery remain coverage gaps. A raw-video stand-up is not guaranteed to be recognized if identity or geometry changes.

## Multi-person and conservative experiments

MOT provides real pedestrian overlap/crossing and near-camera scale changes, but no person falling. A coherent synthetic tracker→temporal→tool test verifies A falls, A becomes absent, B walks nearby, and B retains its own ID, velocity and non-fall history. An explicit ambiguous-box test demonstrates why choosing an owner is unsafe; no box-only tracker can infer identity from indistinguishable evidence. These unit tests do not establish the real critical multi-person fall branch.

Short-gap ambiguity rejection was evaluated by replaying recorded real MOT detections (baseline ID sequence asserted identical). It changes **37 → 92 ID changes**, with **12 → 12 fragments** and unchanged localization. Rejected as default; retained only as an explicit experimental tracker argument. It protects the synthetic ambiguous ownership case by starting a fresh history, at a severe continuity cost. No counterfactual FPS or fall recall is claimed.

Paired detector-only comparison on the same 84 raw snapshots (same model, confidence .3, input 640; no tracker or fall evaluation):

| Detector configuration | Recall @.5 | Matched IoU | Unmatched main-view boxes | Detector FPS | p50 ms | p95 ms | Process peak MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| YOLOX fallback | 78/83 | 0.879 | 7 | 1.49 | 528.2 | 1462.4 | 191.0 |
| YOLOX all_views | 79/83 | 0.880 | 35 | 0.67 | 1442.3 | 1729.2 | 193.1 |

All-view inference adds only one reference match, leaves ground recall at 27/28, increases unmatched boxes from 7 to 35, and worsens center/area stability. Rejected as default. `rotation_all_views=False` remains selected. Snapshot timing excludes pipeline tracking, motion and evidence; process peaks are cumulative within the paired process. No new model or dependency was added.

## Full-pipeline performance

Baseline run `20261028T144937925673`: **1.46 FPS**, pooled **528.6 ms p50 / 1443.8 ms p95**, wall-weighted **184.8% of one CPU core**, **228.9 MiB process peak**. OpenCV CPU, 2 threads, 5 Hz source sampling. Different footage explains differences from Phase 1B; this is not evidence of an optimization speedup. No competing DNN benchmark ran concurrently.

| Stage | Total seconds | Share of measured stages |
|---|---:|---:|
| preprocessing | 0.641 | 0.14% |
| detector | 455.600 | 97.73% |
| tracking | 0.079 | 0.02% |
| motion | 4.402 | 0.94% |
| temporal_and_logging | 0.224 | 0.05% |
| evidence | 2.309 | 0.50% |
| visualization | 2.906 | 0.62% |

The detector dominates measured stage time. It includes tensor preparation and rotation passes; decode/startup/final serialization are outside stage buckets. Motion is summed across people; evidence includes tool/packet I/O, visualization includes debug-video writes. Overall throughput includes source processing overhead. The next speed investigation should target detector execution only after perception quality improves. A 5 FPS operating target remains unmet.

## Acceptance gate and regression protection

| Preregistered engineering goal | Observed gap |
|---|---|
| Detect all 8 falls | 1 missed |
| Zero false-positive non-fall clips | 1 of 7 falsely flagged |
| Localize every visible reference at IoU .5 | 5/83 sparse and 55/397 MOT misses |
| Zero identity changes/history transfer | 37 MOT ID changes; ownership guarantee absent |
| Continuity supporting .5 s motion gate | 1.4 s MOT missed-sample span |
| Critical real multi-person/recovery branches covered | Falling during overlap, immediate/partial recovery missing |
| 5 FPS processing target | Measured 1.46 FPS |

Regression validation: **54/54 tests passed in 99.895 seconds**, with no skips (`docs/test-results-phase1c.txt`). Existing 44 tests are retained; 10 new mechanism/audit tests cover matching, jitter semantics, missing spans, optional all-view behavior, short ambiguous ownership, nearby-person occlusion, partial movement, initial ground state, compact descent limitations and intention ambiguity. Known-limit tests document behavior; they are not claims that those limitations were fixed.

Formal interface: `docs/perception-contract.md`; schema exports under `docs/schemas/`. Runtime scores are heuristic, IDs are run-local, missing evidence is unknown, and no tracking confidence is fabricated.

## Artifacts and remaining risks

Full observations, empty-sample diagnostics, debug videos, evidence packets, timeline CSVs, state transitions and annotated/original representative frames: `data/evaluation/20261028T144937925673/<clip>/`. Each clip has `contact.jpg` and `diagnostic-frames/`. Independent raw sheets: `data/phase1c-annotation/`. Aggregate measurements and experiments: `evaluation/phase1c/`. Prior Phase 1B report/results are preserved in `evaluation/phase1c/phase1b-*`.

Risks: identity transfer during overlap; sparse approximate annotations; staged mats/beds and composite cameras; no natural multi-person fall; incomplete recovery/foreshortening coverage; intentional-lying ambiguity; seated slow descent miss; physical camera not tested; throughput below target. No numerical deployment-risk acceptance has been agreed. The final reserve remains untouched because the fresh gate failed.

**INCOMPLETE — perception still needs work**. Single highest-priority blocker: **identity continuity through overlapping people**.
