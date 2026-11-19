# Actual footage evaluation

small development set; not held-out accuracy or medical validation

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| gmdcsa_lying_s2_ADL_03 | False | False | True | 26.70 | 21.1 | 43.3 | 4 |
| gmdcsa_lying_s2_ADL_12 | False | False | True | 19.55 | 36.2 | 44.4 | 1 |
| gmdcsa_lying_s2_ADL_16 | False | False | True | 22.74 | 39.4 | 46.0 | 1 |
| gmdcsa_lying_s2_ADL_08 | False | True | True | 20.08 | 33.1 | 51.5 | 6 |
| gmdcsa_lying_s3_ADL_08 | False | False | True | 16.23 | 49.6 | 59.4 | 1 |
| gmdcsa_lying_s3_ADL_06 | False | False | True | 22.97 | 26.1 | 41.4 | 1 |
| gmdcsa_lying_s4_ADL_08 | False | False | True | 23.15 | 26.1 | 39.7 | 1 |
| gmdcsa_lying_s4_ADL_10 | False | False | True | 20.37 | 37.2 | 43.6 | 1 |
| gmdcsa_lying_s4_ADL_15 | False | False | True | 19.67 | 36.9 | 42.7 | 1 |
| gmdcsa_lying_s4_ADL_16 | False | False | True | 21.61 | 27.2 | 42.5 | 1 |
| gmdcsa_lying_s3_ADL_03 | False | False | True | 21.14 | 32.4 | 41.4 | 4 |

```json
{
  "immediate": {
    "positive_clips": 0,
    "negative_clips": 11,
    "true_positive_clips": 0,
    "false_positive_clips": 11,
    "event_recall": null,
    "precision": 0.0,
    "false_positive_clip_rate": 1.0,
    "false_alert_events": 15,
    "negative_observation_hours": 0.029140403727656857,
    "false_alerts_per_negative_hour": 514.7492169356478
  },
  "temporal": {
    "positive_clips": 0,
    "negative_clips": 11,
    "true_positive_clips": 0,
    "false_positive_clips": 1,
    "event_recall": null,
    "precision": 0.0,
    "false_positive_clip_rate": 0.09090909090909091,
    "false_alert_events": 1,
    "negative_observation_hours": 0.029140403727656857,
    "false_alerts_per_negative_hour": 34.31661446237652
  }
}
```

Candidate detection and human-review alerts are separate outcomes. Refer to JSON for review times.
False-alarm reduction must be interpreted alongside recall; rejecting every clip is not success.
Latency uses publisher onset labels where available; missing labels remain null.
