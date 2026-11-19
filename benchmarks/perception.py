"""Run sequentially without competing inference jobs."""
import json
import time
from pathlib import Path
from datetime import datetime, timezone
import cv2
import numpy as np
from vision.pipeline import run_video
from vision.schemas import Config


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--backend', choices=['opencv', 'directml'], default='opencv')
    ap.add_argument('--device-id', type=int, default=0)
    ap.add_argument('--threads', type=int, default=2)
    ap.add_argument('--tag', default='', help='suffix for results/report file names, e.g. gpu-directml')
    args = ap.parse_args()
    suffix = f'-{args.tag}' if args.tag else ''
    root = Path('data/benchmarks') / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')
    rows = []
    grid = [(320, 5), (320, 10), (320, 15), (320, 30), (640, 5)]
    if args.backend == 'directml':  # static 640x640 ONNX input; 320 needs a separate export
        grid = [(640, 5), (640, 10), (640, 15), (640, 30)]
    for size, fps in grid:
        print('benchmark', size, fps, flush=True)
        result = run_video('data/clips/clip_00.mp4', root / f'{size}-{fps}',
                           Config(detector_size=size, sample_fps=fps, detector_backend=args.backend,
                                  detector_device=args.device_id, threads=args.threads))
        rows.append({k: v for k, v in result.items() if k != 'incidents'})
    capture = cv2.VideoCapture('data/clips/clip_00.mp4')
    _, a = capture.read()
    _, b = capture.read()
    capture.release()
    a = cv2.resize(cv2.cvtColor(a, cv2.COLOR_BGR2GRAY), (96, 96))
    b = cv2.resize(cv2.cvtColor(b, cv2.COLOR_BGR2GRAY), (96, 96))
    measurements = {}
    for name, operation in [('difference', lambda: cv2.absdiff(a, b)),
            ('farneback', lambda: cv2.calcOpticalFlowFarneback(a, b, None, .5, 2, 15, 2, 5, 1.2, 0))]:
        values = []
        for i in range(55):
            start = time.perf_counter()
            operation()
            if i >= 5:
                values.append((time.perf_counter() - start) * 1000)
        measurements[name] = {'p50_ms': float(np.percentile(values, 50)),
            'p95_ms': float(np.percentile(values, 95)), 'samples': 50, 'resolution': [96, 96]}
    result = {'scope': f'Replay ({args.backend}, {args.threads} threads) including evidence/debug encoding; not live throughput', 'backend': args.backend, 'device_id': args.device_id, 'threads': args.threads,
              'runs': rows, 'motion_microbenchmarks': measurements}
    Path(f'benchmarks/results{suffix}.json').write_text(json.dumps(result, indent=2))
    lines = ['# Measured perception performance', '', result['scope'], '',
        '| Detector input | Sampling FPS | Processing FPS | p50 ms | p95 ms | CPU % of one core |',
        '|---|---|---|---|---|---|']
    for row in rows:
        lines.append(f"| {row['config']['detector_size']} | {row['config']['sample_fps']} | {row['processing_fps']:.2f} | {row['p50_ms']:.1f} | {row['p95_ms']:.1f} | {row['cpu_one_core_percent']:.1f} |")
    lines += ['', '```json', json.dumps(measurements, indent=2), '```', '',
        'Sampling FPS is footage-time cadence, not achieved processing throughput.',
        'Multiple cores permit CPU usage above 100%. Short runs do not establish sustained thermal performance.',
        'Motion timings are kernel microbenchmarks, not evidence of comparative fall accuracy.']
    Path(f'benchmarks/report{suffix}.md').write_text('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main()
