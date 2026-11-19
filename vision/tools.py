from collections import deque
from time import perf_counter
from vision.schemas import WindowRequest, WindowResult
from vision.schemas import RegionRequest, RegionResult
import cv2
import numpy as np


class EvidenceTools:
    """Real analysis over observed evidence; bounded to ten seconds / 300 samples."""
    def __init__(self):
        self.history = deque(maxlen=300)
        self.calls = []

    def add(self, observation):
        self.history.append(observation)
        while self.history and observation.timestamp-self.history[0].timestamp > 10:
            self.history.popleft()

    def analyze_temporal_window(self, request: WindowRequest) -> WindowResult:
        start = perf_counter()
        # Revalidate even when a caller supplies a constructed model.
        request = WindowRequest.model_validate(request.model_dump())
        if self.history and request.end > self.history[-1].timestamp + .001:
            raise ValueError('cannot inspect future evidence')
        rows = [o for o in self.history if o.track_id == request.track_id and request.start <= o.timestamp <= request.end]
        coverage = rows[-1].timestamp-rows[0].timestamp if len(rows)>1 else 0.
        valid = len(rows)>=2 and all(o.motion.reliable for o in rows[1:])
        result = WindowResult(status='ok' if valid else 'insufficient_evidence',observations=rows,
            coverage_seconds=coverage, stationary_seconds=rows[-1].stationary_duration if rows else 0.,
            recovery_observed=any(o.action=='dismiss' for o in rows),
            latency_ms=(perf_counter()-start)*1000,reason='observed history only; no future frames')
        self.calls.append({'tool':'analyze_temporal_window','input':request.model_dump(),
                           'output':result.model_dump(mode='json')})
        return result

    def inspect_region(self, request: RegionRequest, frame: np.ndarray) -> RegionResult:
        start=perf_counter()
        request=RegionRequest.model_validate(request.model_dump())
        if frame is None or frame.dtype!=np.uint8 or frame.ndim!=3 or max(frame.shape[:2])>1280:
            raise ValueError('expected bounded uint8 BGR frame')
        b=request.bbox
        if b.x+b.w>frame.shape[1]+.01 or b.y+b.h>frame.shape[0]+.01:
            raise ValueError('ROI outside frame')
        roi=frame[int(b.y):int(b.y+b.h),int(b.x):int(b.x+b.w)]
        if min(roi.shape[:2])<2: raise ValueError('ROI too small')
        gray=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
        bright=float(gray.mean()); texture=float(gray.std())
        result=RegionResult(status='ok' if bright>=15 and texture>=3 else 'insufficient_evidence',
            brightness=bright,texture_std=texture,laplacian_variance=float(cv2.Laplacian(gray,cv2.CV_32F).var()),
            latency_ms=(perf_counter()-start)*1000,reason='image quality only; not identity or diagnosis')
        self.calls.append({'tool':'inspect_region','input':request.model_dump(),'output':result.model_dump()})
        return result
