# Actual footage evaluation

reused subject-held-out clips for Phase 1B regression; not unseen generalization

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| holdout_s2_Fall_13 | True | False | True | 1.00 | 1202.8 | 1571.7 | 5 |
| holdout_s2_ADL_14 | False | False | False | 1.80 | 423.4 | 1240.2 | 2 |
| holdout_s3_Fall_16 | True | False | True | 0.90 | 1203.6 | 1850.0 | 2 |
| holdout_s3_ADL_13 | False | False | True | 1.56 | 544.0 | 1303.8 | 1 |
| holdout_s3_ADL_09 | False | True | True | 1.33 | 539.9 | 1430.7 | 1 |

```json
{
  "immediate": {
    "positive_clips": 2,
    "negative_clips": 3,
    "true_positive_clips": 2,
    "false_positive_clips": 2,
    "event_recall": 1.0,
    "precision": 0.5,
    "false_positive_clip_rate": 0.6666666666666666,
    "false_alert_events": 3,
    "negative_observation_hours": 0.007520776414973185,
    "false_alerts_per_negative_hour": 398.8949856330354
  },
  "temporal": {
    "positive_clips": 2,
    "negative_clips": 3,
    "true_positive_clips": 0,
    "false_positive_clips": 1,
    "event_recall": 0.0,
    "precision": 0.0,
    "false_positive_clip_rate": 0.3333333333333333,
    "false_alert_events": 1,
    "negative_observation_hours": 0.007520776414973185,
    "false_alerts_per_negative_hour": 132.9649952110118
  }
}
```

Candidate detection and human-review alerts are separate outcomes. Refer to JSON for review times.
False-alarm reduction must be interpreted alongside recall; rejecting every clip is not success.
Latency uses publisher onset labels where available; missing labels remain null.
