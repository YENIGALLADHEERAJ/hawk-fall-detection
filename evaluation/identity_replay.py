"""Replay recorded real detections through tracker variants on MOT17-09 (identity only).

No detector runs. Detections come from a recorded pipeline run (same frozen detector
configuration); frames come from the retained 5 Hz clip so appearance features see the
same pixels as the pipeline. Scored with the Phase 1C localization audit matcher, plus the
ownership failure that matters for fall history: one track id covering two different
reference people. This is a local audit, not MOTChallenge MOTA/IDF1/HOTA.
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path
import cv2
import numpy as np
from evaluation.localization_audit import summarize, xyxy, match
from vision.schemas import Detection
from vision.tracking import PersonTracker, appearance_feature

SOURCE = 'data/sources/mot17-09-audit'
CLIP = 'data/clips/fresh_mot17_09.avi'


def load(run_id, clip='fresh_mot17_09', source=SOURCE, video=CLIP):
    rows = [json.loads(s) for s in (Path('data/evaluation') / run_id / clip / 'diagnostics.jsonl').read_text().splitlines()]
    gt = np.loadtxt(f'{source}/gt.txt', delimiter=',')
    mapping = json.loads(Path(f'{source}/mapping.json').read_text())
    capture = cv2.VideoCapture(video); frames = []
    while True:
        ok, frame = capture.read()
        if not ok: break
        h, w = frame.shape[:2]
        scale = 640 / max(h, w)
        frames.append(cv2.resize(frame, (max(1, round(w * scale)), max(1, round(h * scale)))) if max(h, w) > 640 else frame)
    capture.release()
    return rows, gt, mapping, frames


def references(gt, mapping, row):
    refs = []
    for v in gt[gt[:, 0] == mapping[row['frame_index']]['original_frame']]:
        if v[6] != 1 or v[7] != 1 or v[8] <= 0: continue
        x, y, w, h = v[2:6] / 3
        b = [max(0, x), max(0, y), min(640, x + w), min(360, y + h)]
        if b[2] <= b[0] or b[3] <= b[1]: continue
        refs.append({'box': b, 'identity': int(v[1]), 'phase': 'visibility_low' if v[8] < .5 else 'visibility_high'})
    return refs


def replay(data, make_tracker, use_appearance=False):
    rows, gt, mapping, frames = data
    tracker = make_tracker(); samples = []; owner = {}; owner_changes = 0
    for row in rows:
        detections = [Detection.model_validate(d) for d in row['detections']]
        features = [appearance_feature(frames[row['frame_index']], d.bbox) for d in detections] if use_appearance else None
        tracks = tracker.update(detections, row['timestamp'], features) if use_appearance else tracker.update(detections, row['timestamp'])
        refs = references(gt, mapping, row)
        preds = [{'box': xyxy(t.detection.bbox.model_dump()), 'track_id': t.track_id} for t in tracks]
        for r, p in match([r['box'] for r in refs], [p['box'] for p in preds], .5).items():
            tid, ref = preds[p]['track_id'], refs[r]['identity']
            if tid in owner and owner[tid] != ref: owner_changes += 1
            owner[tid] = ref
        samples.append({'timestamp': row['timestamp'], 'references': refs, 'predictions': preds})
    s = summarize(samples)
    return {'id_changes': s['id_switches'], 'fragments': s['fragments_after_missing'],
            'owner_changes': owner_changes, 'recall_iou50': round(s['recall_iou50'], 4),
            'tracks_created': tracker.next_id - 1}


def main():
    p = argparse.ArgumentParser(); p.add_argument('--run-id', default='20261115T105816214382')
    p.add_argument('--output', default='evaluation/identity/replay.json')
    p.add_argument('--clip', default='fresh_mot17_09'); p.add_argument('--source', default=SOURCE); p.add_argument('--video', default=CLIP)
    p.add_argument('--run-dir', default=None, help='Directory under data/evaluation holding the recorded run (default: --run-id)')
    a = p.parse_args()
    data = load(a.run_dir or a.run_id, a.clip, a.source, a.video)
    def tracker(**k): return lambda: PersonTracker(1.5, improved=True, **k)
    result = {'scope': f'Replay of recorded real detections, clip {a.clip} (51 frames, 5 Hz). Weight 1.0 / decay .7 (and the optimal option) were first chosen on MOT17-09; '
              'any other clip is a held-out check of those fixed parameters.',
              'run_id': a.run_id, 'baseline': replay(data, tracker()), 'optimal_assignment_only': replay(data, tracker(optimal=True)),
              'appearance_only_greedy': replay(data, tracker(appearance_weight=1.0), True),
              'appearance_and_optimal': replay(data, tracker(appearance_weight=1.0, optimal=True), True), 'sweep': []}
    for w in (.3, .6, 1.0, 1.5, 2, 3, 5, 10):
        for gate in (1.0, .7):
            for optimal in (False, True):
                result['sweep'].append({'appearance_weight': w, 'appearance_gate': gate, 'optimal': optimal,
                    **replay(data, tracker(appearance_weight=w, appearance_gate=gate, optimal=optimal), True)})
    Path(a.output).parent.mkdir(parents=True, exist_ok=True); Path(a.output).write_text(json.dumps(result, indent=2))
    for k in ('baseline', 'optimal_assignment_only', 'appearance_only_greedy', 'appearance_and_optimal'): print(k, result[k])


if __name__ == '__main__': main()
