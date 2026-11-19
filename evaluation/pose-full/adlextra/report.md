# Actual footage evaluation

small development set; not held-out accuracy or medical validation

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| gmdcsa_extra_s2_ADL_01 | False | False | False | 41.86 | 15.7 | 20.2 | 3 |
| gmdcsa_extra_s2_ADL_04 | False | False | True | 35.74 | 16.9 | 25.6 | 5 |
| gmdcsa_extra_s2_ADL_07 | False | False | False | 29.62 | 22.8 | 30.4 | 3 |
| gmdcsa_extra_s2_ADL_10 | False | False | True | 31.22 | 21.3 | 34.5 | 3 |
| gmdcsa_extra_s2_ADL_13 | False | False | False | 17.26 | 27.3 | 77.0 | 1 |
| gmdcsa_extra_s2_ADL_17 | False | False | True | 22.74 | 28.3 | 49.1 | 2 |
| gmdcsa_extra_s2_ADL_20 | False | False | False | 22.82 | 28.0 | 47.7 | 3 |
| gmdcsa_extra_s3_ADL_01 | False | False | False | 21.47 | 28.3 | 38.0 | 4 |
| gmdcsa_extra_s3_ADL_03 | False | False | True | 21.01 | 30.7 | 41.0 | 4 |
| gmdcsa_extra_s3_ADL_05 | False | False | False | 21.44 | 26.5 | 43.2 | 3 |
| gmdcsa_extra_s3_ADL_07 | False | False | False | 20.78 | 25.9 | 46.0 | 1 |
| gmdcsa_extra_s3_ADL_10 | False | False | False | 22.42 | 26.3 | 45.5 | 2 |
| gmdcsa_extra_s3_ADL_12 | False | False | False | 27.86 | 25.4 | 30.2 | 1 |
| gmdcsa_extra_s3_ADL_15 | False | False | True | 23.71 | 26.3 | 39.7 | 3 |
| gmdcsa_extra_s4_ADL_01 | False | False | False | 24.07 | 25.9 | 31.9 | 1 |
| gmdcsa_extra_s4_ADL_03 | False | False | False | 22.33 | 26.6 | 33.5 | 1 |
| gmdcsa_extra_s4_ADL_05 | False | False | True | 21.22 | 27.9 | 49.5 | 2 |
| gmdcsa_extra_s4_ADL_07 | False | False | True | 17.55 | 39.9 | 49.9 | 1 |
| gmdcsa_extra_s4_ADL_09 | False | False | False | 24.12 | 25.7 | 30.5 | 1 |
| gmdcsa_extra_s4_ADL_11 | False | False | False | 22.87 | 27.6 | 34.5 | 1 |
| gmdcsa_extra_s4_ADL_13 | False | False | False | 20.11 | 26.1 | 48.3 | 1 |

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
