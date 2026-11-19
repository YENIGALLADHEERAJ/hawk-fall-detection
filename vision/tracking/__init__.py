from collections import deque
from dataclasses import dataclass, field
import math
import cv2
import numpy as np
from vision.schemas import Detection

BIG = 1e9


def appearance_feature(frame, box):
    """HSV colour histogram of the upper-body region (L1-normalised). None when the crop is too small.

    Cheap, deterministic, OpenCV-only. Not a re-identification model: clothing colour can be shared by
    different people, so it is only an association cue, never an identity claim.
    """
    h, w = frame.shape[:2]
    x1, x2 = int(box.x + .2 * box.w), int(box.x + .8 * box.w)
    y1, y2 = int(box.y + .12 * box.h), int(box.y + .55 * box.h)
    x1, y1, x2, y2 = max(0, x1), max(0, y1), min(w, x2), min(h, y2)
    if x2 - x1 < 4 or y2 - y1 < 4: return None
    hsv = cv2.cvtColor(frame[y1:y2, x1:x2], cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1, 2], None, [8, 4, 4], [0, 180, 0, 256, 0, 256]).ravel()
    total = hist.sum()
    return (hist / total).astype(np.float32) if total > 0 else None


def appearance_distance(a, b):
    """Bhattacharyya distance in [0, 1]; 0 identical. None if either side is missing."""
    if a is None or b is None: return None
    return float(np.sqrt(max(0., 1. - float(np.sum(np.sqrt(a * b))))))


def optimal_assignment(cost):
    """Minimum-cost one-to-one assignment (Hungarian, rows <= cols after transposition). Returns (row, col) pairs."""
    cost = np.asarray(cost, dtype=float)
    if cost.size == 0: return []
    transposed = cost.shape[0] > cost.shape[1]
    if transposed: cost = cost.T
    n, m = cost.shape
    u, v = np.zeros(n + 1), np.zeros(m + 1); way = np.zeros(m + 1, dtype=int); match = np.zeros(m + 1, dtype=int)
    for i in range(1, n + 1):
        match[0] = i; j0 = 0; minv = np.full(m + 1, np.inf); used = np.zeros(m + 1, dtype=bool)
        while True:
            used[j0] = True; i0 = match[j0]; delta = np.inf; j1 = 0
            for j in range(1, m + 1):
                if used[j]: continue
                cur = cost[i0 - 1, j - 1] - u[i0] - v[j]
                if cur < minv[j]: minv[j] = cur; way[j] = j0
                if minv[j] < delta: delta = minv[j]; j1 = j
            for j in range(m + 1):
                if used[j]: u[match[j]] += delta; v[j] -= delta
                else: minv[j] -= delta
            j0 = j1
            if match[j0] == 0: break
        while j0:
            j1 = way[j0]; match[j0] = match[j1]; j0 = j1
    pairs = [(match[j] - 1, j - 1) for j in range(1, m + 1) if match[j]]
    return [(c, r) for r, c in pairs] if transposed else pairs


def iou(a, b):
    inter = max(0, min(a.x+a.w, b.x+b.w)-max(a.x,b.x)) * max(0, min(a.y+a.h,b.y+b.h)-max(a.y,b.y))
    return inter / (a.w*a.h+b.w*b.h-inter)


@dataclass
class Track:
    track_id: int
    detection: Detection
    velocity: tuple[float, float] = (0., 0.)
    history: deque = field(default_factory=deque)
    feature: object = None

    @property
    def last_seen(self):
        return self.detection.timestamp


