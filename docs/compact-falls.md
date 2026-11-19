# Compact falls: why they were missed, and an optional fix — 2026-11-16

## Why three of the five MPFDD misses happened

The fall gate in `vision/temporal_v2.py` requires, besides a horizontal box and height loss, a **net center drop of at least 0.18 upright heights** at an average speed of at least 0.15 heights/s. A person who collapses in place shrinks the box around its middle, so the center barely moves even though the box is clearly lying down.

Traced frame by frame from the recorded diagnostics (`data/evaluation/20261115T182220678563`):

| Clip | Evidence at its best frame | Gate that failed |
|---|---|---|
| S2-F1-3 | w/h 1.87, height ratio 0.32 | center drop 0.10 to 0.15 (needs 0.18); speed 0.07 to 0.11 (needs 0.15) |
| S1-F1-2 | w/h 1.25, height ratio 0.54 to 0.62 | center drop 0.09 to 0.11 |
| S1-F1-3 | w/h 1.49 only at 8.8 to 10 s, under a new track | no upright reference left (clip end) |
| S2-F1-5, S3-F1-3 | box never clearly horizontal (kneeling, seated) | horizontal gate; not addressed here |

The bottom edge cannot replace the center: in S2-F1-3 the lying box's bottom is about 0.2 heights *above* the standing feet.

## Option: `compact_collapse_height_ratio` (default off)

`--compact-collapse-ratio R` (or `Config.compact_collapse_height_ratio`). When the box is horizontal, its height has fallen to `R` times the upright height or less, and its center did not rise, the transition is accepted without the center-drop and speed gates. Everything else (upright reference, horizontal geometry, recovery, immobility, human-review timing) is unchanged. With the option unset, behavior is identical to before (test `test_off_by_default_...`).

## Replay on recorded detections (no new inference)

`python -m evaluation.replay_temporal <results.json> --output <file> --set compact_collapse_height_ratio=<R>`. Recorded GPU-run detections and motion; results in `evaluation/compact/`.

| Set | Off | R = 0.7 | R = 0.6 | R = 0.5 | R = 0.4 |
|---|---|---|---|---|---|
| Development (10 falls / 0 FP clips) | 10 / 0 | 10 / **2** | 10 / 0 | 10 / 0 | 10 / 0 |
| Fresh (1 FP clip before the change) | 7 / 1 | 8 / 1 | 8 / 1 | 7 / 1 | 7 / 1 |
| Holdout | 2 / 0 | 2 / 0 | 2 / 0 | 2 / 0 | 2 / 0 |
| MPFDD (22 falls, 6 no-fall clips) | 17 / 0 | 19 / 0 | **19 / 0** | 18 / 0 | 18 / 0 |

Values are falls detected / clips with a false candidate. R = 0.6 is the loosest tested value with no false-positive clip on any set; 0.7 let in two development false positives. At 0.6 the change recovers **S1-F1-2, S2-F1-3 (MPFDD) and `fresh_gmd4_Fall_08`**, makes candidates fire 0.2 s earlier on 6 existing detections, and adds a second candidate event on two clips (`fresh_assist_04`, `S2-F2-3`). No clip lost its candidate. The one false-positive clip in the fresh set was already there and is unchanged.

## Limits of this evidence

- **R was chosen after looking at the MPFDD misses**, so MPFDD (+2) is not a held-out measurement of the fix. The only independent signal is `fresh_gmd4_Fall_08` (+1) and the absence of new false positives on 19 no-fall clips (13 earlier, 6 MPFDD).
- The threshold sits near a cliff: 0.7 adds false positives. Treat 0.6 as a starting point that needs fresh no-fall footage (squats, sitting down, bending, picking things up, getting onto a bed) before it becomes a default.
- The replay uses recorded detections; a full-inference run with the flag (below) gave the same counts.
- Still missed: falls that end kneeling or seated (S2-F1-5, S3-F1-3) and falls at the very end of a clip (S1-F1-3). These need different evidence than box geometry.
- Heuristic evidence, not a calibrated probability. A fall candidate is a request for evidence or human review, not a diagnosis.

Defaults and frozen thresholds are unchanged. Tests: 69 pass (5 new, `CompactCollapseTests` in `tests/test_phase1b.py`).

## Full-inference confirmation (GPU, `--compact-collapse-ratio 0.6`)

Run after the replay, all four sets, results in `evaluation/compact-full/`. Falls detected / clips with a false candidate: MPFDD 19/22, 0/6; dev 10/11, 0/13; holdout 2/2, 0/3; fresh 8/8, 1/7. These match the replay counts exactly. The one fresh false-positive clip is `fresh_assist_12_sitting_laying_down_quickly`, the same clip that was already a false positive without the flag. The limits above still hold: R was chosen after seeing MPFDD, and no new no-fall footage was tested.

