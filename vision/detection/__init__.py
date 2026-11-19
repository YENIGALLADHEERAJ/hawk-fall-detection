"""Replaceable detector contract and real OpenCV DNN implementation."""
from pathlib import Path
from typing import Protocol
import cv2
import numpy as np
from vision.schemas import Box, Detection


class PersonDetector(Protocol):
    def detect(self, frame: np.ndarray, timestamp: float, frame_index: int) -> list[Detection]: ...


class YoloXDetector:
    """YOLOX export from OpenCV Zoo, RGB 0..255, top-left letterbox.

    Decoder follows the model's documented grid/stride contract. Original HAWK
    adapter: class filtering, bounds checks, typed outputs and timestamp handling.
    See third_party/YOLOX-LICENSE and docs/model-selection.md.
    """
    def __init__(self, model='data/models/yolox.onnx', threshold=.3, size=640, rotation_fallback=True, all_views=False,
                 backend='opencv', device_id=0, threads=2):
        if cv2.__version__.split('.')[0] != '5':
            raise RuntimeError('OpenCV 5 is required')
        if not Path(model).is_file():
            raise FileNotFoundError(model)
        self.backend = backend
        if backend == 'opencv':
            self.net = cv2.dnn.readNetFromONNX(str(model))
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        elif backend == 'directml':
            # Same model and decoder through ONNX Runtime on a DirectX 12 GPU. device_id is the
            # DirectML adapter index (machine specific). Never falls back silently to CPU.
            import onnxruntime as ort
            if 'DmlExecutionProvider' not in ort.get_available_providers():
                raise RuntimeError('onnxruntime-directml is required for the directml backend')
            options = ort.SessionOptions()
            options.enable_mem_pattern = False
            options.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
            options.intra_op_num_threads = threads
            self.session = ort.InferenceSession(str(model), options,
                providers=[('DmlExecutionProvider', {'device_id': device_id})])
            if self.session.get_providers()[0] != 'DmlExecutionProvider':
                raise RuntimeError('DirectML provider was not activated')
            self.input_name = self.session.get_inputs()[0].name
        else:
            raise ValueError(f'unknown detector backend {backend!r}')
        self.threshold = threshold
        self.size = size
        self.rotation_fallback = rotation_fallback
        self.all_views = all_views
        grids, strides = [], []
        for stride in (8, 16, 32):
            y, x = np.mgrid[:size // stride, :size // stride]
            grids.append(np.stack((x, y), axis=-1).reshape(-1, 2))
            strides.append(np.full((x.size, 1), stride))
        self.grid, self.stride = np.concatenate(grids), np.concatenate(strides)

    def detect(self, frame, timestamp, frame_index):
        detections=self._detect_single(frame,timestamp,frame_index)
        if (detections and not self.all_views) or not self.rotation_fallback: return detections
        h,w=frame.shape[:2]
        for rotate,name in [(cv2.ROTATE_90_CLOCKWISE,'clockwise'),(cv2.ROTATE_90_COUNTERCLOCKWISE,'counterclockwise')]:
            rotated=self._detect_single(cv2.rotate(frame,rotate),timestamp,frame_index)
            for det in rotated:
                b=det.bbox
                if name=='clockwise': x,y,bw,bh=b.y,h-b.x-b.w,b.h,b.w
                else: x,y,bw,bh=w-b.y-b.h,b.x,b.h,b.w
                det.bbox=Box(x=max(0,x),y=max(0,y),w=min(bw,w-max(0,x)),h=min(bh,h-max(0,y)))
                det.inference_view=name
            if rotated and not self.all_views: return rotated
            detections.extend(rotated)
        if not detections: return []
        keep=cv2.dnn.NMSBoxes([[d.bbox.x,d.bbox.y,d.bbox.w,d.bbox.h] for d in detections],
            [d.confidence for d in detections],self.threshold,.5)
        return [detections[int(i)] for i in np.asarray(keep).reshape(-1)]

    def _detect_single(self, frame, timestamp, frame_index):
        if frame is None or frame.ndim != 3 or frame.shape[2] != 3 or frame.dtype != np.uint8:
            raise ValueError('expected nonempty uint8 BGR frame')
        h, w = frame.shape[:2]
        if min(h, w) == 0:
            raise ValueError('empty frame')
        scale = min(self.size / w, self.size / h)
        resized = cv2.resize(frame, (max(1, int(w * scale)), max(1, int(h * scale))))
        canvas = np.full((self.size, self.size, 3), 114, dtype=np.uint8)
        canvas[:resized.shape[0], :resized.shape[1]] = resized
        blob = cv2.dnn.blobFromImage(canvas, swapRB=True)
        if self.backend == 'opencv':
            self.net.setInput(blob)
            raw = self.net.forward()[0]
        else:
            raw = self.session.run(None, {self.input_name: blob})[0][0]
        if raw.shape != (len(self.grid), 85) or not np.isfinite(raw).all():
            raise RuntimeError(f'unexpected YOLOX output {raw.shape}')
        scores = raw[:, 4] * raw[:, 5]
        mask = (scores >= self.threshold) & (raw[:, 5:].argmax(axis=1) == 0)
        centers = (raw[mask, :2] + self.grid[mask]) * self.stride[mask] / scale
        sizes = np.exp(np.clip(raw[mask, 2:4], -20, 20)) * self.stride[mask] / scale
        boxes = np.concatenate((centers - sizes / 2, sizes), axis=1)
        scores = scores[mask]
        keep = cv2.dnn.NMSBoxes(boxes.tolist(), scores.tolist(), self.threshold, .5)
        result = []
        for i in np.asarray(keep).reshape(-1):
            x, y, bw, bh = boxes[i]
            x1, y1, x2, y2 = max(0, x), max(0, y), min(w, x + bw), min(h, y + bh)
            if x2 > x1 and y2 > y1:
                result.append(Detection(bbox=Box(x=x1, y=y1, w=x2-x1, h=y2-y1),
                    confidence=float(scores[i]), timestamp=timestamp, frame_index=frame_index))
        return result
