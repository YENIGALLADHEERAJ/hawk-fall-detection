"""Measured per-sample diagnostics; absent detections remain explicitly absent."""
import math


def sample_record(index, timestamp, detections, tracks, observations, elapsed_ms):
    records = []
    by_id = {o.track_id: o for o in observations}
    for track in tracks:
        d, b = track.detection, track.detection.bbox
        prior = track.history[-2] if len(track.history) >= 2 else None
        dt = timestamp-prior.timestamp if prior else None
        dx = b.center[0]-prior.bbox.center[0] if prior else None
        dy = b.center[1]-prior.bbox.center[1] if prior else None
        o = by_id[track.track_id]
        records.append({'track_id': track.track_id, 'bbox': b.model_dump(),
            'center': b.center, 'area': b.w*b.h, 'aspect_ratio': b.w/b.h,
            'observed_gap_seconds': dt, 'dx_px': dx, 'dy_px': dy,
            'displacement_px': math.hypot(dx, dy) if prior else None,
            'velocity_px_s': track.velocity, 'trajectory':
                [[v.timestamp, *v.bbox.center] for v in track.history],
            'observation': o.model_dump(mode='json')})
    return {'frame_index': index, 'timestamp': timestamp,
        'detections': [d.model_dump(mode='json') for d in detections],
        'tracks': records, 'missing_visual_evidence': not bool(tracks),
        'processing_ms': elapsed_ms}
