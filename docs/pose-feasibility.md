# Pose keypoints as extra evidence: feasibility probe — 2026-11-19

**Status: exploratory. Nothing in the pipeline uses pose; no thresholds were tuned; the frozen configuration is unchanged.**

## Why

The remaining misses and the one forward-bend false candidate are cases where the 2-D person box looks the same for different events (see `docs/multi-person-validation.md` and `docs/compact-falls.md`). Body keypoints can tell a person whose hips drop to the floor from one who bends with the hips still high.

## Model

RTMPose-m (COCO 17 keypoints, body7, 256x192, SimCC) from the OpenMMLab release, via the Hugging Face mirror `Tau-J/RTMPose` (repository tagged Apache-2.0). 50.8 MB zip, extracted with path checks to `data/models/pose/` (git-ignored). `end2end.onnx` SHA-256 prefix `5c0a4bf67953e6d2`. **Licence caveat:** the repository tag is Apache-2.0, but the licences of the datasets the weights were trained on were not checked; do that before any commercial use.

## Probe

`python -m evaluation.pose_probe <results.json> <clip ids...> --output <file>` (`evaluation/pose_probe.py`). It crops each tracked person from the recorded box, runs the model, and reports, per observation:

- `hip_height` = (mean ankle y minus mean hip y) / largest box height seen so far for that track. About 0.33 to 0.41 standing in these clips; near 0 when the hips are at ankle level.
- `torso_angle` = shoulder-to-hip line against vertical (0 upright, 90 horizontal, above 90 head below hips).
- Keypoints under a 0.3 peak-score floor (not calibrated) are dropped; a missing feature is `None`, never guessed.

Outputs: `evaluation/pose/lying.json`, `evaluation/pose/mpfdd.json`.

## What it showed (6 clips, observed values; no thresholds fitted)

| Clip | Box evidence | Hip height | Torso angle |
|---|---|---|---|
| `S2 ADL_08` forward bend (false candidate) | w/h 1.2, height ratio 0.61 | **stays 0.35 to 0.41** (hips never drop) | 84 to 112 deg |
| `S2-F1-5` fall ending kneeling (missed) | w/h never above 1.05 | **0.33 to 0.07 in about 0.8 s** (3.2 to 4.0 s), stays at 0.06 to 0.22 | 2 to 18 deg |
| `S1-F1-3` (missed) | box gate saw nothing until the clip end | 0.33 at 3.2 s, **0.20 at 4.0 s**, 0.11 by 9 s | 52 to 82 deg |
| `S2-F1-3` compact fall (recovered by compact flag) | w/h 1.87 | 0.38 to 0.11 in about 0.4 s, then 0.00 to 0.07 | 11 to 49 deg |
| `S4 ADL_10` lying onto a bed (no fall) | w/h up to 2.2 | **also falls to 0.03**, but over about 2.6 s (0.45 at 1.0 s, 0.04 at 3.6 s) | 5 to 63 deg |
| `S3-F1-3` (missed) | late track, no upright reference | already 0.06 to 0.08 on first sight | 18 to 20 deg |

## Reading

- Hip height tells a **bend** (hips stay high) from a **fall** (hips drop to the floor), which the box cannot do, and it shows a drop in the kneeling and late-visible falls that the box gate missed.
- It does **not** by itself tell a fall from **lying down on purpose**: lying onto a bed ends at the same hip height. In these clips the lying case was slower (about 0.15 hip-heights per second against about 0.3 or more for the falls), but that is three or four clips and an observation, not a tested rule. A usable feature would combine descent rate, context and recovery behaviour.
- A person with no upright reference (`S3-F1-3`) still cannot be judged on a drop, only on being already low.

## Limits

- Six clips, one dataset family each for falls and activities, chosen because they were the problem cases. No false-positive or recall number can be claimed from this.
- Hip height is normalised by the largest box seen so far, which is noisy early in a track and breaks under partial visibility or perspective changes.
- Keypoint quality drops on the lying and occluded frames (12 to 15 of 17 keypoints above the floor), so features there are less reliable.
- Not benchmarked for speed in the full pipeline; the probe ran on recorded boxes only.

## Suggested next steps (not done)

