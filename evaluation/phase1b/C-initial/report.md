# Actual footage evaluation

reused subject-held-out clips for Phase 1B regression; not unseen generalization

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| holdout_s2_Fall_13 | True | False | True | 0.83 | 1055.0 | 2381.9 | 8 |
| holdout_s2_ADL_14 | False | False | False | 1.56 | 480.5 | 1381.4 | 3 |
| holdout_s3_Fall_16 | True | False | True | 0.86 | 1353.4 | 1900.9 | 5 |
| holdout_s3_ADL_13 | False | False | True | 1.19 | 695.9 | 1490.3 | 1 |
| holdout_s3_ADL_09 | False | False | True | 1.22 | 555.4 | 1700.4 | 1 |

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
    "false_positive_clips": 0,
    "event_recall": 0.0,
    "precision": null,
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
