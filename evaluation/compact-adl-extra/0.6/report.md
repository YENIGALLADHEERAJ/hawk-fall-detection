# Actual footage evaluation

small development set; not held-out accuracy or medical validation

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| gmdcsa_extra_s2_ADL_01 | False | False | False | 40.62 | 14.0 | 18.0 | 3 |
| gmdcsa_extra_s2_ADL_04 | False | False | True | 36.52 | 14.9 | 25.3 | 5 |
| gmdcsa_extra_s2_ADL_07 | False | False | False | 38.21 | 15.4 | 19.1 | 3 |
| gmdcsa_extra_s2_ADL_10 | False | False | True | 38.90 | 14.4 | 18.7 | 3 |
| gmdcsa_extra_s2_ADL_13 | False | False | False | 39.51 | 13.3 | 32.0 | 1 |
| gmdcsa_extra_s2_ADL_17 | False | False | True | 40.86 | 14.9 | 34.0 | 2 |
| gmdcsa_extra_s2_ADL_20 | False | False | False | 39.03 | 13.9 | 34.9 | 3 |
| gmdcsa_extra_s3_ADL_01 | False | False | False | 41.16 | 14.1 | 18.2 | 4 |
| gmdcsa_extra_s3_ADL_03 | False | False | True | 40.00 | 14.4 | 23.1 | 4 |
| gmdcsa_extra_s3_ADL_05 | False | False | False | 39.66 | 13.9 | 18.8 | 3 |
| gmdcsa_extra_s3_ADL_07 | False | False | False | 37.30 | 13.8 | 23.5 | 1 |
| gmdcsa_extra_s3_ADL_10 | False | False | False | 42.94 | 13.5 | 17.3 | 2 |
| gmdcsa_extra_s3_ADL_12 | False | False | False | 52.43 | 13.4 | 16.9 | 1 |
| gmdcsa_extra_s3_ADL_15 | False | False | True | 45.18 | 13.7 | 18.0 | 3 |
| gmdcsa_extra_s4_ADL_01 | False | False | False | 41.09 | 13.7 | 17.7 | 1 |
| gmdcsa_extra_s4_ADL_03 | False | False | False | 41.61 | 13.8 | 16.4 | 1 |
| gmdcsa_extra_s4_ADL_05 | False | False | True | 39.44 | 13.6 | 19.2 | 2 |
| gmdcsa_extra_s4_ADL_07 | False | False | True | 28.96 | 23.6 | 30.7 | 1 |
| gmdcsa_extra_s4_ADL_09 | False | False | False | 40.68 | 14.0 | 18.0 | 1 |
| gmdcsa_extra_s4_ADL_11 | False | False | False | 39.92 | 14.1 | 18.1 | 1 |
| gmdcsa_extra_s4_ADL_13 | False | False | False | 39.76 | 14.5 | 17.1 | 1 |

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
