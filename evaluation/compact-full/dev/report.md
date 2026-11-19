# Actual footage evaluation

small development set; not held-out accuracy or medical validation

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| clip_00 | True | True | True | 26.53 | 12.5 | 29.7 | 1 |
| clip_01 | None | False | False | 28.56 | 12.6 | 16.4 | 1 |
| clip_02 | True | True | True | 28.69 | 12.6 | 20.8 | 1 |
| clip_03 | True | True | True | 26.57 | 13.7 | 22.0 | 1 |
| clip_04 | True | True | True | 25.91 | 13.8 | 22.2 | 1 |
| clip_05 | True | False | False | 23.14 | 15.6 | 31.3 | 1 |
| clip_06 | False | False | False | 26.90 | 13.9 | 17.8 | 1 |
| clip_07 | False | False | False | 26.95 | 13.5 | 18.1 | 1 |
| clip_08 | False | False | False | 26.81 | 14.0 | 19.4 | 1 |
| clip_09 | False | False | False | 26.75 | 14.1 | 18.1 | 1 |
| clip_10 | False | False | False | 26.58 | 13.7 | 19.8 | 1 |
| clip_11 | False | False | False | 25.37 | 14.5 | 20.5 | 1 |
| gmdcsa_Fall_01 | True | True | True | 31.19 | 18.9 | 34.4 | 1 |
| gmdcsa_Fall_02 | True | True | True | 26.72 | 32.3 | 38.4 | 1 |
| gmdcsa_Fall_03 | True | True | True | 26.13 | 23.0 | 40.2 | 2 |
| gmdcsa_Fall_07 | True | True | True | 27.61 | 25.0 | 33.9 | 1 |
| gmdcsa_Fall_11 | True | True | True | 29.03 | 22.5 | 38.9 | 1 |
| gmdcsa_Fall_12 | True | True | True | 26.55 | 31.6 | 38.6 | 1 |
| gmdcsa_ADL_01 | False | False | True | 25.08 | 33.1 | 40.8 | 1 |
| gmdcsa_ADL_02 | False | False | True | 33.16 | 15.5 | 37.0 | 3 |
| gmdcsa_ADL_03 | False | False | True | 23.20 | 35.0 | 41.0 | 2 |
| gmdcsa_ADL_04 | False | False | True | 30.74 | 15.9 | 39.0 | 2 |
| gmdcsa_ADL_08 | False | False | False | 38.73 | 14.2 | 17.3 | 3 |
| gmdcsa_ADL_11 | False | False | False | 38.55 | 14.4 | 18.9 | 1 |
| gmdcsa_ADL_13 | False | False | False | 37.30 | 14.8 | 18.7 | 1 |

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
