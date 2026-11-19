# Actual footage evaluation

Fresh Phase 1C validation, first measurement of frozen Phase 1B configuration; reserved final test untouched. Sparse localization audit reported separately.

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| fresh_gmd4_Fall_03 | True | True | True | 22.12 | 30.3 | 80.3 | 4 |
| fresh_gmd4_Fall_07 | True | True | True | 0.17 | 57.1 | 270.6 | 1 |
| fresh_gmd4_Fall_08 | True | False | True | 21.67 | 29.0 | 56.8 | 1 |
| fresh_gmd4_Fall_11 | True | True | True | 22.51 | 28.3 | 53.3 | 2 |
| fresh_gmd4_ADL_14 | False | False | False | 26.58 | 26.3 | 31.8 | 1 |
| fresh_gmd4_ADL_17 | False | False | False | 23.06 | 27.3 | 73.3 | 1 |
| fresh_assist_02_fall_backward | True | True | True | 34.65 | 15.4 | 34.7 | 4 |
| fresh_assist_04_forward_fall_jogging | True | True | True | 23.58 | 29.3 | 60.7 | 2 |
| fresh_assist_05_vertical_fall_faint | True | True | True | 23.56 | 30.2 | 55.0 | 3 |
| fresh_assist_07_fall_to_knees_forward | True | True | True | 21.48 | 32.3 | 53.4 | 2 |
| fresh_assist_01_walking_slowly | False | False | True | 26.71 | 28.4 | 30.2 | 3 |
| fresh_assist_12_sitting_laying_down_quickly | False | True | True | 23.69 | 31.0 | 50.0 | 3 |
| fresh_assist_13_bending_at_knees | False | False | True | 20.05 | 29.1 | 71.4 | 3 |
| fresh_assist_14_bending_wo_knees | False | False | True | 19.81 | 33.8 | 73.5 | 3 |
| fresh_mot17_09 | False | False | False | 23.00 | 35.9 | 41.3 | 35 |

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
