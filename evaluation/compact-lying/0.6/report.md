# Actual footage evaluation

small development set; not held-out accuracy or medical validation

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| gmdcsa_lying_s2_ADL_03 | False | False | True | 33.66 | 15.1 | 35.3 | 4 |
| gmdcsa_lying_s2_ADL_12 | False | False | True | 29.36 | 19.1 | 35.1 | 1 |
| gmdcsa_lying_s2_ADL_16 | False | False | True | 29.74 | 33.4 | 37.7 | 1 |
| gmdcsa_lying_s2_ADL_08 | False | True | True | 36.96 | 15.6 | 18.6 | 6 |
| gmdcsa_lying_s3_ADL_08 | False | False | True | 24.13 | 35.7 | 42.7 | 1 |
| gmdcsa_lying_s3_ADL_06 | False | False | True | 38.04 | 14.6 | 18.5 | 1 |
| gmdcsa_lying_s4_ADL_08 | False | False | True | 39.91 | 14.1 | 24.4 | 1 |
| gmdcsa_lying_s4_ADL_10 | False | False | True | 31.67 | 24.4 | 28.8 | 1 |
| gmdcsa_lying_s4_ADL_15 | False | False | True | 31.79 | 24.3 | 28.0 | 1 |
| gmdcsa_lying_s4_ADL_16 | False | False | True | 36.08 | 14.6 | 27.5 | 1 |
| gmdcsa_lying_s3_ADL_03 | False | False | True | 33.13 | 17.3 | 22.6 | 4 |

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
