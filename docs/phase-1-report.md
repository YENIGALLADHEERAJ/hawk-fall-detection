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

<!-- PHASE1C END -->

# Phase 1 execution report — updated 2026-10-27

## Phase 1B findings — 2026-10-27

**INCOMPLETE — perception still needs work.** The two previously missed falls are now
detected, but the reused five-clip set cannot establish generalization or live readiness.
The original 2026-10-26 results below are preserved as historical baseline results.

The fresh baseline reproduced 0/2 falls and 1/3 false-positive non-fall clips. The
diagnostic timelines show detection gaps of 0.602 and 1.203 seconds during the falls,
exceeding the original 0.5-second track expiry and temporal reset. At the next observed
horizontal box, the original state machine had lost the preceding upright/descent
history. Candidate scoring and recovery were not reached. The false positive was
a person crouching/bending while getting up; stale velocity and aspect-ratio jitter
were combined without requiring net downward movement.

| Configuration | Falls detected | False-positive non-fall clips | Final dismissed candidates | Aggregate FPS | Pooled p50 / p95 ms |
|---|---:|---:|---:|---:|---:|
| A: Original baseline | 0/2 | 1/3 | 1 | 1.10 | 702.1 / 2022.2 |
| B: Tracking only | 0/2 | 1/3 | 1 | 1.24 | 548.1 / 1508.2 |
| C: Temporal only | 0/2 | 0/3 | 0 | 0.97 | 816.7 / 2252.8 |
| D: Tracking + temporal | 2/2 | 0/3 | 0 | 0.92 | 697.1 / 2327.2 |
| E: Initial D + low-score continuation (rejected) | 2/2 | 0/3 | 0 | 1.13 | 572.7 / 1945.3 |

All five use real CPU inference and unchanged clip hashes/labels. A–D consume identical
sampled detections, verified record by record. D creates candidates at 3.813 and 3.007
seconds (1.313 and 1.207 seconds after publisher onset labels); E moves the second to
2.004 seconds (0.204-second latency). None reaches human review. D's main-track coverage
improves from 16/45 to 34/45 sampled frames and from 10/31 to 15/31; distinct IDs fall
from 8 to 5 and 5 to 2. These are proxies, not annotated tracking-accuracy metrics.

Selected default: D. Identity retention is now 1.5 seconds, prediction is capped at
0.25 seconds, area/ambiguity gates constrain reattachment, and missing boxes are never
emitted. The new temporal rule combines net downward displacement, downward speed,
upright history, height loss and horizontal geometry. Missing frames reset stationarity;
they may support only an uncertain endpoint transition, never observed immobility.
Recovery requires upright geometry plus upward motion. Fall events and prolonged
immobility have separate structured fields. No clip names or annotations enter inference.

E is opt-in: weak detections can continue an existing track but cannot create identities
or establish immobility. It reduces frames with no detections from 9 to 3 and 16 to 7
in the two falls. However, visual inspection finds an oversized box over much of the
room at the earlier Subject 3 alert (confidence 0.276, approximately 482x203 pixels).
More raw detections do not establish better localization. E is rejected as the default;
its earlier latency is not trusted as an earlier observation of the fall. E used the
initial temporal logic, before the development-squat correction. Detector weights are unchanged;
no new dependency, pose model, training, cloud, frontend or agent layer was introduced.

**44/44 tests pass**: the original 22 plus 18 mechanism regressions and four additional
real-video integrations. Coverage includes multi-person association, missing-frame
reattachment/ambiguity, expiration boundaries, new fall after recovery, immediate recovery,
continuous immobility, gap resets, sitting/crouching/partial visibility, stale velocity,
cross-person history isolation, tool-window boundaries and weak-detection association.
Real replay still demonstrates fall followed by immobility. Output:
[Phase 1B test log](test-results-phase1b.txt).

