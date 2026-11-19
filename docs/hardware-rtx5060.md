# Re-run on new hardware — 2026-11-15

Machine: AMD Ryzen 9 9955HX (16 cores / 32 threads), NVIDIA GeForce RTX 5060 Laptop GPU (8 GiB, driver 621.14), 15.2 GiB RAM, Windows 11, Python 3.11.1, OpenCV 5.0.0, ONNX Runtime DirectML 1.24.4. The previous measurements (Phase 1C) were on an i5-10210U / MX250 / 8 GB machine.

**Nothing about perception quality changed; only speed did.** Every detection-level outcome below is identical across the GPU, 32-thread CPU and 2-thread CPU configurations, and identical to the Phase 1C results from the old machine. The Phase 1C INCOMPLETE verdict and its blockers (identity continuity, one missed fall, one false-positive clip, coverage gaps) stand unchanged.

## What was run

`scripts/run_all_hardware.ps1` and `scripts/run_benchmarks_hardware.ps1`, sequentially, nothing else running during timed work. Same frozen configuration as Phase 1B/1C (.3 confidence, 640 input, combined variant, rotation fallback). Three detector setups:

| Setup | Detector execution |
|---|---|
| gpu-directml | Same YOLOX ONNX model through ONNX Runtime DirectML on the RTX 5060 (adapter 1; adapter 0 is the integrated AMD GPU) |
| cpu-32t | OpenCV 5 DNN, CPU, 32 threads |
| cpu-2t | OpenCV 5 DNN, CPU, 2 threads (the Phase 1C setting) |

OpenCV's own DNN cannot use this GPU: the pip wheel has no CUDA and OpenCV 5's new graph engine ignores target selection ("Targets are not supported by the new graph engine"). The GPU path is therefore ONNX Runtime, an added optional dependency (`requirements-gpu.txt`).

## Parity

On 30 sampled frames (25 detections) of a fall clip, GPU and CPU gave identical detection counts, maximum box difference 0.0002 px and confidence difference under 1e-3. Test `tests/test_backends.py` asserts this. The audit sets the DirectML adapter by index, which is machine specific (`--device-id`, or `HAWK_DML_DEVICE` for the test).

## Accuracy (identical on every setup)

| Set | Fall recall | False-positive non-fall clips |
|---|---|---|
| Development (25 clips) | 10/11 | 0/13 |
| Subject-held-out regression (5 clips) | 2/2 | 0/3 |
| Fresh Phase 1C validation (15 clips) | 7/8 | 1/7 |

Localization audit on the fresh set, all three setups and the Phase 1C baseline: sparse matches 78/83 (recall .940 at IoU .5, .892 at .75), MOT17 342/397 (.861 / .683), **37 ID changes and 12 fragments on MOT17**. Bit-identical. The tests passed 57/57 (54 existing + 3 new) in 28 s (`docs/test-results-rtx5060.txt`).

## Raw model inference (640x640, one frame)

| Path | p50 ms | p95 ms |
|---|---:|---:|
| OpenCV CPU, 2 threads | 142.9 | 145.4 |
| OpenCV CPU, 8 threads | 54.6 | 58.4 |
| OpenCV CPU, 16 threads | 41.7 | 43.0 |
| OpenCV CPU, 32 threads | 37.2 | 38.8 |
| ONNX Runtime CPU, 16 threads | 40.5 | 42.7 |
| DirectML, integrated AMD GPU | 80.7 | 83.2 |
| DirectML, RTX 5060 | **6.1** | 6.1 |

## Full pipeline, fresh set (15 clips, 705 sampled frames, 5 Hz sampling)

| Setup | Processing FPS | p50 ms | p95 ms | Detector share of stage time | Process peak MiB |
|---|---:|---:|---:|---:|---:|
| gpu-directml | **40.4** | 13.7 | 32.0 | 72.6% | 478 |
| cpu-32t | 15.8 | 46.5 | 121.4 | 90.7% | 275 |
| cpu-2t | 5.1 | 157.9 | 350.8 | 97.3% | 272 |
| Phase 1C, old machine | 1.46 | 528.6 | 1443.8 | 97.7% | 229 |

Across all 45 evaluation clips: GPU ~17.7–20.9 FPS on the development/holdout sets (first-run timings), cpu-32t ~12–13, cpu-2t ~4.0–4.2.

Source-sampling benchmark on `clip_00` (`benchmarks/report-*.md`): GPU 29.7 / 43.1 / 52.5 / 62.4 FPS at 5 / 10 / 15 / 30 Hz sampling; cpu-32t 15.8 FPS at 640 input and 5 Hz; cpu-2t 5.95. The 320-input rows exist for the CPU only, because the shipped ONNX has a static 640 input. `benchmarks/report.md` and `results.json` remain the old-machine measurements.

**The 5 FPS processing target is now met** on this machine by every setup at 5 Hz sampling (the old 2-thread setting barely, 5.1), and with large margin on the GPU, which also covers 30 Hz sampling. This is a measurement on one machine with short clips; sustained thermal behavior, live camera capture and a real webcam were not tested.

With the GPU, the detector falls to about 73% of stage time; motion (10.8%), visualization (8.3%) and evidence (5.9%) are now visible. GPU memory use was not measured.

## Measurement caveats (honest record)

- One clip in the first GPU fresh run took 188 s of wall time (3.26 FPS for the set) while other work was active on the machine. A clean re-run (`evaluation/rtx5060/gpu-directml-fresh-rerun`) gave 40.4 FPS with identical detections; the 40.4 figure is the one used. The first run is kept as `gpu-directml/fresh`.
- Part of the first cpu-2t run overlapped a benchmark. Its development set was re-run cleanly (`cpu-2t-dev-rerun`: 4.15 FPS vs 4.02), detections identical.
- Benchmarks that overlapped the evaluation were discarded and re-run.
- Everything here is replay of local files, includes evidence and debug-video encoding, and does not measure accuracy beyond the covered clips. Validation sets remain seen validation; no final reserve was opened.

## Now possible, not done

The speed headroom makes the previously rejected `rotation_all_views` experiment and other detector-heavy experiments cheap to repeat, and pose estimation or a larger detector now fit the time budget. None was run or adopted; each needs its own measured comparison. The next step on the critical path is still identity continuity through overlapping people.
