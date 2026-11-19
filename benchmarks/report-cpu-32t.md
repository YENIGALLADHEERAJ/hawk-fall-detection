# Measured perception performance

Replay (opencv, 32 threads) including evidence/debug encoding; not live throughput

| Detector input | Sampling FPS | Processing FPS | p50 ms | p95 ms | CPU % of one core |
|---|---|---|---|---|---|
| 320 | 5.0 | 22.32 | 25.7 | 40.8 | 1485.5 |
| 320 | 10.0 | 32.80 | 15.6 | 38.7 | 1864.1 |
| 320 | 15.0 | 32.06 | 16.4 | 39.4 | 1803.3 |
| 320 | 30.0 | 37.22 | 16.1 | 39.6 | 1925.5 |
| 640 | 5.0 | 15.84 | 43.8 | 52.8 | 1574.1 |

```json
{
  "difference": {
    "p50_ms": 0.0011000010999850929,
    "p95_ms": 0.0014549998013535512,
    "samples": 50,
    "resolution": [
      96,
      96
    ]
  },
  "farneback": {
    "p50_ms": 0.6350000003294554,
    "p95_ms": 0.6398500005161623,
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
