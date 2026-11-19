"""Detector backend parity: DirectML (GPU) must reproduce the OpenCV CPU decoder output."""
import unittest
from pathlib import Path
import cv2
import numpy as np
from vision.detection import YoloXDetector
from vision.schemas import Config

CLIP = 'data/clips/fresh_gmd4_Fall_03.mp4'
try:
    import onnxruntime as ort
    HAVE_DML = 'DmlExecutionProvider' in ort.get_available_providers()
except ImportError:
    HAVE_DML = False


class BackendTests(unittest.TestCase):
    def test_config_validates_backend(self):
        self.assertEqual(Config().detector_backend, 'opencv')
        with self.assertRaises(Exception): Config(detector_backend='cuda')
        self.assertEqual(Config(threads=32).threads, 32)

    def test_unknown_backend_rejected(self):
        with self.assertRaises(ValueError): YoloXDetector(backend='nope')

    @unittest.skipUnless(HAVE_DML and Path(CLIP).is_file(), 'needs onnxruntime-directml and the clip')
    def test_directml_matches_opencv(self):
        cpu, gpu = YoloXDetector(), YoloXDetector(backend='directml', device_id=int(__import__('os').environ.get('HAWK_DML_DEVICE', 1)))
        cap = cv2.VideoCapture(CLIP); compared = 0
        for i in range(0, 120, 6):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i); ok, frame = cap.read()
            if not ok: break
            a = sorted(cpu.detect(frame, 0, i), key=lambda d: d.bbox.x)
            b = sorted(gpu.detect(frame, 0, i), key=lambda d: d.bbox.x)
            self.assertEqual(len(a), len(b))
            for x, y in zip(a, b):
                self.assertLess(abs(x.bbox.x - y.bbox.x) + abs(x.bbox.w - y.bbox.w), 1.0)
                self.assertLess(abs(x.confidence - y.confidence), 1e-3)
            compared += len(a)
        cap.release()
        self.assertGreater(compared, 0)


if __name__ == '__main__': unittest.main()
