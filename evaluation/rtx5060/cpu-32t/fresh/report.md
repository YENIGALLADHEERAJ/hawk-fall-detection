# Actual footage evaluation

Fresh Phase 1C validation, first measurement of frozen Phase 1B configuration; reserved final test untouched. Sparse localization audit reported separately.

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| fresh_gmd4_Fall_03 | True | True | True | 10.57 | 97.8 | 149.5 | 4 |
| fresh_gmd4_Fall_07 | True | True | True | 10.03 | 89.9 | 142.5 | 1 |
| fresh_gmd4_Fall_08 | True | False | True | 15.38 | 47.1 | 91.8 | 1 |
| fresh_gmd4_Fall_11 | True | True | True | 13.92 | 48.2 | 97.9 | 2 |
| fresh_gmd4_ADL_14 | False | False | False | 18.37 | 46.0 | 48.2 | 1 |
| fresh_gmd4_ADL_17 | False | False | False | 14.15 | 50.2 | 129.0 | 1 |
| fresh_assist_02_fall_backward | True | True | True | 17.50 | 47.1 | 59.6 | 4 |
| fresh_assist_04_forward_fall_jogging | True | True | True | 18.86 | 43.9 | 69.8 | 2 |
| fresh_assist_05_vertical_fall_faint | True | True | True | 18.80 | 44.1 | 67.9 | 3 |
| fresh_assist_07_fall_to_knees_forward | True | True | True | 18.71 | 44.5 | 65.1 | 2 |
| fresh_assist_01_walking_slowly | False | False | True | 19.08 | 44.6 | 46.5 | 3 |
| fresh_assist_12_sitting_laying_down_quickly | False | True | True | 18.22 | 45.2 | 71.2 | 3 |
| fresh_assist_13_bending_at_knees | False | False | True | 12.30 | 49.6 | 129.7 | 3 |
| fresh_assist_14_bending_wo_knees | False | False | True | 12.73 | 50.5 | 127.1 | 3 |
| fresh_mot17_09 | False | False | False | 16.56 | 53.6 | 59.9 | 35 |

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
