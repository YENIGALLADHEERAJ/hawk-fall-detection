"""Fail-closed OpenCV 5 compatibility probe, not a fall-detection benchmark."""
import ctypes
import json
import platform
import sys
import time
from pathlib import Path

import cv2
import numpy as np


def main():
    if cv2.__version__.split('.')[0] != '5':
        raise RuntimeError(f'OpenCV 5 required; found {cv2.__version__}')
    cv2.setNumThreads(1)
    rng = np.random.default_rng(42)
    first = rng.integers(0, 256, (120, 160), dtype=np.uint8)
    second = np.roll(first, 3, axis=1)
    durations = []
    for i in range(25):
        start = time.perf_counter_ns()
        flow = cv2.calcOpticalFlowFarneback(first, second, None, .5, 3, 15, 3, 5, 1.2, 0)
        if i >= 5:
            durations.append((time.perf_counter_ns() - start) / 1e6)
    assert flow.shape == (120, 160, 2) and np.isfinite(flow).all()
    assert 2 < float(np.median(flow[20:-20, 20:-20, 0])) < 4
    gray = cv2.cvtColor(cv2.cvtColor(first, cv2.COLOR_GRAY2BGR), cv2.COLOR_BGR2GRAY)
    assert np.array_equal(gray, first)
    delta = cv2.absdiff(first, second)
    assert cv2.countNonZero(delta) > 0
    assert cv2.resize(first, (80, 60)).shape == (60, 80)
    ok, encoded = cv2.imencode('.png', first)
    assert ok and np.array_equal(cv2.imdecode(encoded, 0), first)
    ram = None
    if sys.platform == 'win32':
        class Memory(ctypes.Structure):
            _fields_ = [('length', ctypes.c_uint32), ('load', ctypes.c_uint32)] + [
                (name, ctypes.c_uint64) for name in ('total', 'available', 'page', 'available_page', 'virtual', 'available_virtual', 'extended')]
        memory = Memory()
        memory.length = ctypes.sizeof(memory)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory)):
            ram = round(memory.total / 2**30, 2)
    result = {
        'scope': 'synthetic API smoke test; no real-world accuracy claim',
        'python': sys.version, 'platform': platform.platform(), 'ram_gib': ram,
        'opencv': cv2.__version__, 'numpy': np.__version__, 'threads': cv2.getNumThreads(),
        'flow_median_x': float(np.median(flow[20:-20, 20:-20, 0])),
        'flow_p50_ms': float(np.percentile(durations, 50)),
        'flow_p95_ms': float(np.percentile(durations, 95)),
        'samples': len(durations), 'resolution': [160, 120],
        'dnn_available': hasattr(cv2.dnn, 'readNetFromONNX'),
        'capture_available': hasattr(cv2, 'VideoCapture'),
        'status': 'passed'
    }
    target = Path(__file__).resolve().parents[1] / 'docs' / 'environment-verification.json'
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
