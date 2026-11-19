# Actual footage evaluation

Fresh Phase 1C validation, first measurement of frozen Phase 1B configuration; reserved final test untouched. Sparse localization audit reported separately.

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| fresh_gmd4_Fall_03 | True | True | True | 3.42 | 322.6 | 483.0 | 4 |
| fresh_gmd4_Fall_07 | True | True | True | 3.16 | 316.4 | 491.8 | 1 |
| fresh_gmd4_Fall_08 | True | False | True | 4.78 | 165.2 | 333.5 | 1 |
| fresh_gmd4_Fall_11 | True | True | True | 4.34 | 173.3 | 330.5 | 2 |
| fresh_gmd4_ADL_14 | False | False | False | 5.81 | 161.5 | 171.1 | 1 |
| fresh_gmd4_ADL_17 | False | False | False | 4.50 | 160.2 | 476.4 | 1 |
| fresh_assist_02_fall_backward | True | True | True | 5.81 | 160.9 | 177.4 | 4 |
| fresh_assist_04_forward_fall_jogging | True | True | True | 5.28 | 156.8 | 244.4 | 2 |
| fresh_assist_05_vertical_fall_faint | True | True | True | 6.08 | 151.6 | 174.9 | 3 |
| fresh_assist_07_fall_to_knees_forward | True | True | True | 6.18 | 150.1 | 169.0 | 2 |
| fresh_assist_01_walking_slowly | False | False | True | 6.11 | 153.7 | 158.9 | 3 |
| fresh_assist_12_sitting_laying_down_quickly | False | True | True | 6.19 | 150.5 | 169.2 | 3 |
| fresh_assist_13_bending_at_knees | False | False | True | 3.83 | 151.6 | 459.5 | 3 |
| fresh_assist_14_bending_wo_knees | False | False | True | 4.14 | 152.4 | 437.0 | 3 |
| fresh_mot17_09 | False | False | False | 6.12 | 156.8 | 160.9 | 35 |

```json
{
  "immediate": {
    "positive_clips": 8,
    "negative_clips": 7,
    "true_positive_clips": 8,
    "false_positive_clips": 4,
    "event_recall": 1.0,
    "precision": 0.6666666666666666,
    "false_positive_clip_rate": 0.5714285714285714,
    "false_alert_events": 6,
    "negative_observation_hours": 0.015850898297491037,
    "false_alerts_per_negative_hour": 378.5274428862944
  },
  "temporal": {
    "positive_clips": 8,
    "negative_clips": 7,
    "true_positive_clips": 7,
    "false_positive_clips": 1,
    "event_recall": 0.875,
    "precision": 0.875,
    "false_positive_clip_rate": 0.14285714285714285,
    "false_alert_events": 2,
    "negative_observation_hours": 0.015850898297491037,
    "false_alerts_per_negative_hour": 126.17581429543146
  }
}
```

Candidate detection and human-review alerts are separate outcomes. Refer to JSON for review times.
False-alarm reduction must be interpreted alongside recall; rejecting every clip is not success.
Latency uses publisher onset labels where available; missing labels remain null.
