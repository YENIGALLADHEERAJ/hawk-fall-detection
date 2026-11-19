# Phase 1 model, tracker and motion decisions

This updates Phase 0: geometry is the initial posture proxy; pose is optional.

| Detector | CPU/size/license/compatibility tradeoff | Decision |
|---|---|---|
| OpenCV Zoo YOLOX ONNX | 35,858,002-byte artifact; Apache-2.0 per model directory; executes in OpenCV 5 without another inference runtime | Selected, measured on real frames at 320/640; prone/occluded recall remains a failure mode |
| OpenCV Zoo MediaPipe person detector | CPU-oriented person proposal model; model-specific license must accompany weights; oriented proposals useful for pose | Deferred: would require another decoder and real prone-person validation; no measured comparison claimed |
| OpenCV Zoo NanoDet | Lightweight general detector; another CPU-friendly OpenCV DNN route | Candidate for later speed comparison; not downloaded or benchmarked in this phase |
| Ultralytics nano detector/pose | Convenient ecosystem but AGPL/enterprise obligations and additional export tooling | Not installed; no need to add PyTorch for this phase |

Sources: [YOLOX model](https://github.com/opencv/opencv_zoo/tree/main/models/object_detection_yolox),
[MediaPipe model](https://github.com/opencv/opencv_zoo/tree/main/models/person_detection_mediapipe),
[NanoDet](https://github.com/opencv/opencv_zoo/tree/main/models/object_detection_nanodet),
[Ultralytics license](https://www.ultralytics.com/license).

YOLOX input contract: RGB float32 in 0..255; top-left letterbox filled with 114;
grid/stride decode; objectness times person class score; person-only NMS; coordinates
mapped back to processed-frame pixels. No ImageNet normalization. Dynamic square
input sizes 320, 416 and 640 were exercised successfully. Rotating a difficult prone
frame did not initially recover detection, but clockwise/counterclockwise passes on
a second clip did recover it. The selected detector tries those views only if the
original view has no detections, records the inference view, and maps boxes back.
This costs up to three DNN passes and does not recover a missed person when another
person is already detected. It is a real inference fallback, not predicted boxes.
Model hash and download provenance are in `datasets/assets.json`.

Tracker alternatives: centroid-only association is cheap but ignores overlap;
Kalman filtering can smooth motion but requires covariance tuning and still depends
on association; ByteTrack additionally uses low-confidence detections and is stronger
under occlusion, with more integration/validation work. Selected: gated box overlap
and velocity-predicted center association with one-to-one greedy matching. It is not
ByteTrack, does not claim reliable crossings, and emits only current detections.
Missed detections never become synthetic person boxes. Short gaps reset stationary
duration; expired identities reset temporal evidence.

Motion combines normalized centroid velocity with real Farneback flow on a 96×96
person ROI. Frame difference is recorded as an auxiliary signal. Flow is gated by
brightness, texture, frame continuity and track continuity. It cannot distinguish
person motion from camera shake; this limitation remains in the failure gallery.
The flow unit is pixels/second in the normalized ROI, not original-frame pixels.

Posture is bounding-box aspect ratio, not skeletal orientation or center of mass.
Temporal evidence requires an observed upright-to-downward-to-horizontal sequence.
Thresholds are centralized in `Config`. The descent threshold was reduced from
0.45 to 0.25 body-heights/second after development clips showed slow descents were
missed; this is development tuning, not an independently validated optimum.

No pose estimator was installed. Geometry is adequate for testing the plumbing but
is insufficient for dependable discrimination of intentional lying down, sitting
falls, foreshortening and occlusion. Those failures determine whether pose earns its
cost in a later revision; an LLM cannot repair missing visual evidence.
