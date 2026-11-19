# Actual footage evaluation

small development set; not held-out accuracy or medical validation

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| mpfdd_S1_P2_F0_ADL_1 | False | False | False | 48.30 | 13.8 | 15.4 | 3 |
| mpfdd_S1_P2_F0_ADL_2 | False | False | False | 46.67 | 13.8 | 31.1 | 2 |
| mpfdd_S1_P2_F0_ADL_3 | False | False | True | 52.05 | 14.0 | 17.2 | 2 |
| mpfdd_S1_P2_F1_FALL_1 | True | True | True | 45.50 | 15.4 | 19.0 | 2 |
| mpfdd_S1_P2_F1_FALL_2 | True | False | True | 50.89 | 14.4 | 17.2 | 2 |
| mpfdd_S1_P2_F1_FALL_3 | True | False | True | 51.00 | 14.1 | 18.0 | 2 |
| mpfdd_S1_P2_F2_FALL_1 | True | True | True | 45.72 | 14.0 | 44.0 | 2 |
| mpfdd_S1_P2_F2_FALL_2 | True | True | True | 52.85 | 13.1 | 18.6 | 2 |
| mpfdd_S1_P2_F2_FALL_3 | True | True | True | 49.44 | 14.6 | 18.0 | 3 |
| mpfdd_S2_P2_F0_ADL_1 | False | False | False | 54.60 | 13.1 | 16.5 | 3 |
| mpfdd_S2_P2_F0_ADL_2 | False | False | False | 52.29 | 13.7 | 18.5 | 2 |
| mpfdd_S2_P2_F0_ADL_3 | False | False | False | 52.97 | 13.5 | 17.5 | 2 |
| mpfdd_S2_P2_F1_FALL_1 | True | True | True | 49.79 | 13.8 | 18.9 | 2 |
| mpfdd_S2_P2_F1_FALL_2 | True | True | True | 51.50 | 13.7 | 17.8 | 2 |
| mpfdd_S2_P2_F1_FALL_3 | True | False | True | 49.47 | 14.6 | 17.2 | 2 |
| mpfdd_S2_P2_F1_FALL_4 | True | True | True | 48.33 | 14.1 | 18.6 | 2 |
| mpfdd_S2_P2_F1_FALL_5 | True | False | False | 53.25 | 13.5 | 16.9 | 3 |
| mpfdd_S2_P2_F2_FALL_1 | True | True | True | 53.47 | 13.2 | 18.0 | 2 |
| mpfdd_S2_P2_F2_FALL_2 | True | True | True | 54.89 | 13.2 | 15.9 | 2 |
| mpfdd_S2_P2_F2_FALL_3 | True | True | True | 50.35 | 13.4 | 23.1 | 2 |
| mpfdd_S2_P2_F2_FALL_4 | True | True | True | 52.50 | 13.4 | 19.1 | 2 |
| mpfdd_S2_P2_F2_FALL_5 | True | True | True | 49.21 | 14.3 | 18.6 | 2 |
| mpfdd_S3_P4_F1_FALL_1 | True | True | True | 47.81 | 16.2 | 18.2 | 4 |
| mpfdd_S3_P4_F1_FALL_2 | True | True | True | 49.26 | 16.3 | 18.0 | 5 |
| mpfdd_S3_P4_F1_FALL_3 | True | False | True | 50.11 | 16.2 | 18.1 | 5 |
| mpfdd_S3_P4_F1_FALL_4 | True | True | True | 48.29 | 16.1 | 21.1 | 4 |
| mpfdd_S4_P4_F2_FALL_1 | True | True | True | 40.27 | 16.2 | 29.6 | 6 |
| mpfdd_S4_P4_F2_FALL_2 | True | True | True | 43.41 | 16.1 | 23.5 | 5 |

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
