"""RTMPose-m (COCO-17, SimCC) person keypoints reduced to small, explicit posture evidence.

Top-down: the tracked person box is cropped (padding 1.25, 192x256), the network returns SimCC
x/y distributions, keypoints are the argmax positions. Keypoints below a peak-score floor are
dropped, so a missing joint gives None for the features that need it, never a guess.
"""
import math
import cv2
import numpy as np
import onnxruntime as ort
from vision.schemas import PoseEvidence

W, H = 192, 256
MEAN = np.array([123.675, 116.28, 103.53], np.float32)
STD = np.array([58.395, 57.12, 57.375], np.float32)
FLOOR = .3   # SimCC peak value; not a calibrated probability
SHOULDERS, HIPS, ANKLES = (5, 6), (11, 12), (15, 16)


class PoseEstimator:
    def __init__(self, model, backend='opencv', device_id=0, floor=FLOOR):
        self.floor = floor
        options = ort.SessionOptions()
        if backend == 'directml':
            if 'DmlExecutionProvider' not in ort.get_available_providers():
                raise RuntimeError('DirectML provider unavailable; refusing silent CPU fallback')
            options.enable_mem_pattern = False
            options.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
            providers = [('DmlExecutionProvider', {'device_id': device_id})]
        else:
            providers = ['CPUExecutionProvider']
        self.session = ort.InferenceSession(model, options, providers=providers)
        if backend == 'directml' and self.session.get_providers()[0] != 'DmlExecutionProvider':
            raise RuntimeError('DirectML provider was not activated for the pose model')

    def keypoints(self, frame, bbox):
        """(17, 3) array of x, y (frame pixels) and peak score."""
        w, h = bbox.w, bbox.h
        cx, cy = bbox.x + w / 2, bbox.y + h / 2
        if w > h * W / H: h = w * H / W
        else: w = h * W / H
        w, h = w * 1.25, h * 1.25
        sx, sy = W / w, H / h
        m = np.array([[sx, 0, W / 2 - cx * sx], [0, sy, H / 2 - cy * sy]], np.float32)
        crop = cv2.warpAffine(frame, m, (W, H), flags=cv2.INTER_LINEAR)
        img = (crop[:, :, ::-1].astype(np.float32) - MEAN) / STD
        kx, ky = self.session.run(None, {'input': img.transpose(2, 0, 1)[None]})
        kx, ky = kx[0], ky[0]
        px, py = kx.argmax(1) / 2.0, ky.argmax(1) / 2.0   # simcc_split_ratio 2
        return np.stack([(px - W / 2) / sx + cx, (py - H / 2) / sy + cy, np.minimum(kx.max(1), ky.max(1))], 1)

    def estimate(self, frame, bbox):
        if bbox.w <= 1 or bbox.h <= 1: return PoseEvidence()
        return evidence(self.keypoints(frame, bbox), self.floor)


def evidence(kp, floor=FLOOR):
    ok = lambda i: kp[i, 2] >= floor
    def mid(pair):
        pts = [kp[i, :2] for i in pair if ok(i)]
        return np.mean(pts, 0) if pts else None
    shoulder, hip, ankle = mid(SHOULDERS), mid(HIPS), mid(ANKLES)
    hip_ankle = float(ankle[1] - hip[1]) if hip is not None and ankle is not None else None
    angle = None
    if shoulder is not None and hip is not None:
        v = hip - shoulder
        a = math.degrees(math.atan2(abs(v[0]), abs(v[1])))
        angle = float(a if v[1] >= 0 else 180 - a)
    return PoseEvidence(hip_ankle_px=hip_ankle, torso_angle_deg=angle, keypoints=int((kp[:, 2] >= floor).sum()))
