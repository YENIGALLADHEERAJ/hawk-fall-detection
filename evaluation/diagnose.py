"""Export actual inference timelines and representative original/annotated frames."""
import argparse
import csv
import json
from pathlib import Path
import cv2
import numpy as np
from vision.schemas import Config, Detection, Motion
from vision.tracking import Track
from vision.temporal import TemporalEstimator


def export(run_dir, clip):
    run_dir = Path(run_dir)
    samples = [json.loads(s) for s in (run_dir/'diagnostics.jsonl').read_text().splitlines()]
    config = json.loads((run_dir/'metrics.json').read_text())['config']
    legacy_config={k:v for k,v in config.items() if k!='minimum_ground_width_ratio'}
    legacy = TemporalEstimator(Config(**legacy_config)) if not config.get('improved_temporal') else None
    if legacy:
        # Reconstruct explanations from recorded inputs; assert decisions are unchanged.
        for sample in samples:
            for track in sample['tracks']:
                o=track['observation']
                replay=legacy.update(Track(track['track_id'],Detection.model_validate(o['detection'])),
                                     Motion.model_validate(o['motion']),o['camera_id'])
                assert replay.state.value==o['state'] and replay.action==o['action']
                o['decision_reason']=replay.decision_reason
    destination = run_dir/'diagnostic-frames'
    destination.mkdir(exist_ok=True)
    transitions=[];last_states={}
    for sample in samples:
        for track in sample['tracks']:
            o=track['observation'];key=track['track_id'];state=(o['state'],o['action'])
            if last_states.get(key)!=state:
                transitions.append({'timestamp':sample['timestamp'],'frame_index':sample['frame_index'],
                    'track_id':key,'state':o['state'],'action':o['action'],
                    'reason':o.get('decision_reason'),'motion':o['motion'],
                    'transition_signals':o.get('transition_signals',{})})
            last_states[key]=state
    (run_dir/'state-transitions.json').write_text(json.dumps(transitions,indent=2))
    metrics=json.loads((run_dir/'metrics.json').read_text())
    (run_dir/'final-decision.json').write_text(json.dumps({k:metrics[k] for k in
        ['candidate_times','human_review_times','dismissed_candidates','exit_reason','incidents']},indent=2))
    fields = ['frame', 'timestamp', 'detections', 'track_id', 'x', 'y', 'width', 'height',
              'center_x', 'center_y', 'area', 'aspect_ratio', 'gap', 'dx', 'dy',
              'displacement', 'vx', 'vy', 'flow', 'motion_reliable', 'state', 'score',
              'fall_candidate', 'stationary_seconds', 'action', 'reason']
    with (run_dir/'timeline.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f); writer.writerow(fields)
        for sample in samples:
            prefix = [sample['frame_index'], sample['timestamp'], len(sample['detections'])]
            if not sample['tracks']:
                writer.writerow(prefix+['']*(len(fields)-4)+['missing_visual_evidence'])
            for track in sample['tracks']:
                o = track['observation']; b = track['bbox']; m = o['motion']
                writer.writerow(prefix+[track['track_id'], b['x'], b['y'], b['w'], b['h'],
                    *track['center'], track['area'], track['aspect_ratio'], track['observed_gap_seconds'],
                    track['dx_px'], track['dy_px'], track['displacement_px'], *track['velocity_px_s'],
                    m['flow_px_s'], m['reliable'], o['state'], o['evidence_score'], o['fall_candidate'],
                    o['stationary_duration'], o['action'], o.get('decision_reason', 'legacy state rule; see diagnosis')])
    if not samples:
        return
    onset = clip.get('incident_onset')
    targets = ([max(0,onset-.4), onset, onset+.4, onset+1.2, samples[-1]['timestamp']]
               if onset is not None else [0, samples[-1]['timestamp']*.4, samples[-1]['timestamp']*.7, samples[-1]['timestamp']])
    targets += [event['timestamp'] for event in transitions if event['action']!='observe']
    chosen = sorted({min(range(len(samples)), key=lambda i:abs(samples[i]['timestamp']-t)) for t in targets})
    if len(chosen)>12:chosen=chosen[:11]+chosen[-1:]
    cap = cv2.VideoCapture(clip['path']); panels=[]
    for i in chosen:
        sample = samples[i]; cap.set(cv2.CAP_PROP_POS_FRAMES,sample['frame_index']); ok, frame=cap.read()
        if not ok: raise RuntimeError('representative frame decode failed')
        h,w=frame.shape[:2]; scale=min(1,config['max_width']/max(h,w))
        frame=cv2.resize(frame,(round(w*scale),round(h*scale)))
        cv2.imwrite(str(destination/f'{i:04d}-original.jpg'),frame)
        annotated=frame.copy()
        for track in sample['tracks']:
            b=track['bbox'];o=track['observation'];x,y,bw,bh=map(round,(b['x'],b['y'],b['w'],b['h']))
            cv2.rectangle(annotated,(x,y),(x+bw,y+bh),(0,220,255),2)
            pts=np.array([v[1:] for v in track['trajectory']],np.int32)
            if len(pts)>1:cv2.polylines(annotated,[pts],False,(0,255,0),2)
            cv2.putText(annotated,f"ID {track['track_id']} {o['state']}",(x,max(15,y-5)),cv2.FONT_HERSHEY_SIMPLEX,.4,(0,255,255),1)
            flow=o['motion']['flow_px_s']
            measurement=f"vy={o['motion']['vy_px_s']:.1f} flow={flow:.1f}" if flow is not None else f"vy={o['motion']['vy_px_s']:.1f} flow=unknown"
            cv2.putText(annotated,measurement,(x,min(annotated.shape[0]-5,y+15)),cv2.FONT_HERSHEY_SIMPLEX,.35,(0,255,255),1)
        cv2.putText(annotated,f"t={sample['timestamp']:.3f} frame={sample['frame_index']}",(5,20),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),1)
        cv2.imwrite(str(destination/f'{i:04d}-annotated.jpg'),annotated)
        panels.append(cv2.resize(annotated,(320,240)))
    cap.release()
    while len(panels)%3:panels.append(np.zeros_like(panels[0]))
    cv2.imwrite(str(run_dir/'contact.jpg'),np.vstack([np.hstack(panels[i:i+3]) for i in range(0,len(panels),3)]))


def main():
    p=argparse.ArgumentParser();p.add_argument('results');a=p.parse_args()
    result=json.loads(Path(a.results).read_text())
    for row in result['clips']:
        if 'error' not in row:export(Path('data/evaluation')/result['run_id']/row['clip']['id'],row['clip'])


if __name__=='__main__':main()
