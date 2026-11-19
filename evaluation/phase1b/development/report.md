# Actual footage evaluation

small development set; not held-out accuracy or medical validation

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| clip_00 | True | True | True | 1.45 | 583.6 | 960.9 | 1 |
| clip_01 | None | False | False | 0.92 | 842.2 | 1522.3 | 1 |
| clip_02 | True | True | True | 0.81 | 1168.6 | 1392.5 | 1 |
| clip_03 | True | True | True | 0.73 | 1294.4 | 1702.9 | 1 |
| clip_04 | True | True | True | 1.54 | 525.0 | 919.0 | 1 |
| clip_05 | True | False | False | 1.20 | 486.4 | 1569.9 | 1 |
| clip_06 | False | True | False | 1.73 | 508.5 | 652.9 | 1 |
| clip_07 | False | False | False | 1.81 | 492.7 | 573.6 | 1 |
| clip_08 | False | False | False | 1.29 | 720.3 | 845.9 | 1 |
| clip_09 | False | False | False | 1.76 | 513.5 | 604.2 | 1 |
| clip_10 | False | False | False | 1.69 | 529.1 | 673.7 | 1 |
| clip_11 | False | False | False | 1.78 | 493.8 | 647.9 | 1 |
| gmdcsa_Fall_01 | True | True | True | 0.92 | 841.1 | 1702.3 | 1 |
| gmdcsa_Fall_02 | True | True | True | 0.69 | 1501.7 | 2419.6 | 1 |
| gmdcsa_Fall_03 | True | True | True | 0.89 | 955.2 | 1930.6 | 2 |
| gmdcsa_Fall_07 | True | True | True | 0.92 | 1078.9 | 1667.5 | 1 |
| gmdcsa_Fall_11 | True | True | True | 1.09 | 679.3 | 1600.2 | 1 |
| gmdcsa_Fall_12 | True | True | True | 0.80 | 1420.5 | 2222.1 | 1 |
| gmdcsa_ADL_01 | False | False | True | 0.68 | 1487.7 | 2849.1 | 1 |
| gmdcsa_ADL_02 | False | False | True | 1.25 | 572.0 | 1757.2 | 3 |
| gmdcsa_ADL_03 | False | False | True | 0.69 | 1521.2 | 2098.3 | 2 |
| gmdcsa_ADL_04 | False | False | True | 1.25 | 503.8 | 1648.4 | 2 |
| gmdcsa_ADL_08 | False | False | False | 1.80 | 511.6 | 690.4 | 3 |
| gmdcsa_ADL_11 | False | False | False | 1.53 | 575.2 | 957.2 | 1 |
| gmdcsa_ADL_13 | False | True | False | 1.74 | 521.7 | 749.0 | 1 |

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
    "negative_observation_hours": 0.016554408328914902,
    "false_alerts_per_negative_hour": 483.25496393771624
  },
  "temporal": {
    "positive_clips": 11,
    "negative_clips": 13,
    "true_positive_clips": 10,
    "false_positive_clips": 2,
    "event_recall": 0.9090909090909091,
    "precision": 0.8333333333333334,
    "false_positive_clip_rate": 0.15384615384615385,
    "false_alert_events": 2,
    "negative_observation_hours": 0.016554408328914902,
    "false_alerts_per_negative_hour": 120.81374098442906
  }
}
```

Candidate detection and human-review alerts are separate outcomes. Refer to JSON for review times.
False-alarm reduction must be interpreted alongside recall; rejecting every clip is not success.
Latency uses publisher onset labels where available; missing labels remain null.
