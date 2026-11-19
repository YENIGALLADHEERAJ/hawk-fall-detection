# Actual footage evaluation

small development set; not held-out accuracy or medical validation

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| clip_00 | True | True | True | 22.25 | 14.2 | 35.6 | 1 |
| clip_01 | None | False | False | 23.91 | 14.4 | 19.2 | 1 |
| clip_02 | True | True | True | 19.98 | 15.0 | 46.1 | 1 |
| clip_03 | True | True | True | 16.52 | 27.1 | 59.6 | 1 |
| clip_04 | True | True | True | 14.77 | 28.7 | 83.0 | 1 |
| clip_05 | True | False | False | 14.49 | 41.5 | 77.7 | 1 |
| clip_06 | False | False | False | 23.10 | 14.8 | 19.2 | 1 |
| clip_07 | False | False | False | 21.32 | 15.5 | 21.6 | 1 |
| clip_08 | False | False | False | 25.64 | 14.5 | 19.9 | 1 |
| clip_09 | False | False | False | 23.10 | 15.4 | 21.1 | 1 |
| clip_10 | False | False | False | 23.19 | 15.6 | 21.4 | 1 |
| clip_11 | False | False | False | 20.52 | 17.2 | 29.5 | 1 |
| gmdcsa_Fall_01 | True | True | True | 23.77 | 33.0 | 45.3 | 1 |
| gmdcsa_Fall_02 | True | True | True | 23.71 | 35.2 | 44.1 | 1 |
| gmdcsa_Fall_03 | True | True | True | 24.49 | 26.7 | 41.8 | 2 |
| gmdcsa_Fall_07 | True | True | True | 27.35 | 25.8 | 36.3 | 1 |
| gmdcsa_Fall_11 | True | True | True | 27.18 | 22.5 | 57.2 | 1 |
| gmdcsa_Fall_12 | True | True | True | 26.41 | 33.2 | 36.4 | 1 |
| gmdcsa_ADL_01 | False | False | True | 24.39 | 34.4 | 39.4 | 1 |
| gmdcsa_ADL_02 | False | False | True | 33.09 | 14.6 | 39.1 | 3 |
| gmdcsa_ADL_03 | False | False | True | 22.78 | 35.7 | 40.6 | 2 |
| gmdcsa_ADL_04 | False | False | True | 32.46 | 15.2 | 37.3 | 2 |
| gmdcsa_ADL_08 | False | False | False | 38.63 | 14.4 | 17.7 | 3 |
| gmdcsa_ADL_11 | False | False | False | 39.68 | 14.5 | 17.1 | 1 |
| gmdcsa_ADL_13 | False | False | False | 38.11 | 15.0 | 19.6 | 1 |

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
