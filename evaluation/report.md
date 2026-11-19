# Actual footage evaluation

small development set; not held-out accuracy or medical validation

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| clip_00 | True | True | True | 2.54 | 341.5 | 445.5 | 1 |
| clip_01 | None | False | False | 1.28 | 692.3 | 951.8 | 1 |
| clip_02 | True | True | True | 0.99 | 969.8 | 1201.7 | 1 |
| clip_03 | True | True | True | 1.04 | 876.0 | 1192.9 | 1 |
| clip_04 | True | True | True | 2.07 | 411.0 | 678.7 | 1 |
| clip_05 | True | False | False | 1.63 | 362.9 | 1104.6 | 1 |
| clip_06 | False | False | False | 2.47 | 369.4 | 406.6 | 1 |
| clip_07 | False | False | False | 2.45 | 369.3 | 421.0 | 1 |
| clip_08 | False | False | False | 2.48 | 372.6 | 415.5 | 1 |
| clip_09 | False | False | False | 2.21 | 401.2 | 481.7 | 1 |
| clip_10 | False | False | False | 2.33 | 393.0 | 414.9 | 1 |
| clip_11 | False | False | False | 2.21 | 406.0 | 515.6 | 1 |
| gmdcsa_Fall_01 | True | True | True | 1.01 | 432.8 | 1930.1 | 1 |
| gmdcsa_Fall_02 | True | True | True | 0.97 | 1226.6 | 1440.4 | 5 |
| gmdcsa_Fall_03 | True | True | True | 1.16 | 678.2 | 1310.0 | 2 |
| gmdcsa_Fall_07 | True | True | True | 1.24 | 836.7 | 1338.6 | 2 |
| gmdcsa_Fall_11 | True | True | True | 1.32 | 667.8 | 1151.8 | 1 |
| gmdcsa_Fall_12 | True | True | True | 1.03 | 1273.3 | 1423.8 | 1 |
| gmdcsa_ADL_01 | False | False | True | 0.83 | 1336.1 | 1850.5 | 2 |
| gmdcsa_ADL_02 | False | False | True | 1.50 | 484.2 | 1398.8 | 3 |
| gmdcsa_ADL_03 | False | False | True | 0.80 | 1366.5 | 1827.0 | 2 |
| gmdcsa_ADL_04 | False | False | True | 1.41 | 468.8 | 1395.2 | 2 |
| gmdcsa_ADL_08 | False | False | False | 1.69 | 526.2 | 838.1 | 3 |
| gmdcsa_ADL_11 | False | False | False | 2.07 | 454.3 | 506.6 | 1 |
| gmdcsa_ADL_13 | False | False | False | 2.07 | 460.5 | 510.7 | 1 |

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
    "false_alert_events": 9,
    "negative_observation_hours": 0.016554408328914902,
    "false_alerts_per_negative_hour": 543.6618344299308
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
    "negative_observation_hours": 0.016554408328914902,
    "false_alerts_per_negative_hour": 0.0
  }
}
```

Candidate detection and human-review alerts are separate outcomes. Refer to JSON for review times.
False-alarm reduction must be interpreted alongside recall; rejecting every clip is not success.
Latency uses publisher onset labels where available; missing labels remain null.
