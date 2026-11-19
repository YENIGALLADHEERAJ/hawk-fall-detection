# HAWK — Hazard Assessment & Watchkeeping

**HAWK doesn't just see an incident. It investigates it.**

Status: Phase 1 local perception prototype. Real OpenCV 5 inference, tracking,
temporal evidence, local debug video and evaluation are implemented. This is an
offline research prototype, not a validated safety system. No AWS or LLM deployment.

Start with [the technical decision report](docs/architecture-decisions.md),
[research](docs/research.md), and [environment audit](docs/environment-audit.md).

The current pipeline uses YOLOX person boxes, gated tracking, bounding-box geometry
and optical flow. Bounded tools inspect observed history and ROI quality. Pose is
not a dependency. Missing detections are never replaced with fabricated person boxes.

## Verify the vision environment

Use Python 3.12 in an isolated environment:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-vision.txt
.\.venv\Scripts\python.exe scripts/verify_environment.py
```

The local machine's Python command is broken; see the audit for the working
runtime and installation workaround. The probe rejects OpenCV 4. It measures
only synthetic optical-flow execution, never incident accuracy.
On Windows, `scripts/bootstrap.ps1 -Python '<working Python executable>'` also
supports creating the venv without ensurepip and installing through external pip.

## Run real footage

```powershell
.\.venv\Scripts\python.exe scripts/fetch_assets.py
.\.venv\Scripts\python.exe -m vision.run data/clips/gmdcsa_Fall_11.mp4 --output data/my-run --fps 5 --view
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m evaluation.run
.\.venv\Scripts\python.exe -m benchmarks.perception
```

Choose a fresh output directory for every run. Omit `--view` for headless execution;
`debug.avi` remains available. Press Q in the debug window to stop. Sampling FPS is
video-time cadence, not achieved processing FPS. Local files are the validated mode.
For explicitly requested webcam capture, run:

```powershell
.\.venv\Scripts\python.exe -m vision.run --camera 0 --output data/camera-run --fps 5 --max-seconds 30 --view
.\.venv\Scripts\python.exe -m evaluation.run --manifest datasets/holdout.json --output evaluation/holdout
```

Camera capture has a two-second read timeout and at most two reconnect attempts,
with the native capture backend isolated in a terminable process. Transport tests
pass; a physical webcam has not been validated. RTSP is not implemented. The selected
detector cannot sustain 5 processing FPS on this machine; live capture drops queued
frames and uses capture timestamps rather than pretending to process them all.

Outputs: `observations.jsonl`, `trace.json`, `metrics.json`, `debug.avi` and bounded
incident packets containing original/annotated frames, observed video windows and
JSON evidence. Scores are heuristic evidence strength, not calibrated probabilities.
Keep raw evidence local and delete obsolete run directories after review; automatic
time-based retention is not yet implemented. Per-run duration and packet counts are capped.

See [model choices](docs/model-selection.md), [footage attribution](datasets/README.md),
[actual evaluation](evaluation/report.md), and [measured performance](benchmarks/report.md).
Phase 1B's default `combined` variant detected both previously missed falls with no
false candidates in the three non-fall clips. These clips now inform development;
the [five-configuration evaluation](evaluation/holdout/report.md) is a regression
comparison, not unseen-test accuracy. Phase 1 validation remains open.
Use `--variant baseline` to reproduce the original algorithm. The experimental
`--continuation-threshold 0.15` accepts weaker detections only for existing tracks;
it is not enabled by default because visual inspection found poor localization.
See the report for its measured tradeoffs.
The next phase is the agent layer only after the remaining perception validation
gaps are accepted or resolved. Never infer a medical condition from these outputs.

## GPU detector backend (optional)

`pip install -r requirements-gpu.txt` adds ONNX Runtime DirectML. Then pass
`--backend directml --device-id N` to `vision.run`, `evaluation.run` or `benchmarks.perception`
(`N` is the DirectML adapter index, machine specific; on the development machine the RTX 5060 is 1).
OpenCV remains the default backend and `--threads` controls CPU threads. Detections match the CPU path
(see [hardware report](docs/hardware-rtx5060.md)); on that machine the pipeline processes about 40 FPS at
5 Hz sampling versus 5 FPS for the old 2-thread CPU setting. Perception quality is unchanged.

Experimental identity continuity: `--identity-tracking` (colour-histogram appearance cue); see
[identity-tracking.md](docs/identity-tracking.md). Off by default; lowered ID changes on all three MOT17 clips tested (88 to 60 in total), not a solution.
