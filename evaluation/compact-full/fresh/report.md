# Actual footage evaluation

Fresh Phase 1C validation, first measurement of frozen Phase 1B configuration; reserved final test untouched. Sparse localization audit reported separately.

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| fresh_gmd4_Fall_03 | True | True | True | 42.70 | 21.3 | 35.2 | 4 |
| fresh_gmd4_Fall_07 | True | True | True | 29.19 | 23.8 | 36.2 | 1 |
| fresh_gmd4_Fall_08 | True | True | True | 34.02 | 14.5 | 28.0 | 1 |
| fresh_gmd4_Fall_11 | True | True | True | 32.25 | 15.1 | 29.8 | 2 |
| fresh_gmd4_ADL_14 | False | False | False | 39.33 | 14.4 | 15.8 | 1 |
| fresh_gmd4_ADL_17 | False | False | False | 33.58 | 14.5 | 37.1 | 1 |
| fresh_assist_02_fall_backward | True | True | True | 37.73 | 14.3 | 22.6 | 4 |
| fresh_assist_04_forward_fall_jogging | True | True | True | 35.54 | 14.5 | 41.5 | 2 |
| fresh_assist_05_vertical_fall_faint | True | True | True | 36.87 | 14.3 | 40.6 | 3 |
| fresh_assist_07_fall_to_knees_forward | True | True | True | 36.50 | 14.4 | 37.2 | 2 |
| fresh_assist_01_walking_slowly | False | False | True | 38.51 | 14.3 | 17.8 | 3 |
| fresh_assist_12_sitting_laying_down_quickly | False | True | True | 34.68 | 15.7 | 40.7 | 3 |
| fresh_assist_13_bending_at_knees | False | False | True | 31.21 | 16.5 | 32.3 | 3 |
| fresh_assist_14_bending_wo_knees | False | False | True | 32.23 | 18.5 | 34.2 | 3 |
| fresh_mot17_09 | False | False | False | 32.32 | 24.0 | 29.3 | 35 |

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
    "true_positive_clips": 8,
    "false_positive_clips": 1,
    "event_recall": 1.0,
    "precision": 0.8888888888888888,
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
