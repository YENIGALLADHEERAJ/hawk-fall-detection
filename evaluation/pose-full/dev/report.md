# Actual footage evaluation

small development set; not held-out accuracy or medical validation

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| clip_00 | True | True | True | 24.14 | 16.1 | 59.7 | 1 |
| clip_01 | None | False | False | 27.23 | 15.8 | 38.9 | 1 |
| clip_02 | True | True | True | 25.78 | 16.5 | 43.8 | 1 |
| clip_03 | True | True | True | 23.33 | 18.1 | 48.2 | 1 |
| clip_04 | True | True | True | 23.39 | 16.9 | 51.3 | 1 |
| clip_05 | True | False | False | 21.26 | 19.3 | 58.7 | 1 |
| clip_06 | False | False | False | 24.03 | 17.6 | 45.0 | 1 |
| clip_07 | False | False | False | 24.23 | 17.3 | 46.5 | 1 |
| clip_08 | False | False | False | 20.25 | 26.7 | 51.9 | 1 |
| clip_09 | False | False | False | 22.95 | 18.5 | 45.3 | 1 |
| clip_10 | False | False | False | 22.21 | 19.2 | 54.7 | 1 |
| clip_11 | False | False | False | 21.88 | 17.9 | 45.9 | 1 |
| gmdcsa_Fall_01 | True | True | True | 25.89 | 27.9 | 68.2 | 1 |
| gmdcsa_Fall_02 | True | True | True | 27.41 | 28.2 | 48.0 | 1 |
| gmdcsa_Fall_03 | True | True | True | 26.01 | 30.1 | 55.4 | 2 |
| gmdcsa_Fall_07 | True | True | True | 27.63 | 26.7 | 40.0 | 1 |
| gmdcsa_Fall_11 | True | True | True | 27.61 | 25.7 | 48.3 | 1 |
| gmdcsa_Fall_12 | True | True | True | 28.01 | 28.8 | 37.2 | 1 |
| gmdcsa_ADL_01 | False | False | True | 27.42 | 29.1 | 35.0 | 1 |
| gmdcsa_ADL_02 | False | False | True | 30.58 | 18.4 | 39.0 | 3 |
| gmdcsa_ADL_03 | False | False | True | 22.00 | 38.0 | 42.9 | 2 |
| gmdcsa_ADL_04 | False | False | True | 28.15 | 19.0 | 39.9 | 2 |
| gmdcsa_ADL_08 | False | False | False | 32.37 | 18.1 | 26.9 | 3 |
| gmdcsa_ADL_11 | False | False | False | 32.92 | 18.7 | 21.8 | 1 |
| gmdcsa_ADL_13 | False | False | False | 32.64 | 20.1 | 22.8 | 1 |

```json
{
  "immediate": {
    "positive_clips": 11,
    "negative_clips": 13,
    "true_positive_clips": 10,
    "false_positive_clips": 4,
    "event_recall": 0.9090909090909091,
    "precision": 0.7142857142857143,
    "false_positive_clip_rate": 0.3076923076923077,
    "false_alert_events": 8,
    "negative_observation_hours": 0.016554408328914905,
    "false_alerts_per_negative_hour": 483.2549639377161
  },
  "temporal": {
    "positive_clips": 11,
    "negative_clips": 13,
    "true_positive_clips": 10,
    "false_positive_clips": 0,
    "event_recall": 0.9090909090909091,
    "precision": 1.0,
    "false_positive_clip_rate": 0.0,
    "false_alert_events": 0,
    "negative_observation_hours": 0.016554408328914905,
    "false_alerts_per_negative_hour": 0.0
  }
}
```

Candidate detection and human-review alerts are separate outcomes. Refer to JSON for review times.
False-alarm reduction must be interpreted alongside recall; rejecting every clip is not success.
Latency uses publisher onset labels where available; missing labels remain null.
