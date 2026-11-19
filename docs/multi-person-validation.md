# Real multi-person fall clips (MPFDD public subset) — 2026-11-15

First real footage in this project where several people share a scene with a fall. **No license is stated** for the data (GitHub API reports none; README gives no terms; the paper says only part of the data is public and the rest is available from the authors on request). Used locally for research evaluation only: not redistributed, not committed (`data/` is git-ignored; `datasets/mpfdd.json` holds only metadata, hashes and source URLs). Please cite the dataset and paper.

- Repository: https://github.com/Hnnuliulei123456/MPFDD
- Paper: https://www.nature.com/articles/s41598-025-86429-6
- Public subset: 28 `.mp4` files, 73.0 MB, fixed camera, 1060x516, 20 or 30 FPS, 7-16 s each (hashes in `data/sources/mpfdd/manifest.json`). Fetched with plain HTTPS from `raw.githubusercontent.com`.
- Filename code `S{scene}-P{people}-F{fallers}-{ADL|FALL}-{n}`. Labels used: FALL = fall present, ADL = daily activity, no fall. No onset times, no per-person boxes or IDs.

## Run

GPU backend, frozen detector/temporal settings, baseline tracker versus `--identity-tracking`, 5 Hz sampling. Results in `evaluation/mpfdd/{baseline,identity}`; manifest `datasets/mpfdd.json`.

| Group | Clips | Fall candidate raised |
|---|---:|---:|
| One person falls, 2 people (scenes 1-2) | 8 | 4 |
| One person falls, 4 people (scene 3) | 4 | 3 |
| Two people fall (2 or 4 in scene) | 10 | 10 |
| **All falls** | **22** | **17 (77%)** |
| Daily activity, 2 people, no fall | 6 | **0 false candidates** |

No clip reached a human-review request: the clips are short and the person recovers or the clip ends first, so this set says nothing about prolonged immobility.

Baseline and identity-tracking runs were **identical** on every clip (same candidate times, same track counts: 2 for two people, 4-5 for four). The appearance cue made no difference here because the baseline tracker already kept the right identities.

## Ownership of the fall evidence (the question this footage was fetched for)

- **Crossing case, inspected directly** (`S2-P2-F1-FALL-1`): one person falls at about 1.4-2.6 s (track 1, box width/height 0.4 to 2.3); the other stands then walks across the scene (track 2) and passes in front of the fallen person at about 5.0-5.6 s. Track 1 has no detection for about 0.6 s during the occlusion, reappears at 5.6 s in the same place and its box grows as the person gets up. Track 2 never takes over the history. Both trackers behave this way.
- **All seven detected single-faller clips** (2-person and 4-person): the fall candidate is on the track whose box became widest (a proxy for the faller, since there are no per-person labels): 7 of 7 for both trackers.
- A crude jump check over all 12 single-faller clips (track center moves more than 0.8 box heights within 0.45 s) found 0 jumps for both trackers. This catches gross swaps only.
- In the 4-person clips people cross each other before a fall, which is the situation of interest, but I only inspected contact sheets for a few clips, and I did not annotate individual people. A swap between two people standing close together could still be missed by the checks above.

## Missed falls (5 of 22, all single-faller; same failure classes as Phase 1C)

| Clip | What the tracker saw |
|---|---|
| S2-F1-5 | box never wider than tall (max w/h 1.05): fall ends kneeling/crouching |
| S3-F1-3 | box never clearly horizontal (max 1.04, seated); a lying box appears only briefly at the very end under a new track |
| S1-F1-2 | box becomes horizontal (w/h 1.29) at 4.4-5.0 s but the temporal score stays 0 under the frozen gates |
| S1-F1-3 | box becomes horizontal only at 8.8-10.0 s, at the end of the clip; score 0 |
| S2-F1-3 | box horizontal from 1.4 s (w/h up to 1.87), near the clip start; score 0 |

These are geometry and temporal-gate limits (compact falls, falls ending seated or kneeling, falls at the clip edges), not identity failures. The causes for the last three are inferred from the logged signals, not traced frame by frame. Thresholds were not changed.

## What this does and does not show

- Supports: with a fixed camera, a bystander walking in front of a fallen person did not capture the fall history in the one crossing case inspected, and fall candidates landed on the faller's track in all detected single-faller clips.
- Does not show: identity continuity under dense crowds or long occlusions, anything about prolonged-immobility escalation, behavior on moving cameras, or generalization (these are staged clips by one research group, mostly one scene per group, 28 clips).
- The recall figure (17/22) is a first measurement on new footage with the frozen configuration and is not comparable with the earlier sets; no tuning was done on it.
- Only 28 of the 220 reported videos are public; the full set would require asking the authors. Permission to reuse beyond local evaluation was not obtained.
