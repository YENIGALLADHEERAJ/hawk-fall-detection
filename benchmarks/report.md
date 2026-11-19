# Measured perception performance

CPU replay including evidence/debug encoding; not live throughput

| Detector input | Sampling FPS | Processing FPS | p50 ms | p95 ms | CPU % of one core |
|---|---|---|---|---|---|
| 320 | 5.0 | 3.14 | 212.4 | 537.1 | 194.7 |
| 320 | 10.0 | 5.20 | 143.2 | 335.9 | 194.7 |
| 320 | 15.0 | 4.67 | 126.8 | 386.1 | 194.7 |
| 320 | 30.0 | 5.10 | 127.3 | 369.9 | 189.6 |
| 640 | 5.0 | 1.95 | 474.1 | 521.4 | 197.1 |

```json
{
  "difference": {
    "p50_ms": 0.004300032742321491,
    "p95_ms": 0.004554970655590296,
    "samples": 50,
    "resolution": [
      96,
      96
    ]
  },
  "farneback": {
    "p50_ms": 2.2391999955289066,
    "p95_ms": 3.344965080032125,
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
