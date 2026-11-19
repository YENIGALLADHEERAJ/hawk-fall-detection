# Actual footage evaluation

Fresh Phase 1C validation, first measurement of frozen Phase 1B configuration; reserved final test untouched. Sparse localization audit reported separately.

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| fresh_gmd4_Fall_03 | True | True | True | 36.15 | 25.4 | 43.2 | 4 |
| fresh_gmd4_Fall_07 | True | True | True | 27.20 | 27.1 | 42.7 | 1 |
| fresh_gmd4_Fall_08 | True | False | True | 30.84 | 18.4 | 30.6 | 1 |
| fresh_gmd4_Fall_11 | True | True | True | 26.75 | 22.4 | 38.4 | 2 |
| fresh_gmd4_ADL_14 | False | False | False | 29.95 | 21.4 | 25.5 | 1 |
| fresh_gmd4_ADL_17 | False | False | False | 28.88 | 19.8 | 40.1 | 1 |
| fresh_assist_02_fall_backward | True | True | True | 35.42 | 17.3 | 40.3 | 4 |
| fresh_assist_04_forward_fall_jogging | True | True | True | 35.63 | 17.0 | 43.4 | 2 |
| fresh_assist_05_vertical_fall_faint | True | True | True | 33.30 | 18.0 | 50.4 | 3 |
| fresh_assist_07_fall_to_knees_forward | True | True | True | 33.62 | 17.6 | 43.7 | 2 |
| fresh_assist_01_walking_slowly | False | False | True | 34.50 | 18.0 | 25.1 | 3 |
| fresh_assist_12_sitting_laying_down_quickly | False | True | True | 31.41 | 21.3 | 44.0 | 3 |
| fresh_assist_13_bending_at_knees | False | False | True | 30.17 | 21.7 | 34.0 | 3 |
| fresh_assist_14_bending_wo_knees | False | False | True | 31.53 | 22.9 | 34.4 | 3 |
| fresh_mot17_09 | False | False | False | 14.38 | 58.6 | 90.4 | 35 |

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
