# Actual footage evaluation

small development set; not held-out accuracy or medical validation

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| clip_00 | True | True | True | 15.26 | 44.3 | 60.3 | 1 |
| clip_01 | None | False | False | 14.99 | 46.2 | 50.6 | 1 |
| clip_02 | True | True | True | 13.81 | 50.9 | 57.8 | 1 |
| clip_03 | True | True | True | 13.65 | 49.6 | 61.9 | 1 |
| clip_04 | True | True | True | 13.12 | 50.3 | 78.1 | 1 |
| clip_05 | True | False | False | 10.40 | 49.7 | 136.3 | 1 |
| clip_06 | False | False | False | 13.95 | 50.3 | 55.2 | 1 |
| clip_07 | False | False | False | 14.35 | 49.7 | 54.4 | 1 |
| clip_08 | False | False | False | 15.83 | 44.3 | 49.7 | 1 |
| clip_09 | False | False | False | 14.84 | 46.9 | 53.5 | 1 |
| clip_10 | False | False | False | 14.35 | 47.3 | 57.2 | 1 |
| clip_11 | False | False | False | 14.94 | 47.3 | 51.8 | 1 |
| gmdcsa_Fall_01 | True | True | True | 10.47 | 51.4 | 137.4 | 1 |
| gmdcsa_Fall_02 | True | True | True | 8.78 | 128.1 | 150.0 | 1 |
| gmdcsa_Fall_03 | True | True | True | 10.70 | 68.8 | 130.0 | 2 |
| gmdcsa_Fall_07 | True | True | True | 11.51 | 85.1 | 127.5 | 1 |
| gmdcsa_Fall_11 | True | True | True | 12.92 | 51.1 | 124.1 | 1 |
| gmdcsa_Fall_12 | True | True | True | 9.91 | 125.3 | 134.4 | 1 |
| gmdcsa_ADL_01 | False | False | True | 8.93 | 127.2 | 136.3 | 1 |
| gmdcsa_ADL_02 | False | False | True | 13.64 | 49.0 | 138.0 | 3 |
| gmdcsa_ADL_03 | False | False | True | 7.77 | 139.6 | 150.1 | 2 |
| gmdcsa_ADL_04 | False | False | True | 12.67 | 48.4 | 140.3 | 2 |
| gmdcsa_ADL_08 | False | False | False | 17.00 | 50.9 | 52.6 | 3 |
| gmdcsa_ADL_11 | False | False | False | 17.25 | 49.3 | 53.0 | 1 |
| gmdcsa_ADL_13 | False | False | False | 17.27 | 49.1 | 51.7 | 1 |

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
