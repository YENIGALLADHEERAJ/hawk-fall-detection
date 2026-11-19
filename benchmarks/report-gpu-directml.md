# Measured perception performance

Replay (directml, 8 threads) including evidence/debug encoding; not live throughput

| Detector input | Sampling FPS | Processing FPS | p50 ms | p95 ms | CPU % of one core |
|---|---|---|---|---|---|
| 640 | 5.0 | 29.72 | 12.2 | 29.1 | 301.8 |
| 640 | 10.0 | 43.11 | 12.2 | 18.1 | 166.6 |
| 640 | 15.0 | 52.47 | 11.8 | 15.9 | 339.6 |
| 640 | 30.0 | 62.44 | 11.8 | 13.0 | 111.5 |

```json
{
  "difference": {
    "p50_ms": 0.0010000003385357559,
    "p95_ms": 0.0022000021999701858,
    "samples": 50,
    "resolution": [
      96,
      96
    ]
  },
  "farneback": {
    "p50_ms": 0.6355000004987232,
    "p95_ms": 0.6543400002556155,
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
