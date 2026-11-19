# Actual footage evaluation

Fresh Phase 1C validation, first measurement of frozen Phase 1B configuration; reserved final test untouched. Sparse localization audit reported separately.

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| fresh_gmd4_Fall_03 | True | True | True | 0.99 | 949.3 | 1802.9 | 4 |
| fresh_gmd4_Fall_07 | True | True | True | 0.95 | 1046.2 | 1808.4 | 1 |
| fresh_gmd4_Fall_08 | True | False | True | 1.34 | 568.9 | 1454.3 | 1 |
| fresh_gmd4_Fall_11 | True | True | True | 0.99 | 744.1 | 1967.9 | 2 |
| fresh_gmd4_ADL_14 | False | False | False | 1.52 | 591.0 | 915.3 | 1 |
| fresh_gmd4_ADL_17 | False | False | False | 1.61 | 455.2 | 1336.6 | 1 |
| fresh_assist_02_fall_backward | True | True | True | 1.71 | 512.4 | 887.1 | 4 |
| fresh_assist_04_forward_fall_jogging | True | True | True | 1.70 | 521.7 | 869.4 | 2 |
| fresh_assist_05_vertical_fall_faint | True | True | True | 1.85 | 495.4 | 709.9 | 3 |
| fresh_assist_07_fall_to_knees_forward | True | True | True | 1.81 | 514.2 | 668.0 | 2 |
| fresh_assist_01_walking_slowly | False | False | True | 1.51 | 544.0 | 944.7 | 3 |
| fresh_assist_12_sitting_laying_down_quickly | False | True | True | 1.76 | 516.7 | 770.5 | 3 |
| fresh_assist_13_bending_at_knees | False | False | True | 1.21 | 551.4 | 1424.6 | 3 |
| fresh_assist_14_bending_wo_knees | False | False | True | 1.11 | 556.0 | 1733.9 | 3 |
| fresh_mot17_09 | False | False | False | 1.60 | 520.3 | 970.9 | 35 |

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
    "negative_observation_hours": 0.01585089829749104,
    "false_alerts_per_negative_hour": 378.52744288629435
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
    "negative_observation_hours": 0.01585089829749104,
    "false_alerts_per_negative_hour": 126.17581429543144
  }
}
```

Candidate detection and human-review alerts are separate outcomes. Refer to JSON for review times.
False-alarm reduction must be interpreted alongside recall; rejecting every clip is not success.
Latency uses publisher onset labels where available; missing labels remain null.