A broader full-inference run of the initial combined logic retained 10/11 development
falls but introduced 2/13 false-positive clips: an ordinary squat (`clip_06`) and
chair sitting (`gmdcsa_ADL_13`). Both came from an optional compact-low geometry
branch without horizontal posture. That branch was removed. Final temporal replay
of the recorded real detections/motion across all 25 clips yields 10/11 falls and
0/13 false-positive clips; this is a recorded-evidence regression, not a second
full detector benchmark. Both negative clips then passed full-inference integration
tests. Replay candidate timestamps also agree exactly with the final full held-out
run. Source hashes and scope are in
[development replay results](../evaluation/phase1b/development-final-replay.json).

D averages 190.3% of one CPU core; end-of-clip working set is 150.9-171.1 MiB and
process-lifetime peak reaches 229.2 MiB. All variants remain offline prototypes, well
below live 5 FPS. Sequential single runs are affected by scheduling/thermal variation;
timing differences do not establish a tracker speedup. Full per-clip metrics, CPU/memory,
diagnostic CSVs, original/annotated frames, trajectories, decisions and debug videos:
[Phase 1B evaluation](../evaluation/holdout/report.md),
[machine-readable ablation](../evaluation/phase1b/ablation.json).

Highest-priority next fix: improve actual detector coverage through descent/prone poses
and validate that change on fresh untouched subjects. The low-score experiment shows
that simply accepting more boxes is insufficient; gaps and poor localization prevent strong
identity claims. Natural multi-person interactions, true fall/recovery, severe low light,
camera-motion robustness and physical-camera reconnect validation also remain open.
No Phase 2 work is authorized by these regression results.

---

## Historical Phase 1 baseline — 2026-10-26

The real perception path is implemented and demonstrated. **Full Phase 1 validation
is not complete:** natural multi-person footage, fall-followed-by-recovery footage,
dedicated poor-light footage and physical-camera disconnect/reconnect remain unvalidated.
No frontend, AWS deployment or LLM agent was added.

## What runs

Recorded video → sampled frames → real OpenCV 5 YOLOX inference → one-to-one tracking
→ ROI motion and box geometry → temporal state → bounded evidence tools → local
candidate packets, JSON trace and annotated debug video. Pydantic validates canonical
schemas; JSON Schema exports are in `docs/schemas/`.

Selected detector: Apache-licensed OpenCV Zoo YOLOX, with original-view inference
followed by rotated-view inference only when no person is detected. A 640×640 input
was retained for the evaluated configuration because 320 lost prone-person detections.
This is a compatibility/quality choice, not the fastest model. MediaPipe person,
NanoDet and Ultralytics alternatives were compared qualitatively, not empirically
benchmarked against YOLOX. See [model selection](model-selection.md).

Selected tracker: gated overlap plus velocity-predicted centroid association. It
avoids new dependencies and maintained one identity through the proof clip. It is
not reliable enough to claim identity continuity at crossings or long occlusions;
IDF1/HOTA remain unavailable without identity annotations.

Selected motion: centroid velocity plus Farneback flow in a normalized 96×96 ROI;
frame difference is retained as an auxiliary measurement. Flow cost is small relative
to DNN inference. Pose was not needed to demonstrate this loop, but geometry alone
misses foreshortened/seated falls and may need pose or a different temporal classifier.

## Actual proof

Unmodified GMDCSA24 Subject 1 Fall/11, with source attribution and SHA-256 in
[the manifest](../datasets/manifest.json):

1. Person detected and tracked as ID 1.
2. Candidate created at 2.021 seconds.
3. `analyze_temporal_window` executes on observed history.
4. At 6.064 seconds, continuous low-motion duration reaches 1.617 seconds: IMMOBILE.
5. `inspect_region` executes and the incident evidence is updated.

The clip does not satisfy the separate 2.5-second continuous-stationarity review rule.
No automatic confirmation or medical diagnosis is produced.

Saved [annotated frame](../data/runs/proof-rotation/incidents/incident-0001-000060/annotated.jpg),
[observation evidence](../data/runs/proof-rotation/incidents/incident-0001-000060/evidence.json),
[trace](../data/runs/proof-rotation/trace.json), and
[debug video](../data/runs/proof-rotation/debug.avi).
The final evaluation independently reproduced the IMMOBILE transition; the integration
test also checks it using real DNN inference, not mocked detections.

## Actual footage results

