# Actual footage evaluation

small development set; not held-out accuracy or medical validation

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| clip_00 | True | True | True | 5.87 | 147.3 | 167.4 | 1 |
| clip_01 | None | False | False | 6.03 | 145.4 | 151.2 | 1 |
| clip_02 | True | True | True | 5.95 | 147.0 | 154.7 | 1 |
| clip_03 | True | True | True | 5.96 | 146.2 | 157.2 | 1 |
| clip_04 | True | True | True | 5.50 | 147.0 | 229.4 | 1 |
| clip_05 | True | False | False | 3.96 | 149.2 | 435.0 | 1 |
| clip_06 | False | False | False | 5.97 | 147.3 | 151.7 | 1 |
| clip_07 | False | False | False | 6.01 | 145.4 | 150.0 | 1 |
| clip_08 | False | False | False | 6.01 | 146.1 | 151.3 | 1 |
| clip_09 | False | False | False | 6.04 | 145.2 | 150.1 | 1 |
| clip_10 | False | False | False | 5.96 | 147.5 | 153.8 | 1 |
| clip_11 | False | False | False | 5.87 | 149.7 | 152.1 | 1 |
| gmdcsa_Fall_01 | True | True | True | 3.38 | 153.1 | 451.6 | 1 |
| gmdcsa_Fall_02 | True | True | True | 2.80 | 433.6 | 449.2 | 1 |
| gmdcsa_Fall_03 | True | True | True | 3.36 | 224.1 | 448.6 | 2 |
| gmdcsa_Fall_07 | True | True | True | 3.65 | 290.0 | 433.4 | 1 |
| gmdcsa_Fall_11 | True | True | True | 4.30 | 155.5 | 376.6 | 1 |
| gmdcsa_Fall_12 | True | True | True | 3.18 | 422.2 | 435.8 | 1 |
| gmdcsa_ADL_01 | False | False | True | 2.86 | 425.6 | 436.1 | 1 |
| gmdcsa_ADL_02 | False | False | True | 4.86 | 145.0 | 429.3 | 3 |
| gmdcsa_ADL_03 | False | False | True | 2.69 | 427.6 | 437.4 | 2 |
| gmdcsa_ADL_04 | False | False | True | 4.54 | 144.0 | 426.6 | 2 |
| gmdcsa_ADL_08 | False | False | False | 6.53 | 143.7 | 148.5 | 3 |
| gmdcsa_ADL_11 | False | False | False | 6.46 | 144.7 | 151.8 | 1 |
| gmdcsa_ADL_13 | False | False | False | 6.46 | 145.7 | 149.9 | 1 |

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