## Independent no-fall check and exposure analysis (2026-11-16)

**Crowd clips not used to choose R.** `datasets/crowd_negatives.json` (MOT17-02 and MOT17-04, crowded pedestrians, no falls, about 10 s each at 5 Hz; CC BY-NC-SA 3.0). Full inference, GPU, flag off versus 0.6 (`evaluation/compact-crowd/`): **0 fall candidates in both**, identical. MOT17-09 was already in the fresh set (0 candidates).

**How much did the flag actually have a chance to fire?** Across all 29 no-fall clips (3,397 person-observations), only **19 observations in 4 clips** were horizontal with a height ratio of 0.6 or less: `gmdcsa_ADL_01/02/03` (12 observations) and `fresh_assist_12` (7, the existing false positive). None of the 12 GMDCSA ADL observations became a candidate. In all 12 the box center was *rising* (net drop -0.03 to -0.17, w/h 1.7 to 4.3), so the `drop >= 0` guard is what rejects them. That guard is load-bearing, and one frame (ADL_02 at 1.4 s) is only 0.03 below it.

So the no-false-positive result has a narrow evidence base: **the flag was exercised by about 19 observations**, and the margin on 12 of them is the sign of the center movement. A wider no-fall set that includes people lying down, stretching out or sitting on beds, and a camera that is not fixed, is still needed before this can be recommended as a default.

## 21 more no-fall clips (GMDCSA24 Subjects 2-4 ADL, not used for tuning)

`datasets/gmdcsa_adl_extra.json`, files in `data/sources/gmdcsa-adl-extra/` (MIT repository licence; sizes checked against the published tree). Full inference, GPU, flag off versus 0.6 (`evaluation/compact-adl-extra/`): **0 false candidates in both (0/21)**, identical. The older immediate-alert baseline flags 7 of the 21, which the temporal logic does not.

**Exposure was zero:** none of the 1,036 person-observations in these clips was horizontal with a height ratio of 0.6 or less, so these clips show the flag does not fire on ordinary activity, but they did not stress its decision rule. The stress evidence is still the 19 observations described above. No-fall footage with lying down, stretching out or sitting on a bed is what would test it.

## Targeted stress test: sleeping, lying and stretching clips (GMDCSA24 ADL)

`datasets/gmdcsa_lying.json`, 11 clips chosen from the publisher's activity labels as the cases most likely to look like a compact collapse (sleeping on a bed or floor, sitting then lying, a stretching pose); files in `data/sources/gmdcsa-lying/` (sizes verified; MIT repository licence) plus one already-local clip. Not used to choose R. Full inference, GPU, flag off versus 0.6 (`evaluation/compact-lying/`):

- **Identical results: 1 false-candidate clip of 11 in both.** The flag neither added nor removed anything.
- **The one false candidate (`S2 ADL_08`, the "pyramid pose" stretch, at 7.4 s) is not caused by the flag.** It passes the original gates (center drop 0.22, speed 0.15, height ratio 0.62, w/h 1.76), so it is a pre-existing false positive of the frozen logic that I had not seen before. It is a known gap now, not fixed.
- **Exposure: 16 observations** reached the flag's zone (horizontal, height ratio at or below 0.6), in four clips of a person lying down onto a bed (S2 ADL_03, S4 ADL_10/15/16). **None became a candidate.** All 16 have a rising box center (net drop -0.06 to -0.19, w/h 1.35 to 3.1), so the `drop >= 0` guard rejected them, with a margin of at least 0.06 here.

Combined with the earlier set, the flag has now been exposed to **35 no-fall observations in 8 clips with no activation**, all rejected by that one guard. Caveat: all of this footage is from one dataset, one room and one camera angle, where the bed is higher than the floor so a person lying onto it makes the box center rise. A floor-level sleeper, a low sofa or a different camera height could behave differently, and the guard would then be the only barrier. The recommendation does not change: leave the flag off by default and validate on other rooms and cameras before relying on it.

### Anatomy of the `S2 ADL_08` false candidate (pre-existing, flag-independent)

Timeline from `evaluation/compact-lying/off`: the person bends deep forward (box height 347 to 212 px, width/height 1.0 to 1.21) between 6.8 and 7.4 s; the transition is accepted at 7.4 s on the original gates. The posture is held for about 2 s with enough movement that continuous stationarity is never proven (state stays "stationarity unproven", longest stationary run 0.4 s), so it never reached immobility or a human-review request. When the person stands up the estimator dismisses it (`observed_upright_upward_recovery`, 9.6 s). Net effect: a fall candidate of about 2 s that clears itself, no escalation. A bend and a fall are both "box shrinks, widens, stays low" in 2-D box geometry, so separating them needs pose or motion evidence beyond the box, not a threshold tweaked on one clip. Left unchanged; listed as an open item.
