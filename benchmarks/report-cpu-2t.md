# Measured perception performance

Replay (opencv, 2 threads) including evidence/debug encoding; not live throughput

| Detector input | Sampling FPS | Processing FPS | p50 ms | p95 ms | CPU % of one core |
|---|---|---|---|---|---|
| 320 | 5.0 | 11.49 | 49.6 | 111.2 | 247.9 |
| 320 | 10.0 | 15.07 | 40.2 | 114.5 | 183.4 |
| 320 | 15.0 | 13.74 | 41.0 | 109.6 | 217.0 |
| 320 | 30.0 | 15.02 | 40.5 | 114.1 | 197.9 |
| 640 | 5.0 | 5.95 | 146.6 | 157.2 | 203.5 |

```json
{
  "difference": {
    "p50_ms": 0.0011000010999850929,
    "p95_ms": 0.0020000006770715117,
    "samples": 50,
    "resolution": [
      96,
      96
    ]
  },
  "farneback": {
    "p50_ms": 0.6351999982143752,
    "p95_ms": 0.6585900009667967,
    "samples": 50,
    "resolution": [
      96,
      96
    ]
  }
}
```

Sampling FPS is footage-time cadence, not achieved processing throughput.
Multiple cores permit CPU usage above 100%. Short runs do not establish sustained thermal performance.
Motion timings are kernel microbenchmarks, not evidence of comparative fall accuracy.
