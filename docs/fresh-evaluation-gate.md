# Fresh-footage gate — preregistered 2026-10-28

This is an engineering validation gate, not a medical or deployment certification.
The Phase 1B configuration is frozen before inspecting fresh model outputs. Existing
30 clips are development/regression only. Fresh validation combines GMDCSA24 Subject 4
(new subject and room), independently published ASSIST-IoT activity reference videos,
and a bounded MOT17-09 pedestrian sequence. Eight Ursul Subject 04 / Location 2 members
are reserved by archive metadata and must remain unopened and unrun in this sprint.

The validation media may inform an explicitly reported experimental localization change.
Any such result is paired validation, not a new untouched final test. Fall thresholds
remain frozen in this sprint. Final-test access is deferred while validation is inadequate.

## Measures, fixed before inference

- Match independent reference boxes one-to-one at IoU >= 0.50. Report IoU >= 0.75
  sensitivity too. These conventional overlap cutoffs define measurement, not a
  safety guarantee or a detector-confidence adjustment.
- GMDCSA/ASSIST: six raw-frame snapshots per clip, manually boxed without model
  overlays. Report snapshot recall and localization error explicitly as a sparse,
  single-annotator exploratory audit. Do not claim full-video frame recall or true
  continuous gap lengths from these sparse annotations.
- MOT17: published marked class-1 pedestrian identities, visibility > 0, at the
  actual 5 Hz sampled instants. Fully hidden and ignored classes are reported/excluded;
  ID switches and gaps are defined in the local audit, not claimed as official HOTA/MOTA.
- Center jitter is change in reference-relative center error, normalized by reference
  height; size stability is change in log predicted/reference area. Raw motion must
  not be mislabeled jitter. Report descent/ground strata separately.
- Fall candidates, recoveries and review requests remain separate. A dismissed false
  candidate still counts. Unknown onset remains null; report temporal-label resolution.
- Measure full pipeline FPS, per-frame p50/p95, process CPU/memory and stage times.

## Target, observed gap and decision

Targets are deliberately stated as failure-free engineering goals for the covered
cases: detect each annotated fall, produce no fall candidates on annotated non-falls,
localize every visible reference person at IoU 0.50, avoid identity switches/history
transfer, and preserve sufficient observed continuity for the configured 0.5-second
motion gate. Report actual counts and the gap to these goals; do not relax them after
seeing results. Passing a small set still does not establish population reliability.

Completion also requires actual footage for all critical multi-person/fall/recovery
branches, stable localization in descent and prone states, meaningful sample diversity,
all regression tests green and a documented perception contract. Missing coverage
or systematic localization/temporal failures means INCOMPLETE. Live 5 FPS remains a
future operating target, not permission to sacrifice accuracy or hide slow inference.

Numerical deployment-risk thresholds and acceptable uncertainty intervals have not
been established with a domain owner. No small-sample point estimate can substitute
for that decision. Leave the final reserve untouched if this gate is not satisfied.
