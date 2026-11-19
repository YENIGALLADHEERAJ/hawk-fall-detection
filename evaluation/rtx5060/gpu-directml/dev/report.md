# Actual footage evaluation

small development set; not held-out accuracy or medical validation

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| clip_00 | True | True | True | 16.85 | 27.9 | 44.5 | 1 |
| clip_01 | None | False | False | 18.86 | 27.8 | 30.4 | 1 |
| clip_02 | True | True | True | 18.78 | 26.4 | 31.7 | 1 |
| clip_03 | True | True | True | 17.28 | 29.4 | 37.6 | 1 |
| clip_04 | True | True | True | 17.66 | 28.4 | 45.0 | 1 |
| clip_05 | True | False | False | 15.24 | 28.4 | 71.5 | 1 |
| clip_06 | False | False | False | 20.93 | 27.1 | 29.0 | 1 |
| clip_07 | False | False | False | 18.18 | 29.4 | 30.6 | 1 |
| clip_08 | False | False | False | 19.91 | 27.8 | 31.4 | 1 |
| clip_09 | False | False | False | 17.99 | 27.4 | 32.4 | 1 |
| clip_10 | False | False | False | 18.78 | 28.4 | 30.7 | 1 |
| clip_11 | False | False | False | 18.83 | 28.5 | 30.8 | 1 |
| gmdcsa_Fall_01 | True | True | True | 17.06 | 32.3 | 78.9 | 1 |
| gmdcsa_Fall_02 | True | True | True | 15.00 | 65.2 | 77.4 | 1 |
| gmdcsa_Fall_03 | True | True | True | 16.38 | 37.7 | 85.9 | 2 |
| gmdcsa_Fall_07 | True | True | True | 15.71 | 51.9 | 77.6 | 1 |
| gmdcsa_Fall_11 | True | True | True | 18.34 | 32.9 | 73.6 | 1 |
| gmdcsa_Fall_12 | True | True | True | 16.53 | 58.0 | 73.3 | 1 |
| gmdcsa_ADL_01 | False | False | True | 13.73 | 71.8 | 81.8 | 1 |
| gmdcsa_ADL_02 | False | False | True | 21.28 | 28.5 | 77.9 | 3 |
| gmdcsa_ADL_03 | False | False | True | 10.84 | 94.4 | 101.9 | 2 |
| gmdcsa_ADL_04 | False | False | True | 19.14 | 29.6 | 80.2 | 2 |
| gmdcsa_ADL_08 | False | False | False | 27.02 | 26.2 | 29.3 | 3 |
| gmdcsa_ADL_11 | False | False | False | 25.99 | 26.4 | 32.9 | 1 |
| gmdcsa_ADL_13 | False | False | False | 27.08 | 26.4 | 33.1 | 1 |

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
