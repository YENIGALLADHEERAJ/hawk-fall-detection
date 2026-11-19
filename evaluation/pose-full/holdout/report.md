# Actual footage evaluation

reused subject-held-out clips for Phase 1B regression; not unseen generalization

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| holdout_s2_Fall_13 | True | True | True | 34.31 | 27.9 | 36.8 | 5 |
| holdout_s2_ADL_14 | False | False | False | 38.65 | 16.9 | 30.0 | 2 |
| holdout_s3_Fall_16 | True | True | True | 27.13 | 31.6 | 45.2 | 2 |
| holdout_s3_ADL_13 | False | False | True | 36.11 | 17.6 | 35.7 | 1 |
| holdout_s3_ADL_09 | False | False | True | 28.18 | 18.8 | 42.8 | 1 |

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
    "true_positive_clips": 2,
    "false_positive_clips": 0,
    "event_recall": 1.0,
    "precision": 1.0,
    "false_positive_clip_rate": 0.0,
    "false_alert_events": 0,
    "negative_observation_hours": 0.007520776414973185,
    "false_alerts_per_negative_hour": 0.0
  }
}
```

Candidate detection and human-review alerts are separate outcomes. Refer to JSON for review times.
False-alarm reduction must be interpreted alongside recall; rejecting every clip is not success.
Latency uses publisher onset labels where available; missing labels remain null.
