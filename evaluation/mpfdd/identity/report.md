# Actual footage evaluation

small development set; not held-out accuracy or medical validation

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| mpfdd_S1_P2_F0_ADL_1 | False | False | False | 49.10 | 14.1 | 15.8 | 3 |
| mpfdd_S1_P2_F0_ADL_2 | False | False | False | 45.61 | 14.3 | 29.8 | 2 |
| mpfdd_S1_P2_F0_ADL_3 | False | False | True | 54.36 | 13.4 | 16.4 | 2 |
| mpfdd_S1_P2_F1_FALL_1 | True | True | True | 48.90 | 14.4 | 16.9 | 2 |
| mpfdd_S1_P2_F1_FALL_2 | True | False | True | 49.32 | 14.8 | 17.8 | 2 |
| mpfdd_S1_P2_F1_FALL_3 | True | False | True | 49.36 | 14.7 | 17.6 | 2 |
| mpfdd_S1_P2_F2_FALL_1 | True | True | True | 44.49 | 14.4 | 43.2 | 2 |
| mpfdd_S1_P2_F2_FALL_2 | True | True | True | 48.39 | 14.1 | 19.2 | 2 |
| mpfdd_S1_P2_F2_FALL_3 | True | True | True | 45.88 | 15.5 | 19.5 | 3 |
| mpfdd_S2_P2_F0_ADL_1 | False | False | False | 48.95 | 14.4 | 17.0 | 3 |
| mpfdd_S2_P2_F0_ADL_2 | False | False | False | 49.49 | 14.7 | 16.9 | 2 |
| mpfdd_S2_P2_F0_ADL_3 | False | False | False | 53.28 | 13.5 | 16.7 | 2 |
| mpfdd_S2_P2_F1_FALL_1 | True | True | True | 48.76 | 14.2 | 24.1 | 2 |
| mpfdd_S2_P2_F1_FALL_2 | True | True | True | 48.55 | 14.6 | 18.7 | 2 |
| mpfdd_S2_P2_F1_FALL_3 | True | False | True | 48.31 | 14.6 | 17.5 | 2 |
| mpfdd_S2_P2_F1_FALL_4 | True | True | True | 47.75 | 14.6 | 18.4 | 2 |
| mpfdd_S2_P2_F1_FALL_5 | True | False | False | 47.99 | 15.0 | 18.0 | 3 |
| mpfdd_S2_P2_F2_FALL_1 | True | True | True | 48.90 | 14.1 | 18.6 | 2 |
| mpfdd_S2_P2_F2_FALL_2 | True | True | True | 48.84 | 14.6 | 18.2 | 2 |
| mpfdd_S2_P2_F2_FALL_3 | True | True | True | 46.18 | 14.5 | 23.4 | 2 |
| mpfdd_S2_P2_F2_FALL_4 | True | True | True | 48.81 | 14.2 | 18.2 | 2 |
| mpfdd_S2_P2_F2_FALL_5 | True | True | True | 48.75 | 14.1 | 17.5 | 2 |
| mpfdd_S3_P4_F1_FALL_1 | True | True | True | 47.79 | 16.5 | 20.2 | 4 |
| mpfdd_S3_P4_F1_FALL_2 | True | True | True | 49.14 | 16.3 | 18.4 | 5 |
| mpfdd_S3_P4_F1_FALL_3 | True | False | True | 50.08 | 16.3 | 17.9 | 5 |
| mpfdd_S3_P4_F1_FALL_4 | True | True | True | 46.52 | 16.4 | 19.9 | 4 |
| mpfdd_S4_P4_F2_FALL_1 | True | True | True | 41.66 | 16.1 | 26.8 | 6 |
| mpfdd_S4_P4_F2_FALL_2 | True | True | True | 41.82 | 16.5 | 20.7 | 5 |

```json
{
  "immediate": {
    "positive_clips": 22,
    "negative_clips": 6,
    "true_positive_clips": 21,
    "false_positive_clips": 1,
    "event_recall": 0.9545454545454546,
    "precision": 0.9545454545454546,
    "false_positive_clip_rate": 0.16666666666666666,
    "false_alert_events": 2,
    "negative_observation_hours": 0.017277777777777777,
    "false_alerts_per_negative_hour": 115.7556270096463
  },
  "temporal": {
    "positive_clips": 22,
    "negative_clips": 6,
    "true_positive_clips": 17,
    "false_positive_clips": 0,
    "event_recall": 0.7727272727272727,
    "precision": 1.0,
    "false_positive_clip_rate": 0.0,
    "false_alert_events": 0,
    "negative_observation_hours": 0.017277777777777777,
    "false_alerts_per_negative_hour": 0.0
  }
}
```

Candidate detection and human-review alerts are separate outcomes. Refer to JSON for review times.
False-alarm reduction must be interpreted alongside recall; rejecting every clip is not success.
Latency uses publisher onset labels where available; missing labels remain null.
