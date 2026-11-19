# Actual footage evaluation

Fresh Phase 1C validation, first measurement of frozen Phase 1B configuration; reserved final test untouched. Sparse localization audit reported separately.

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| fresh_gmd4_Fall_03 | True | True | True | 35.00 | 24.0 | 44.5 | 4 |
| fresh_gmd4_Fall_07 | True | True | True | 25.93 | 25.7 | 39.9 | 1 |
| fresh_gmd4_Fall_08 | True | False | True | 36.65 | 14.5 | 27.0 | 1 |
| fresh_gmd4_Fall_11 | True | True | True | 32.15 | 17.5 | 28.7 | 2 |
| fresh_gmd4_ADL_14 | False | False | False | 39.05 | 14.4 | 16.5 | 1 |
| fresh_gmd4_ADL_17 | False | False | False | 30.87 | 16.8 | 38.6 | 1 |
| fresh_assist_02_fall_backward | True | True | True | 36.12 | 15.2 | 23.9 | 4 |
| fresh_assist_04_forward_fall_jogging | True | True | True | 33.81 | 15.6 | 42.5 | 2 |
| fresh_assist_05_vertical_fall_faint | True | True | True | 31.38 | 16.9 | 44.8 | 3 |
| fresh_assist_07_fall_to_knees_forward | True | True | True | 23.09 | 22.7 | 74.2 | 2 |
| fresh_assist_01_walking_slowly | False | False | True | 19.75 | 33.6 | 40.4 | 3 |
| fresh_assist_12_sitting_laying_down_quickly | False | True | True | 24.98 | 21.5 | 68.1 | 3 |
| fresh_assist_13_bending_at_knees | False | False | True | 24.46 | 26.9 | 53.7 | 3 |
| fresh_assist_14_bending_wo_knees | False | False | True | 30.42 | 19.6 | 35.5 | 3 |
| fresh_mot17_09 | False | False | False | 25.42 | 25.5 | 49.4 | 33 |

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
