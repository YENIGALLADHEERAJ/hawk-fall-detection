# Identity continuity — experimental association (2026-11-15)

**Status: consistent but modest gain from the appearance cue; identity continuity not solved. Opt-in only (`--identity-tracking`); frozen defaults unchanged.**

## Problem

Phase 1C found 37 reference-associated ID changes on MOT17-09, 27 of them cases where one track id covered two different reference people. For fall detection the second kind matters: a track switching to another person can carry fall or recovery history to the wrong owner. The original tracker is a greedy match on box distance, overlap and velocity, with no appearance information.

## Options in `vision/tracking` (all off by default)

1. **Appearance cue** (`--identity-tracking`): HSV colour histogram of the upper-body region, Bhattacharyya distance, blended into the association cost (weight 1.0) and kept as a decayed average (0.7). A cue, not re-identification: similar clothing looks alike, and nothing identifies a person.
2. **Optimal assignment** (`--optimal-assignment`): global minimum-cost matching (small Hungarian solver, no new dependency) instead of greedy matching. **Regressed on unseen footage; not recommended.**

No detection is invented; missing people stay missing.

## Measurements (replay of recorded real detections; 51 frames at 5 Hz per clip)

Reproduce with `python -m evaluation.identity_replay` (see the script for the MOT17-02/04 arguments); results in `evaluation/identity/replay*.json`. Weight 1.0 and decay .7 were first chosen on MOT17-09. MOT17-02 was then a held-out check, after which the optimal-assignment option was split off. MOT17-04 is the only clip not seen when the final appearance-only choice was made.

Cells are ID changes / owner changes (owner change = a track id matched to a different reference person than before).

| Association | MOT17-09 (tuned) | MOT17-02 (unseen) | MOT17-04 (unseen, after the choice) | Total |
|---|---:|---:|---:|---:|
| Baseline (greedy, geometry) | 37 / 27 | 22 / 21 | 29 / 24 | 88 / 72 |
| Optimal assignment only | 29 / 25 | 33 / 33 | 23 / 18 | 85 / 76 |
| **Appearance, greedy** (`--identity-tracking`) | **19 / 18** | **19 / 21** | **22 / 13** | **60 / 52** |
| Appearance + optimal | 18 / 17 | 31 / 37 | 17 / 11 | 66 / 65 |

- **Appearance with greedy matching** is no worse than the baseline on any of the three clips for either measure, and improves ID changes by about a third overall (88→60) and owner changes by about a quarter (72→52). On the clip not seen at selection time, MOT17-04, it cut ID changes 29→22 and owner changes 24→13. On MOT17-02 owner changes were unchanged (21→21).
- **Optimal assignment is inconsistent:** better on two clips, much worse on MOT17-02 (22→33). Likely cause, not verified: it maximizes the number of matches and forces weak links. It stays a separate, not-recommended flag (`--optimal-assignment`).
- Recall at IoU .5 is identical across variants (.86, .37, .49) and fragments are unchanged (12, 41, 75): both are set by detector misses, which tracking cannot fix. MOT17-02 (median reference height about 35 px, 71% under 40 px) and MOT17-04 are hard far-field scenes where the detector finds only 37-49% of the references, so small differences are not precise.

## Effect on fall detection (GPU backend, 45 clips, appearance-only variant)

Fall recall and false-positive counts are unchanged on all three sets (development 10/11 and 0/13, holdout 2/2 and 0/3, fresh 7/8 and 1/7). 43 of 45 clips are identical; one fall clip's first candidate moved from 3.4 s to 3.2 s with the same review time, and MOT17-09 distinct track ids fell from 35 to 33. Tests: 64/64 pass (7 cover the solver, the feature, colour-based identity under ambiguous geometry and unchanged defaults).

## What this does not show

- Owner changes are still 18, 21 and 13 across the clips; the zero-switch goal is not met and ownership of fall history through crowds is still not guaranteed.
- Three MOT17 pedestrian sequences, all static cameras and all scored at 5 Hz from 1080p frames; one clip (MOT17-04) was unseen at selection time. That supports, but does not establish, general benefit. A moving camera or a different environment was not tested.
- MOT17 has no falls. Real multi-person fall clips (MPFDD public subset) were later run: ownership stayed with the faller in the one crossing case inspected and in 7 of 7 detected single-faller clips, with and without the appearance cue (identical results); see [multi-person-validation.md](multi-person-validation.md). That is supporting evidence from staged clips, not proof for crowds.
- Clothing-colour cues can fail with similar clothing, lighting change or occlusion; not measured separately.
- Remaining owner changes may partly come from overlapping references and crowded-scene annotation ambiguity.

## Data note

The MOT17-02 and MOT17-04 frames and ground truth (publisher JPEGs, CC BY-NC-SA 3.0, local noncommercial research) were fetched with `scripts/fetch_mot_sequence.py` into `data/sources/mot17-0{2,4}-frcnn-identity/` and `data/clips/identity_mot17_0{2,4}.avi`. They are not part of any validation manifest.

## Next steps

Look at the remaining owner changes individually (several are crowd overlaps), test on footage with a real multi-person fall, then decide whether appearance-only should become a default. It is not a default today.