25 clips processed; 24 have usable binary event labels (11 positive, 13 negative).
One very short clip with a source fall label ends before a complete visible fall and
is excluded. This is a small development set; its results do not establish generalization.
The separate subject-held-out evaluation below exposes substantially worse performance.

| Method | Fall candidates / positive clips | False-positive negative clips |
|---|---:|---:|
| Immediate horizontal-box baseline | 10 / 11 | 4 / 13 |
| HAWK temporal policy | 10 / 11 | 0 / 13 |

Candidate recall is 90.9% for both on this set. HAWK reduced candidate false positives
here, without reducing measured candidate recall. This does not establish general
safety performance. No tested clip reached the final human-review rule, so these
numbers must never be presented as verified-incident recall or escalation precision.
Publisher-annotated onset to candidate latency on six longer detected falls was
0.324–1.021 seconds of video time; replay wall-clock latency is much longer.
The negative footage covers only about 59.6 seconds. Hour-normalized false-alert rates
in JSON are arithmetic summaries of that tiny exposure, not deployment forecasts.

See [evaluation report](../evaluation/report.md) and [raw results](../evaluation/results.json).

### Additional subjects, unchanged thresholds

Five clips from GMDCSA24 Subjects 2 and 3 were evaluated with the existing 640-input,
5-sampled-FPS configuration, without retuning. They are separate subjects but share
the dataset/site; this is not independent site validation. Four publisher-labeled
Night clips remain visibly illuminated and do not establish severe-low-light accuracy.

| Method | Fall candidates / positive clips | False-positive negative clips |
|---|---:|---:|
| Immediate horizontal-box baseline | 2 / 2 | 2 / 3 |
| HAWK temporal policy | 0 / 2 | 1 / 3 |

**Both falls were missed.** Detection gaps and track fragmentation interrupted the
fall transition; later horizontal detections had no earlier descent history. The
baseline count is clip-level presence, not accurate onset detection (one clip has
a baseline alert before its labeled onset). Reduced false-positive counts here do
not compensate for the loss of recall. No tested clip reached human review.

The lying-to-standing non-fall clip produced a false candidate at 6.435 seconds,
then genuine observed recovery dismissed it at 6.837 seconds. This demonstrates
the dismissal path on real footage, but does not validate a real fall followed by
recovery. The candidate still counts as a false positive. Negative exposure totals
only 27.1 seconds; normalized hourly rates are not deployment estimates.

Achieved processing speed was 0.63–1.22 FPS; per-clip p50 latency was 684.6–1931.7 ms
and p95 was 1884.3–2558.7 ms. These harder clips run slower than the earlier short
benchmark, reinforcing the offline operating limit. Full results and per-clip
configuration/metrics: [held-out report](../evaluation/holdout/report.md),
[held-out JSON](../evaluation/holdout/results.json). Failure details and sampled
frames are in [the failure gallery](failure-gallery.md). No thresholds were changed
after these results.

## Actual performance

CPU, two OpenCV threads, including debug/evidence encoding. Short-clip benchmark:

| Detector input | Sampling cadence | Achieved processing FPS | p50 / p95 frame latency |
|---|---|---:|---|
| 320 | 5 FPS | 3.14 | 212.4 / 537.1 ms |
| 320 | 10 FPS | 5.20 | 143.2 / 335.9 ms |
| 320 | 15 FPS | 4.67 | 126.8 / 386.1 ms |
| 320 | 30 FPS | 5.10 | 127.3 / 369.9 ms |
| 640 | 5 FPS | 1.95 | 474.1 / 521.4 ms |

Selected operating mode: offline replay at 5 sampled frames per video second, with
640 input for the current quality tests. This is **not live 5 FPS**. Difficult clips
can require three inference passes and run more slowly. Sampling and compute FPS are
separate. The shorter 320 tests have different evidence workloads and startup costs;
they do not establish a monotonic or sustained performance curve.

96×96 motion kernel p50: frame difference 0.0043 ms; Farneback 2.2392 ms. These measure
cost, not comparative event accuracy. CPU usage was 189.6–197.1% of one core. End-of-run
working set was 118.9–159.6 MiB; process-lifetime peak reached 261.0 MiB across sequential
runs and is not an independent per-run peak. See [benchmark report](../benchmarks/report.md).

