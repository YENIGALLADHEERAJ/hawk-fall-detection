# Actual footage evaluation

small development set; not held-out accuracy or medical validation

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| gmdcsa_extra_s2_ADL_01 | False | False | False | 38.84 | 13.4 | 25.5 | 3 |
| gmdcsa_extra_s2_ADL_04 | False | False | True | 39.70 | 13.5 | 23.7 | 5 |
| gmdcsa_extra_s2_ADL_07 | False | False | False | 41.24 | 14.8 | 17.8 | 3 |
| gmdcsa_extra_s2_ADL_10 | False | False | True | 40.23 | 14.1 | 20.8 | 3 |
| gmdcsa_extra_s2_ADL_13 | False | False | False | 39.00 | 13.4 | 19.9 | 1 |
| gmdcsa_extra_s2_ADL_17 | False | False | True | 43.14 | 14.4 | 34.3 | 2 |
| gmdcsa_extra_s2_ADL_20 | False | False | False | 36.48 | 14.7 | 39.5 | 3 |
| gmdcsa_extra_s3_ADL_01 | False | False | False | 40.31 | 14.9 | 18.9 | 4 |
| gmdcsa_extra_s3_ADL_03 | False | False | True | 39.65 | 14.5 | 20.2 | 4 |
| gmdcsa_extra_s3_ADL_05 | False | False | False | 41.96 | 13.6 | 18.0 | 3 |
| gmdcsa_extra_s3_ADL_07 | False | False | False | 38.65 | 13.2 | 17.3 | 1 |
| gmdcsa_extra_s3_ADL_10 | False | False | False | 43.30 | 13.7 | 16.8 | 2 |
| gmdcsa_extra_s3_ADL_12 | False | False | False | 49.43 | 14.3 | 17.7 | 1 |
| gmdcsa_extra_s3_ADL_15 | False | False | True | 46.67 | 14.3 | 17.3 | 3 |
| gmdcsa_extra_s4_ADL_01 | False | False | False | 42.24 | 13.8 | 17.0 | 1 |
| gmdcsa_extra_s4_ADL_03 | False | False | False | 40.30 | 14.6 | 17.1 | 1 |
| gmdcsa_extra_s4_ADL_05 | False | False | True | 41.43 | 13.6 | 19.0 | 2 |
| gmdcsa_extra_s4_ADL_07 | False | False | True | 28.56 | 25.0 | 32.9 | 1 |
| gmdcsa_extra_s4_ADL_09 | False | False | False | 42.01 | 13.8 | 17.1 | 1 |
| gmdcsa_extra_s4_ADL_11 | False | False | False | 43.29 | 13.5 | 17.3 | 1 |
| gmdcsa_extra_s4_ADL_13 | False | False | False | 43.52 | 13.3 | 17.3 | 1 |

```json
{
  "immediate": {
    "positive_clips": 0,
    "negative_clips": 21,
    "true_positive_clips": 0,
    "false_positive_clips": 7,
    "event_recall": null,
    "precision": 0.0,
    "false_positive_clip_rate": 0.3333333333333333,
    "false_alert_events": 13,
    "negative_observation_hours": 0.051482607023605235,
    "false_alerts_per_negative_hour": 252.5124649192568
  },
  "temporal": {
    "positive_clips": 0,
    "negative_clips": 21,
    "true_positive_clips": 0,
    "false_positive_clips": 0,
    "event_recall": null,
    "precision": null,
    "false_positive_clip_rate": 0.0,
    "false_alert_events": 0,
    "negative_observation_hours": 0.051482607023605235,
    "false_alerts_per_negative_hour": 0.0
  }
}
```

Candidate detection and human-review alerts are separate outcomes. Refer to JSON for review times.
False-alarm reduction must be interpreted alongside recall; rejecting every clip is not success.
Latency uses publisher onset labels where available; missing labels remain null.