class PersonTracker:
    """Gated one-to-one box/velocity association; never emits missing tracks as observed."""
    def __init__(self, max_gap=.5, history_seconds=5, improved=False, prediction_horizon=.25, new_track_threshold=0, reject_short_ambiguity=False,
                 appearance_weight=0., appearance_gate=1., optimal=False, feature_decay=.7):
        self.tracks = {}
        self.next_id = 1
        self.max_gap = max_gap
        self.history_seconds = history_seconds
        self.last_timestamp = -1.
        self.improved = improved
        self.prediction_horizon = prediction_horizon
        self.new_track_threshold = new_track_threshold
        self.reject_short_ambiguity = reject_short_ambiguity
        self.appearance_weight = appearance_weight
        self.appearance_gate = appearance_gate
        self.optimal = optimal
        self.feature_decay = feature_decay

    def update(self, detections, timestamp, features=None):
        if not math.isfinite(timestamp) or timestamp <= self.last_timestamp:
            raise ValueError('timestamps must increase')
        self.last_timestamp = timestamp
        self.tracks = {k:t for k,t in self.tracks.items() if timestamp-t.last_seen <= self.max_gap}
        pairs = []
        for k, track in self.tracks.items():
            dt = timestamp-track.last_seen
            bx = track.detection.bbox
            horizon = min(dt,self.prediction_horizon) if self.improved else dt
            px, py = (bx.center[j]+track.velocity[j]*horizon for j in range(2))
            for i, det in enumerate(detections):
                dx, dy = det.bbox.center
                distance = math.hypot(dx-px,dy-py)/max(bx.h,bx.w,det.bbox.h,det.bbox.w)
                overlap = iou(bx, det.bbox)
                if det.confidence<self.new_track_threshold and (overlap<.1 or distance>=.45):continue
                if self.improved:
                    area_ratio = det.bbox.w*det.bbox.h/(bx.w*bx.h)
                    if not .2 <= area_ratio <= 5: continue
                if distance < .85 and (overlap > .05 or distance < .45):
                    cost = distance + (1-overlap)*.3
                    if features is not None and self.appearance_weight:
                        d_app = appearance_distance(track.feature, features[i])
                        if d_app is not None:
                            if d_app > self.appearance_gate: continue
                            cost += self.appearance_weight * d_app
                    pairs.append((cost,k,i))
        assigned, used, output = set(), set(), []
        ordered = sorted(pairs,key=lambda p:(detections[p[2]].confidence<self.new_track_threshold,p[0]))
        if self.optimal and pairs:
            # Global minimum-cost assignment over gated pairs; the greedy loop below then applies the
            # same ambiguity guard to the chosen pairs only.
            track_keys = sorted({p[1] for p in pairs}); det_keys = sorted({p[2] for p in pairs})
            matrix = np.full((len(track_keys), len(det_keys)), BIG)
            for cost, k, i in pairs: matrix[track_keys.index(k), det_keys.index(i)] = cost
            chosen = {(track_keys[r], det_keys[c]) for r, c in optimal_assignment(matrix) if matrix[r, c] < BIG}
            ordered = [p for p in ordered if (p[1], p[2]) in chosen]
        for cost, k, i in ordered:
            if k in assigned or i in used: continue
            if self.improved and (self.reject_short_ambiguity or timestamp-self.tracks[k].last_seen > .5):
                # Refuse ambiguous reattachment instead of transferring fall history.
                rivals = [other_cost for other_cost, other, j in pairs if j==i and other!=k and other not in assigned]
                if rivals and min(rivals)-cost < .1: continue
            track, det = self.tracks[k], detections[i]
            dt = timestamp-track.last_seen
            track.velocity = tuple((det.bbox.center[j]-track.detection.bbox.center[j])/dt for j in range(2))
            track.detection = det
            if features is not None and features[i] is not None:
                track.feature = features[i] if track.feature is None else (
                    self.feature_decay*track.feature + (1-self.feature_decay)*features[i])
            assigned.add(k); used.add(i); output.append(track)
        for i, det in enumerate(detections):
            if i not in used:
                if det.confidence<self.new_track_threshold:continue
                track = Track(self.next_id, det, feature=None if features is None else features[i])
                self.tracks[self.next_id] = track
                self.next_id += 1
                output.append(track)
        for track in output:
            track.history.append(track.detection)
            while track.history and timestamp-track.history[0].timestamp > self.history_seconds:
                track.history.popleft()
        return output