## Tests and limitations

**22 tests passed**, including real video → detector → tracker → candidate → evidence
and a separate real fall → immobility replay. Unit tests cover schemas, geometry,
velocity, multi-person association, history expiry, missing evidence, low-FPS continuity,
sitting, recovery, motion-quality gating and tool bounds. Full output:
[test-results.txt](test-results.txt).

The additional tests cover stale historical recovery, file timestamps/EOF, bounded
reconnect, fresh frames after reconnect and a stalled capture worker. A historical
recovery can no longer dismiss a new candidate: dismissal requires matching current
track/timestamp evidence and the current recovery action. Webcam capture now runs in
a separate process with bounded reconnect and timeout handling. The capture tests use
transport fixtures; a physical camera was not activated or tested.

Remaining failures/risks:

- Seated fall toward camera (`clip_05`) missed: box shape does not horizontalize.
- Alternate-view fallback is costly and does not run if another person is already detected.
- Tracking fragments on some clips; crossings and natural multi-person interactions unvalidated.
- Camera shake can contaminate flow; image quality is not a medical observation.
- Real fall/recovery, dedicated low-light and physical-camera reconnect tests remain missing.
- Frame-index/FPS timestamps assume regular recorded cadence; VFR timing is unverified.
- Tool pass counts and inputs are bounded; DNN/tool timeout cancellation is not implemented (capture cancellation is).
- Local storage is capped per run, but accumulated runs need manual retention cleanup.

See [failure gallery](failure-gallery.md). A zero false-positive count in this development
subset must not be interpreted as zero risk. No model was trained or fine-tuned.

## Next step

Before declaring every Phase 1 acceptance item closed, add licensed/consented natural
multi-person and fall/recovery clips, verify live-source failure handling if required,
and improve detection/association through falls using development footage. Preserve
this held-out result; any changes informed by these failures need a fresh untouched
test set. The missed seated-fall case also remains unresolved.
Then Phase 2 should wrap the existing typed tools in a bounded agent planner with
strict tool authorization, budgets and timeout handling, while keeping deterministic
sufficiency and human-review rules. The agent must not fabricate missing vision.

Git remains uncommitted because no author name/email is configured. No identity was
invented. Artifacts and source are saved in the working tree; downloaded media/models
are ignored by Git and restored using `scripts/fetch_assets.py`.

## Addendum 2026-11-15 — re-run on new hardware

Re-run on a Ryzen 9 9955HX / RTX 5060 machine; see [hardware-rtx5060.md](hardware-rtx5060.md). All detection, localization and identity results are identical to this report. Only speed changed: 40.4 FPS on the GPU backend, 15.8 FPS on 32 CPU threads and 5.1 on the original 2-thread setting (the 1.46 FPS figure above was the old machine). The 5 FPS target is met; the INCOMPLETE verdict and identity-continuity blocker stand.

## Addendum 2026-11-15 — identity continuity experiment

An optional colour-histogram appearance cue (`--identity-tracking`, off by default) reduces ID changes on three MOT17 pedestrian clips from 88 to 60 in total and track-owner changes from 72 to 52, with no clip worse than baseline and no change in fall recall or false-positive counts on 45 clips. Only one of the three clips was unseen at selection time; optimal assignment, tried first, regressed on one clip and is kept only as a separate flag. The detector still misses 51-63% of people in the two far-field scenes, no fall occurs in any MOT17 clip, and owner changes are not zero, so the identity blocker is reduced, not resolved. See [identity-tracking.md](identity-tracking.md).

## Addendum 2026-11-15 — real multi-person fall clips

The MPFDD public subset (28 staged clips, license not stated, local use only) was run with the frozen configuration: 17 of 22 falls raised a candidate and 0 of 6 non-fall clips did; fall candidates stayed on the faller's track in all 7 detected single-faller clips, including one inspected case where a bystander walked across the fallen person. The five misses are the known geometry/temporal-gate classes. No clip reached review, and these clips do not test crowds. See [multi-person-validation.md](multi-person-validation.md). The previously open "fall during multi-person crossing" gap is partly addressed by staged footage; it is not closed.
