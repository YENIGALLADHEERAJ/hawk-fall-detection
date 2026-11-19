# Actual footage evaluation

small development set; not held-out accuracy or medical validation

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| clip_00 | True | True | True | 5.59 | 149.7 | 174.3 | 1 |
| clip_01 | None | False | False | 5.91 | 147.4 | 158.2 | 1 |
| clip_02 | True | True | True | 5.87 | 148.2 | 157.2 | 1 |
| clip_03 | True | True | True | 5.72 | 149.0 | 165.5 | 1 |
| clip_04 | True | True | True | 5.24 | 149.9 | 238.7 | 1 |
| clip_05 | True | False | False | 3.83 | 151.7 | 444.4 | 1 |
| clip_06 | False | False | False | 5.76 | 149.5 | 153.1 | 1 |
| clip_07 | False | False | False | 5.66 | 152.3 | 155.3 | 1 |
| clip_08 | False | False | False | 5.71 | 151.3 | 154.2 | 1 |
| clip_09 | False | False | False | 4.40 | 221.4 | 237.3 | 1 |
| clip_10 | False | False | False | 4.24 | 216.9 | 246.4 | 1 |
| clip_11 | False | False | False | 3.79 | 239.8 | 261.2 | 1 |
| gmdcsa_Fall_01 | True | True | True | 3.14 | 170.8 | 481.2 | 1 |
| gmdcsa_Fall_02 | True | True | True | 2.78 | 437.4 | 447.6 | 1 |
| gmdcsa_Fall_03 | True | True | True | 3.35 | 223.2 | 455.5 | 2 |
| gmdcsa_Fall_07 | True | True | True | 3.64 | 294.2 | 434.9 | 1 |
| gmdcsa_Fall_11 | True | True | True | 4.27 | 155.6 | 384.3 | 1 |
| gmdcsa_Fall_12 | True | True | True | 3.13 | 427.2 | 446.4 | 1 |
| gmdcsa_ADL_01 | False | False | True | 2.86 | 425.7 | 440.1 | 1 |
| gmdcsa_ADL_02 | False | False | True | 4.85 | 145.7 | 432.2 | 3 |
| gmdcsa_ADL_03 | False | False | True | 2.67 | 431.9 | 441.7 | 2 |
| gmdcsa_ADL_04 | False | False | True | 4.44 | 145.1 | 438.2 | 2 |
| gmdcsa_ADL_08 | False | False | False | 6.50 | 144.5 | 149.7 | 3 |
| gmdcsa_ADL_11 | False | False | False | 6.52 | 144.0 | 149.2 | 1 |
| gmdcsa_ADL_13 | False | False | False | 6.47 | 144.7 | 150.6 | 1 |

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
