# Footage attribution and scope

## Ivan Ursul, 2025 — CC BY 4.0

[Video-Based Fall Detection Dataset with 2017 Activities from 29 Subjects, v2](https://doi.org/10.6084/m9.figshare.28596332.v2).
Publisher metadata explicitly declares CC BY 4.0. Twelve selected short clips are
stored unmodified in `data/clips/clip_00.mp4` through `clip_11.mp4`. Archive member
paths and SHA-256 digests are in `manifest.json`; they are a single-subject development
subset, not a representative test population. The clips are about 1.9 seconds and
cannot establish prolonged immobility. Clip 01 ends before a complete visible fall
and is excluded from event-recall denominators despite its source directory label.
Changes: downsampling and overlays in generated debug/evidence outputs only.
License: https://creativecommons.org/licenses/by/4.0/ . Credit the author when sharing.

## Ekram Alam et al., 2024 — GMDCSA24 v2.1

[Publisher release](https://github.com/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/tree/v2.1),
[archived DOI](https://doi.org/10.5281/zenodo.13354453),
[paper](https://doi.org/10.1016/j.dib.2024.110892).
Authors: E. Alam, A. Sufian, P. Dutta, M. Leo, I. A. Hameed.
The dataset repository includes an MIT license, retained in `third_party/GMDCSA-LICENSE`.
The paper is CC BY; that paper license is not being substituted for the repository license.
Selected Subject 1 fall and ADL clips are stored unmodified. Source CSV onset labels
are retained under `data/sources/`; annotations are coarse and do not precisely label
immobility. Generated overlays/resizing are HAWK modifications. No identity inference.

`holdout.json` adds five unmodified clips from Subjects 2 and 3, initially evaluated
without retuning. Phase 1B reused their failures for engineering changes; its results
are regression measurements, not independent held-out accuracy. The manifest and
its historical split labels remain unchanged. Four are labeled Night in the
publisher CSVs; the room remains visibly illuminated, so they do not establish
performance in severe low light. The fifth shows lying-to-standing without a
preceding fall and therefore does not validate fall-followed-by-recovery. This is
subject separation within the same dataset, not an independent camera/site test.
The asset restoration script verifies these clips against the manifest hashes too.

## Not downloaded successfully

IKAR (Opyrchał et al., 2026, DOI 10.58032/AGH/A1NZPE), CC BY 4.0: metadata read,
but the redirected data-storage host timed out. No IKAR result is claimed.

## Evaluation boundaries

Real samples cover falls, partial body visibility, walking, sitting and intentional
lying down. Natural multi-person interactions, a fall followed immediately by recovery,
and dedicated low-light footage are not yet established in this subset. Controlled
brightness/occlusion perturbations, if used, must be labeled derived tests. Never
loop/freeze a last frame to claim immobility. All files remain local; no footage was
published to an external service. Download scripts verify bounds and preserve hashes.

## Phase 1C additions — 2026-10-28

The historical coverage statement above is superseded by this fresh validation addition:
15 clips under `data/clips/fresh_*`, registered in `datasets/phase1c/validation.json`.
Six GMDCSA24 Subject 4 clips (MIT), eight ASSIST-IoT reference activity videos
(CC BY 4.0), and a 10.2-second MOT17-09 extract (CC BY-NC-SA 3.0; noncommercial
research) have been downloaded. MOT contains real crossing/overlap; ASSIST backward
fall contains prolonged lying followed by recovery. No real immediate recovery or
fall during multi-person crossing has yet been established. ASSIST composites show
two views of the same demonstrator and must not be counted as two people.

ASSIST attribution/source: https://github.com/ASSIST-IoT-SRIPAS/multimodal-fall-detection-dataset
(source license retained as `third_party/ASSIST-LICENSE`; commit pinned in manifest).
MOT attribution/source: https://motchallenge.net/data/MOT17/ (license page retained
as `data/sources/mot-license.html`). MOT publisher frames 1..301 at stride 6 were
encoded as a 5 FPS MJPG audit video. Original JPEG hashes and frame mapping are in
`data/sources/mot17-09-audit/mapping.json`; full publisher annotations are retained
but evaluation uses only the sampled instants. This is not an official MOT benchmark.

`scripts/fetch_phase1c.py` selects/downloads GMD/ASSIST validation assets;
`scripts/fetch_mot_audit.py` adds the bounded MOT extract. Do not rerun selection
against a moving upstream source to claim the same experiment: retained manifests
and hashes define these exact assets. `development.json` contains the prior 30 clips.
`final-reserve.json` contains eight Ursul archive-member names only, not downloaded
or viewed files. It remains untouched because the fresh acceptance gate failed.

Independent raw-frame sparse annotations and their checksum are in
`datasets/phase1c/annotations.json` and `annotations.sha256`. These are single-AI-
annotator approximate visible-body references, not publisher or expert annotations.
See `docs/fresh-evaluation-gate.md` and `evaluation/phase1c/report.md` for limits.

## MPFDD public subset (evaluation only, 2026-11-15)

Multi-Person Falls Dataset, 28 public clips from https://github.com/Hnnuliulei123456/MPFDD
(paper: https://www.nature.com/articles/s41598-025-86429-6). **No license stated**; used locally for
research evaluation only, not redistributed or committed. Metadata and hashes: `datasets/mpfdd.json`.
Results: `docs/multi-person-validation.md`.
