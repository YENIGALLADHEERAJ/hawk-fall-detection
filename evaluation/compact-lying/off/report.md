# Actual footage evaluation

small development set; not held-out accuracy or medical validation

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| gmdcsa_lying_s2_ADL_03 | False | False | True | 34.83 | 14.2 | 35.3 | 4 |
| gmdcsa_lying_s2_ADL_12 | False | False | True | 27.43 | 31.5 | 41.5 | 1 |
| gmdcsa_lying_s2_ADL_16 | False | False | True | 29.83 | 33.7 | 38.4 | 1 |
| gmdcsa_lying_s2_ADL_08 | False | True | True | 38.03 | 15.4 | 21.3 | 6 |
| gmdcsa_lying_s3_ADL_08 | False | False | True | 24.45 | 36.1 | 39.7 | 1 |
| gmdcsa_lying_s3_ADL_06 | False | False | True | 39.86 | 14.3 | 18.3 | 1 |
| gmdcsa_lying_s4_ADL_08 | False | False | True | 39.22 | 14.5 | 24.5 | 1 |
| gmdcsa_lying_s4_ADL_10 | False | False | True | 29.12 | 25.4 | 34.0 | 1 |
| gmdcsa_lying_s4_ADL_15 | False | False | True | 29.64 | 21.9 | 33.0 | 1 |
| gmdcsa_lying_s4_ADL_16 | False | False | True | 28.48 | 17.0 | 33.1 | 1 |
| gmdcsa_lying_s3_ADL_03 | False | False | True | 34.86 | 16.1 | 22.3 | 4 |

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