1. Add `hip_height` and its descent rate as optional extra evidence in the temporal estimator, behind a flag like the compact option.
2. Evaluate with the same discipline: replay on all recorded sets (about 60 no-fall clips and the falls) before and after, report false candidates separately for lying on a bed or floor.
3. Measure pose cost per person on the GPU before deciding whether to run it on every track or only on candidates.

---

## Update: pose evidence built into the pipeline and evaluated (2026-11-19)

**Result: neither pose rule is recommended. Both stay off by default.** The probe above suggested pose could separate bends from falls. Building it and testing it across everything recorded showed that only the bend case holds up.

### What was built (all off by default)

- `vision/pose/` (RTMPose-m, same DirectML settings as the detector); `PoseEvidence` logged on every observation when `--pose-evidence` is set, so any rule can be replayed on recorded runs.
- `pose_hip_drop` (`--pose-hip-drop`): accept a fall when hip height drops by at least 0.2 reference heights, at 0.2/s or faster, from at least 0.25 to at most 0.18.
- `pose_veto_hip_height` (`--pose-veto-hip-height`): veto a box-based fall while hip height is at least 0.28.
- Thresholds were fixed from the probe before the full runs; none were tuned afterwards. 11 new tests; full suite 80 tests pass.
- Cost: about 7 to 12 ms per sampled frame on the GPU (summed over people) on the dev, fresh and MPFDD sets.

### Full replay (recorded pose logs, 7 sets, about 125 clips; `evaluation/pose-full/`, `evaluation/pose-replay/`)

Falls detected / clips with a false candidate:

| Set | Off | Compact 0.6 | Hip-drop | Veto | Drop + veto |
|---|---|---|---|---|---|
| MPFDD (22 falls, 6 no-fall) | 17 / 0 | 19 / 0 | 20 / 0 | 17 / 0 | 20 / 0 |
| Dev (11, 13) | 10 / 0 | 10 / 0 | 10 / **5** | 10 / 0 | 10 / 5 |
| Holdout (2, 3) | 2 / 0 | 2 / 0 | 2 / 1 | 2 / 0 | 2 / 1 |
| Fresh (8, 7) | 7 / 1 | 8 / 1 | 7 / 2 | 7 / 1 | 7 / 2 |
| Crowd (0, 2) | 0 / 0 | 0 / 0 | 0 / 1 | 0 / 0 | 0 / 1 |
| Extra ADL (0, 21) | 0 / 0 | 0 / 0 | 0 / **5** | 0 / 0 | 0 / 5 |
| Lying/sleeping (0, 11) | 0 / 1 | 0 / 1 | 0 / **5** | 0 / **0** | 0 / 4 |

### Hip-drop rule: negative result

It recovers 3 of the 5 MPFDD misses (17 to 20) but raises false-candidate clips from 2 to 19 across the no-fall sets. The new false candidates are ordinary sitting, squatting and lying down, including the squat `clip_06` that the project had already identified as a hard negative. Their hip drops (0.23 to 0.48) and rates (0.20 to 0.49 per second) **overlap completely with the real falls** (0.23 to 0.37 and 0.20 to 0.45), so no threshold on these features separates them; tuning would only overfit. A fast drop of the hips does not distinguish sitting or lying down on purpose from falling.

### Veto: fixes the one known case, small and mixed otherwise

- Removes the forward-bend false candidate (`S2 ADL_08`, lying set 1 to 0 false clips) and loses no detections by itself.
- Delays four real detections by 0.2 to 0.6 s (the transition is suppressed while hips are still high) and removes one duplicate candidate event.
- **Combined with the compact flag it loses `fresh_gmd4_Fall_08`**, the one independent gain the compact flag made (fresh 8 to 7).
- The only clip it helps is the one whose hip height was seen when the threshold was chosen, so this is not validated evidence of improvement.

### Conclusion

Pose keypoints answer one question the box could not (are the hips still high, as in a bend) and that gives one clip. They do not answer the question that matters for falls: whether a person went to the ground on purpose. That needs context and what happens next (recovery, immobility, how the descent began), not a single frame-level body feature. Pose stays an optional, logged signal; the rules are documented here as an experiment and not recommended.

Not committed: the files from this work are in the working tree only.
