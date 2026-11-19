# OpenCV 5 API validation and implementation plan

Status: Phase 1 real perception implemented. The original [probe](../scripts/verify_environment.py)
remains useful, while [evaluation](../evaluation/report.md) and
[benchmarks](../benchmarks/report.md) contain actual pipeline measurements.

| Component | API | Input → output / purpose | Status |
|---|---|---|---|
| Preprocessing | cvtColor, resize | BGR/gray arrays → normalized-size gray | Executed and asserted |
| Motion | absdiff, countNonZero | Frame pair → changed pixels | Executed and asserted |
| Temporal motion | calcOpticalFlowFarneback | Two gray frames → dense XY flow | Known-shift assertion and measured latency |
| Evidence encoding | imencode, imdecode | Array ↔ PNG | Lossless round trip asserted |
| Person detection | dnn.readNetFromONNX, blobFromImage, Net.forward, NMSBoxes | ONNX + RGB tensor → person boxes | Actual YOLOX inference on licensed video |
| Capture | VideoCapture | Recorded files → timestamped frames | Decoding exercised; live camera reconnect pending |
| Tracking | Python box/velocity association | Person measurements → per-camera tracks | Implemented; no KalmanFilter claim |
| Alternate view | rotate | Same camera image → rotated inference view | Real fallback when original detector finds no people |
| Quality | Laplacian, cvtColor | ROI → brightness/texture/sharpness metrics | Real inspect_region tool |
| Debug/evidence | VideoWriter, imwrite, rectangle, line, putText | Frames + measurements → local AVI/JPEG | Saved and decoded in integration validation |

OpenCV is appropriate for reproducible CPU image and temporal computation on the
local machine and cloud worker. Model wrappers must use correct channel order,
letterboxing and coordinate inversion. Frame timestamps must be monotonic and
flow must never span a discontinuity or missing-camera interval.

The probe uses 160×120 synthetic texture, one thread, five warmups and twenty timed
runs. These measurements are not detector latency or throughput. Benchmark real
resolutions, decode, DNN and complete tools separately in the Phase 1 benchmark. Migration reference:
[official OpenCV 5 notes](https://github.com/opencv/opencv/wiki/OpenCV-5).
