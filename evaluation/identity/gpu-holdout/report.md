# Actual footage evaluation

reused subject-held-out clips for Phase 1B regression; not unseen generalization

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| holdout_s2_Fall_13 | True | True | True | 33.61 | 33.5 | 39.0 | 5 |
| holdout_s2_ADL_14 | False | False | False | 38.21 | 14.5 | 36.8 | 2 |
| holdout_s3_Fall_16 | True | True | True | 28.67 | 33.4 | 38.2 | 2 |
| holdout_s3_ADL_13 | False | False | True | 32.02 | 19.8 | 35.0 | 1 |
| holdout_s3_ADL_09 | False | False | True | 22.79 | 21.5 | 55.1 | 1 |

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
