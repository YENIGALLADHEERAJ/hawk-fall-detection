# Actual footage evaluation

small development set; not held-out accuracy or medical validation

| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |
|---|---|---|---|---|---|---|---|
| mot17_02_crowd | False | False | False | 33.11 | 23.4 | 27.2 | 41 |
| mot17_04_crowd | False | False | False | 21.76 | 37.5 | 46.3 | 50 |

```json
{
  "immediate": {
    "positive_clips": 0,
    "negative_clips": 2,
    "true_positive_clips": 0,
    "false_positive_clips": 0,
    "event_recall": null,
    "precision": null,
    "false_positive_clip_rate": 0.0,
    "false_alert_events": 0,
    "negative_observation_hours": 0.005555555555555556,
    "false_alerts_per_negative_hour": 0.0
  },
  "temporal": {
    "positive_clips": 0,
    "negative_clips": 2,
    "true_positive_clips": 0,
    "false_positive_clips": 0,
    "event_recall": null,
    "precision": null,
    "false_positive_clip_rate": 0.0,
    "false_alert_events": 0,
    "negative_observation_hours": 0.005555555555555556,
    "false_alerts_per_negative_hour": 0.0
  }
}
```

Candidate detection and human-review alerts are separate outcomes. Refer to JSON for review times.
False-alarm reduction must be interpreted alongside recall; rejecting every clip is not success.
Latency uses publisher onset labels where available; missing labels remain null.
