# Actual footage evaluation

small development set; not held-out accuracy or medical validation

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| mpfdd_S1_P2_F0_ADL_1 | False | False | False | 20.63 | 21.8 | 25.8 | 3 |
| mpfdd_S1_P2_F0_ADL_2 | False | False | False | 30.03 | 23.9 | 34.8 | 2 |
| mpfdd_S1_P2_F0_ADL_3 | False | False | True | 38.72 | 20.5 | 22.1 | 2 |
| mpfdd_S1_P2_F1_FALL_1 | True | True | True | 29.77 | 25.5 | 29.4 | 2 |
| mpfdd_S1_P2_F1_FALL_2 | True | False | True | 34.20 | 21.9 | 24.6 | 2 |
| mpfdd_S1_P2_F1_FALL_3 | True | False | True | 34.27 | 22.6 | 25.3 | 2 |
| mpfdd_S1_P2_F2_FALL_1 | True | True | True | 30.58 | 22.6 | 60.1 | 2 |
| mpfdd_S1_P2_F2_FALL_2 | True | True | True | 35.15 | 20.3 | 39.1 | 2 |
| mpfdd_S1_P2_F2_FALL_3 | True | True | True | 30.69 | 26.6 | 33.0 | 3 |
| mpfdd_S2_P2_F0_ADL_1 | False | False | False | 33.54 | 22.4 | 26.3 | 3 |
| mpfdd_S2_P2_F0_ADL_2 | False | False | False | 32.82 | 23.1 | 28.4 | 2 |
| mpfdd_S2_P2_F0_ADL_3 | False | False | False | 33.98 | 22.4 | 24.9 | 2 |
| mpfdd_S2_P2_F1_FALL_1 | True | True | True | 31.81 | 24.3 | 42.1 | 2 |
| mpfdd_S2_P2_F1_FALL_2 | True | True | True | 32.20 | 22.7 | 29.7 | 2 |
| mpfdd_S2_P2_F1_FALL_3 | True | False | True | 32.45 | 22.5 | 28.7 | 2 |
| mpfdd_S2_P2_F1_FALL_4 | True | True | True | 28.98 | 25.7 | 32.9 | 2 |
| mpfdd_S2_P2_F1_FALL_5 | True | False | False | 31.66 | 24.0 | 29.0 | 3 |
| mpfdd_S2_P2_F2_FALL_1 | True | True | True | 31.86 | 22.5 | 30.7 | 2 |
| mpfdd_S2_P2_F2_FALL_2 | True | True | True | 32.37 | 22.3 | 29.1 | 2 |
| mpfdd_S2_P2_F2_FALL_3 | True | True | True | 31.03 | 23.1 | 35.3 | 2 |
| mpfdd_S2_P2_F2_FALL_4 | True | True | True | 32.97 | 22.5 | 28.7 | 2 |
| mpfdd_S2_P2_F2_FALL_5 | True | True | True | 31.62 | 24.0 | 34.3 | 2 |
| mpfdd_S3_P4_F1_FALL_1 | True | True | True | 25.23 | 33.4 | 41.5 | 4 |
| mpfdd_S3_P4_F1_FALL_2 | True | True | True | 25.42 | 34.0 | 44.2 | 5 |
| mpfdd_S3_P4_F1_FALL_3 | True | False | True | 26.37 | 33.2 | 39.6 | 5 |
| mpfdd_S3_P4_F1_FALL_4 | True | True | True | 22.53 | 38.1 | 57.8 | 4 |
| mpfdd_S4_P4_F2_FALL_1 | True | True | True | 22.01 | 35.4 | 88.1 | 6 |
| mpfdd_S4_P4_F2_FALL_2 | True | True | True | 23.92 | 32.5 | 71.3 | 5 |

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
