"""Pose-feature probe on recorded person boxes (research only; no pipeline change).

For each tracked person observation in a recorded run, crop the box, run RTMPose-m (COCO-17,
SimCC) and derive two simple posture features:
  hip_height  = (mean ankle y - mean hip y) / reference_height   (0 when hips are at ankle level)
  torso_angle = angle of shoulder-mid -> hip-mid from vertical, degrees (0 upright, 90 horizontal)
reference_height is the largest box height seen for that track so far in the clip (an upright proxy).
Keypoints below the confidence floor are dropped; missing keypoints give None, never a guess.
"""
import argparse
import json
import math
from pathlib import Path
import cv2

from vision.pose import PoseEstimator
from vision.schemas import Config, Box


def session(device_id=None):
    return PoseEstimator(Config().pose_model, 'directml' if device_id is not None else 'opencv', device_id or 0)


def features(pose, ref_h):
    return {'hip_height': None if pose.hip_ankle_px is None else round(pose.hip_ankle_px / ref_h, 2),
            'torso_angle': None if pose.torso_angle_deg is None else round(pose.torso_angle_deg, 0), 'n_kp': pose.keypoints}


def frames_at(path, times):
    cap = cv2.VideoCapture(path); out = {}
    for t in times:
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, f = cap.read()
        if not ok: continue
        h, w = f.shape[:2]; s = 640 / max(h, w)
        out[t] = cv2.resize(f, (max(1, round(w * s)), max(1, round(h * s)))) if max(h, w) > 640 else f
    cap.release()
    return out


def probe(results_path, clip_id, sess):
    r = json.loads(Path(results_path).read_text())
    clip = next(c['clip'] for c in r['clips'] if c['clip']['id'] == clip_id)
    rows = [json.loads(s) for s in (Path('data/evaluation') / r['run_id'] / clip_id / 'diagnostics.jsonl').read_text().splitlines()]
    # follow the track that becomes widest (proxy for the person who changes posture)
    widest = {}
    for row in rows:
        for t in row['tracks']:
            b = t['bbox']; widest[t['track_id']] = max(widest.get(t['track_id'], 0), b['w'] / b['h'])
    tid = max(widest, key=widest.get)
    frames = frames_at(clip['path'], [row['timestamp'] for row in rows])
    ref = 0; series = []
    for row in rows:
        for t in row['tracks']:
            if t['track_id'] != tid or row['timestamp'] not in frames: continue
            b = t['bbox']; ref = max(ref, b['h'])
            f = features(sess.estimate(frames[row['timestamp']], Box(**b)), ref)
            series.append({'t': round(row['timestamp'], 1), 'w_h': round(b['w'] / b['h'], 2), 'h_ratio': round(b['h'] / ref, 2),
                           **f, 'candidate': t['observation']['fall_candidate']})
    return {'clip': clip_id, 'track': tid, 'event_present': clip['event_present'], 'series': series}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('results'); p.add_argument('clips', nargs='+'); p.add_argument('--output', required=True)
    p.add_argument('--device-id', type=int, default=None)
    a = p.parse_args()
    sess = session(a.device_id)
    out = [probe(a.results, c, sess) for c in a.clips]
    Path(a.output).parent.mkdir(parents=True, exist_ok=True); Path(a.output).write_text(json.dumps(out, indent=1))
    for o in out:
        print('==', o['clip'], 'track', o['track'], 'event', o['event_present'])
        for s in o['series']:
            print(' ', s['t'], 'w/h', s['w_h'], 'hr', s['h_ratio'], 'hipH', s['hip_height'], 'torso', s['torso_angle'], 'kp', s['n_kp'], 'C' if s['candidate'] else '')


if __name__ == '__main__': main()
