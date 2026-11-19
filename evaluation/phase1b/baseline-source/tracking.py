from collections import deque
from dataclasses import dataclass, field
import math
from vision.schemas import Detection


def iou(a, b):
    inter = max(0, min(a.x+a.w, b.x+b.w)-max(a.x,b.x)) * max(0, min(a.y+a.h,b.y+b.h)-max(a.y,b.y))
    return inter / (a.w*a.h+b.w*b.h-inter)


@dataclass
class Track:
    track_id: int
    detection: Detection
    velocity: tuple[float, float] = (0., 0.)
    history: deque = field(default_factory=deque)

    @property
    def last_seen(self):
        return self.detection.timestamp


class PersonTracker:
    """Gated one-to-one box/velocity association; never emits missing tracks as observed."""
    def __init__(self, max_gap=.5, history_seconds=5):
        self.tracks = {}
        self.next_id = 1
        self.max_gap = max_gap
        self.history_seconds = history_seconds
        self.last_timestamp = -1.

    def update(self, detections, timestamp):
        if not math.isfinite(timestamp) or timestamp <= self.last_timestamp:
            raise ValueError('timestamps must increase')
        self.last_timestamp = timestamp
        self.tracks = {k:t for k,t in self.tracks.items() if timestamp-t.last_seen <= self.max_gap}
        pairs = []
        for k, track in self.tracks.items():
            dt = timestamp-track.last_seen
            bx = track.detection.bbox
            px, py = (bx.center[j]+track.velocity[j]*dt for j in range(2))
            for i, det in enumerate(detections):
                dx, dy = det.bbox.center
                distance = math.hypot(dx-px,dy-py)/max(bx.h,bx.w,det.bbox.h,det.bbox.w)
                overlap = iou(bx, det.bbox)
                if distance < .85 and (overlap > .05 or distance < .45):
                    pairs.append((distance + (1-overlap)*.3,k,i))
        assigned, used, output = set(), set(), []
        for _, k, i in sorted(pairs):
            if k in assigned or i in used: continue
            track, det = self.tracks[k], detections[i]
            dt = timestamp-track.last_seen
            track.velocity = tuple((det.bbox.center[j]-track.detection.bbox.center[j])/dt for j in range(2))
            track.detection = det
            assigned.add(k); used.add(i); output.append(track)
        for i, det in enumerate(detections):
            if i not in used:
                track = Track(self.next_id, det)
                self.tracks[self.next_id] = track
                self.next_id += 1
                output.append(track)
        for track in output:
            track.history.append(track.detection)
            while track.history and timestamp-track.history[0].timestamp > self.history_seconds:
                track.history.popleft()
        return output
