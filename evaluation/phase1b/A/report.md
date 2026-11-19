# Actual footage evaluation

small subject-held-out set; no threshold retuning; not medical validation

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| holdout_s2_Fall_13 | True | False | True | 0.88 | 1192.4 | 2152.0 | 8 |
| holdout_s2_ADL_14 | False | False | False | 1.11 | 671.8 | 2351.6 | 3 |
| holdout_s3_Fall_16 | True | False | True | 0.91 | 1138.1 | 2073.1 | 5 |
| holdout_s3_ADL_13 | False | False | True | 1.83 | 443.1 | 1332.2 | 1 |
| holdout_s3_ADL_09 | False | True | True | 1.21 | 712.3 | 1548.6 | 1 |

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
