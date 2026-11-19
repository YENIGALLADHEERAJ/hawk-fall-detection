# Open-source landscape

Reviewed 2026-10-25. Repository descriptions are not independently validated performance.
No external source code or model weights have been copied. License fields apply to
repository code unless explicitly stated; models and data need separate verification.

| Project / URL | License | Architecture, method, model, dataset | Strength / weakness | Overlap, learning, do not copy |
|---|---|---|---|---|
| [Ambianic fall-detection](https://github.com/ambianic/fall-detection) | Apache-2.0 | Python TensorFlow/PoseNet plus temporal heuristics; bundled examples/training data, provenance not audited | Interpretable; README documents occlusion, lighting and multi-person limitations | Strong fall overlap; learn failure taxonomy; do not inherit thresholds or accuracy claims |
| [SentinelCV](https://github.com/Shinraya-Tech-Labs/SentinelCV) | README claims MIT; standalone license text not verified | YOLOv8 → fall analysis → Telegram alerts; training weights/data not verified | Clear camera-to-alert demo; reproducibility still on roadmap | Direct CCTV safety overlap; useful immediate-alert baseline concept; do not copy code until license grant verified or reuse credentials |
| [OpenCV Zoo](https://github.com/opencv/opencv_zoo) | Apache-2.0 repository; per-model terms must be checked | OpenCV DNN ONNX model demos and benchmarks; MediaPipe person/pose candidates; upstream training provenance varies | Native inference examples; each exported graph must be tested | Reuse licensed model adapters with attribution after audit; never assume repo license covers every asset |
| [ByteTrack](https://github.com/FoundationVision/ByteTrack) | MIT | Two-stage association including low-score detections; YOLOX detection; MOT benchmarks | Established tracking baseline; detection and dataset domain mismatch remains | Learn association and ID continuity; not a fall classifier or cross-camera identity resolver |
| [YOLOX](https://github.com/Megvii-BaseDetection/YOLOX) | Apache-2.0 | Anchor-free object detection, nano/tiny options; COCO model family | Permissive detector candidate; no pose output | Alternative person proposals; do not infer prone-person accuracy from COCO scores |
| [Ultralytics](https://github.com/ultralytics/ultralytics) | AGPL-3.0 / enterprise terms | Integrated detection, pose and tracking; model-dependent datasets | Convenient exports and ecosystem; license obligations and larger dependency stack | Comparator, not selected dependency; ONNX export does not remove original license obligations |

Research extensions: [BoT-SORT](https://arxiv.org/abs/2206.14651) for moving cameras;
[SSHFD](https://arxiv.org/abs/2004.00797) for occlusion;
[temporal pose falls](https://arxiv.org/abs/2107.14633) for sequence reasoning;
[active perception](https://arxiv.org/abs/1603.02729) for evidence acquisition.
These are methodology references; code availability/license and reproduction remain
unverified unless listed above. Search coverage is a focused initial review, not an
exhaustive novelty search across every safety platform or MCP vision project.
