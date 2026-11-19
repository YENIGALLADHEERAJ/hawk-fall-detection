# Evaluation protocol (planned)

Hypothesis: selective visual investigation reduces false alerts while preserving
incident recall and bounding extra latency. No accuracy result exists yet.

Compare identical detector/tracker and initial trigger across: immediate alert;
fixed temporal verification; deterministic active policy; optionally Bedrock policy.
Use the same replay clock and hardware. Avoid future-frame access before timestamps
are available. Split by person and recording session, not randomly by neighboring frames.
Tune on development clips only. Freeze thresholds before held-out evaluation.

Manifest fields: clip hash, provenance, rights, subject/session split, camera,
timestamps, incident onset, recovery, visibility, ground truth, reviewer agreement.
Use staged consented clips plus permitted research data. Keep synthetic tests separate.

| Scenario | Expected behavior |
|---|---|
| Walking/sitting/bending | No verified incident; report false candidates |
| Fall then recovery | Temporal tool observes recovery; dismissal reason recorded |
| Fall with persistent immobility | Evidence gathered then human review, no medical diagnosis |
| Occlusion | Quality unknown; available-view request or uncertain review |
| Camera outage/tool timeout | Bounded failure and operator-visible degraded state |
| Shake/low light/multiple people | Quality/association handling; preserve failure examples |

Metrics: incident precision TP/(TP+FP), recall TP/(TP+FN), F1; false alerts per
nonincident camera-hour; latency from annotated onset to first candidate and review;
tool counts/failures, sufficiency satisfaction, operator overrides, CPU/memory and
per-tool/end-to-end p50/p95. Match alerts to annotated events with a predeclared time
tolerance and count duplicates separately. Report denominators and bootstrap intervals
by clip/session; small datasets cannot support broad safety claims. Tracking IDF1/HOTA
require track annotations and are N/A otherwise. Cloud cost needs actual usage/pricing.

Test budgets, schema rejection, missing data, stale evidence, duplicate calls,
illegal transitions and authorization. Record actual inputs/results/timestamps in
JSON traces. Replay all five scenarios repeatedly. A failure gallery must show missed
falls, false alarms and uncertain cases, not just successful demonstrations.
