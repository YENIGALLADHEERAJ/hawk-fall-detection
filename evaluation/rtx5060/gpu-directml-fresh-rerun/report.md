# Actual footage evaluation

Fresh Phase 1C validation, first measurement of frozen Phase 1B configuration; reserved final test untouched. Sparse localization audit reported separately.

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| fresh_gmd4_Fall_03 | True | True | True | 42.31 | 22.1 | 33.5 | 4 |
| fresh_gmd4_Fall_07 | True | True | True | 32.38 | 21.7 | 32.3 | 1 |
| fresh_gmd4_Fall_08 | True | False | True | 41.76 | 13.0 | 24.4 | 1 |
| fresh_gmd4_Fall_11 | True | True | True | 36.96 | 13.9 | 25.7 | 2 |
| fresh_gmd4_ADL_14 | False | False | False | 48.67 | 13.3 | 16.1 | 1 |
| fresh_gmd4_ADL_17 | False | False | False | 43.31 | 12.6 | 29.1 | 1 |
| fresh_assist_02_fall_backward | True | True | True | 45.82 | 12.9 | 19.9 | 4 |
| fresh_assist_04_forward_fall_jogging | True | True | True | 43.79 | 12.8 | 36.6 | 2 |
| fresh_assist_05_vertical_fall_faint | True | True | True | 42.94 | 13.0 | 36.5 | 3 |
| fresh_assist_07_fall_to_knees_forward | True | True | True | 37.40 | 14.7 | 36.8 | 2 |
| fresh_assist_01_walking_slowly | False | False | True | 39.23 | 15.0 | 18.3 | 3 |
| fresh_assist_12_sitting_laying_down_quickly | False | True | True | 38.11 | 14.7 | 36.9 | 3 |
| fresh_assist_13_bending_at_knees | False | False | True | 38.58 | 12.9 | 30.4 | 3 |
| fresh_assist_14_bending_wo_knees | False | False | True | 37.44 | 16.2 | 33.0 | 3 |
| fresh_mot17_09 | False | False | False | 33.57 | 22.7 | 30.5 | 35 |

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
