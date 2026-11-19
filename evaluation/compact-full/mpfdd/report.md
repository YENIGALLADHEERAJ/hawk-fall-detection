# Actual footage evaluation

small development set; not held-out accuracy or medical validation

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| mpfdd_S1_P2_F0_ADL_1 | False | False | False | 54.69 | 13.2 | 14.1 | 3 |
| mpfdd_S1_P2_F0_ADL_2 | False | False | False | 46.80 | 13.5 | 31.8 | 2 |
| mpfdd_S1_P2_F0_ADL_3 | False | False | True | 49.83 | 13.8 | 14.8 | 2 |
| mpfdd_S1_P2_F1_FALL_1 | True | True | True | 43.03 | 15.5 | 19.3 | 2 |
| mpfdd_S1_P2_F1_FALL_2 | True | True | True | 44.61 | 14.5 | 19.7 | 2 |
| mpfdd_S1_P2_F1_FALL_3 | True | False | True | 46.49 | 14.6 | 17.5 | 2 |
| mpfdd_S1_P2_F2_FALL_1 | True | True | True | 40.26 | 15.2 | 46.1 | 2 |
| mpfdd_S1_P2_F2_FALL_2 | True | True | True | 41.39 | 14.9 | 21.5 | 2 |
| mpfdd_S1_P2_F2_FALL_3 | True | True | True | 46.79 | 15.0 | 19.4 | 3 |
| mpfdd_S2_P2_F0_ADL_1 | False | False | False | 48.18 | 14.8 | 17.5 | 3 |
| mpfdd_S2_P2_F0_ADL_2 | False | False | False | 50.87 | 14.2 | 16.9 | 2 |
| mpfdd_S2_P2_F0_ADL_3 | False | False | False | 50.49 | 14.1 | 16.8 | 2 |
| mpfdd_S2_P2_F1_FALL_1 | True | True | True | 51.81 | 13.4 | 18.2 | 2 |
| mpfdd_S2_P2_F1_FALL_2 | True | True | True | 54.44 | 13.1 | 16.4 | 2 |
| mpfdd_S2_P2_F1_FALL_3 | True | True | True | 50.80 | 13.5 | 22.7 | 2 |
| mpfdd_S2_P2_F1_FALL_4 | True | True | True | 53.14 | 13.2 | 16.9 | 2 |
| mpfdd_S2_P2_F1_FALL_5 | True | False | False | 52.57 | 14.0 | 15.6 | 3 |
| mpfdd_S2_P2_F2_FALL_1 | True | True | True | 52.95 | 13.3 | 18.0 | 2 |
| mpfdd_S2_P2_F2_FALL_2 | True | True | True | 49.68 | 14.3 | 17.4 | 2 |
| mpfdd_S2_P2_F2_FALL_3 | True | True | True | 45.27 | 14.5 | 31.2 | 2 |
| mpfdd_S2_P2_F2_FALL_4 | True | True | True | 47.44 | 14.9 | 17.3 | 2 |
| mpfdd_S2_P2_F2_FALL_5 | True | True | True | 48.01 | 14.6 | 17.7 | 2 |
| mpfdd_S3_P4_F1_FALL_1 | True | True | True | 46.45 | 16.6 | 20.3 | 4 |
| mpfdd_S3_P4_F1_FALL_2 | True | True | True | 49.08 | 16.3 | 18.4 | 5 |
| mpfdd_S3_P4_F1_FALL_3 | True | False | True | 47.84 | 16.9 | 19.8 | 5 |
| mpfdd_S3_P4_F1_FALL_4 | True | True | True | 45.87 | 16.6 | 21.0 | 4 |
| mpfdd_S4_P4_F2_FALL_1 | True | True | True | 39.95 | 16.3 | 30.8 | 6 |
| mpfdd_S4_P4_F2_FALL_2 | True | True | True | 42.39 | 16.3 | 21.5 | 5 |

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
    "true_positive_clips": 19,
    "false_positive_clips": 0,
    "event_recall": 0.8636363636363636,
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
