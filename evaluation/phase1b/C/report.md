# Actual footage evaluation

reused subject-held-out clips for Phase 1B regression; not unseen generalization

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| holdout_s2_Fall_13 | True | False | True | 0.98 | 915.9 | 2117.6 | 8 |
| holdout_s2_ADL_14 | False | False | False | 1.23 | 608.1 | 1577.6 | 3 |
| holdout_s3_Fall_16 | True | False | True | 0.70 | 1429.4 | 2625.8 | 5 |
| holdout_s3_ADL_13 | False | False | True | 1.19 | 632.4 | 2044.8 | 1 |
| holdout_s3_ADL_09 | False | False | True | 0.88 | 847.5 | 2357.2 | 1 |

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
