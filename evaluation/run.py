import argparse
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone
from vision.pipeline import run_video
from vision.schemas import Config
import cv2


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--manifest',default='datasets/manifest.json')
    parser.add_argument('--fps',type=float,default=5)
    parser.add_argument('--size',type=int,default=640)
    parser.add_argument('--output',default='evaluation')
    parser.add_argument('--variant',choices=['baseline','tracking','temporal','combined'],default='combined')
    parser.add_argument('--continuation-threshold',type=float,default=None)
    parser.add_argument('--all-views',action='store_true',help='Experimental three-view detector with NMS; threshold unchanged')
    parser.add_argument('--backend',choices=['opencv','directml'],default='opencv')
    parser.add_argument('--device-id',type=int,default=0)
    parser.add_argument('--threads',type=int,default=2)
    parser.add_argument('--identity-tracking',action='store_true',help='Experimental colour-histogram appearance cue in association')
    parser.add_argument('--optimal-assignment',action='store_true',help='Experimental global assignment (regressed on unseen footage)')
    parser.add_argument('--compact-collapse-ratio',type=float,default=None,help='Experimental: accept horizontal collapse-in-place down to this height ratio (e.g. 0.6)')
    args=parser.parse_args()
    clips=json.loads(Path(args.manifest).read_text(encoding='utf-8'))
    config=Config(sample_fps=args.fps,detector_size=args.size,continuation_threshold=args.continuation_threshold,rotation_all_views=args.all_views,
                  improved_tracking=args.variant in ('tracking','combined'),
                  improved_temporal=args.variant in ('temporal','combined'),
                  identity_tracking=args.identity_tracking,optimal_assignment=args.optimal_assignment,compact_collapse_height_ratio=args.compact_collapse_ratio,detector_backend=args.backend,detector_device=args.device_id,threads=args.threads)
    run_id=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')
    rows=[]
    for clip in clips:
        if hashlib.sha256(Path(clip['path']).read_bytes()).hexdigest()!=clip['sha256']:
            raise ValueError(f"clip checksum mismatch: {clip['id']}")
        try:
            metrics=run_video(clip['path'],f"data/evaluation/{run_id}/{clip['id']}",config)
            # A positive clip label is not a calibrated diagnosis or temporal label.
            candidate=bool(metrics['candidate_times']); immediate=bool(metrics['baseline_alert_times'])
            rows.append({'clip':clip,'metrics':{k:v for k,v in metrics.items() if k!='incidents'},
                'candidate_detected':candidate,'baseline_detected':immediate,
                'latency_seconds':metrics['candidate_times'][0]-clip['incident_onset']
                    if candidate and clip.get('incident_onset') is not None else None})
            print(clip['id'],'candidate',candidate,'review',bool(metrics['human_review_times']),flush=True)
        except (ValueError,RuntimeError,OSError,cv2.error) as exc:
            rows.append({'clip':clip,'error':str(exc)})
    valid=[r for r in rows if 'error' not in r and r['clip'].get('event_present') is not None]
    positives=[r for r in valid if r['clip']['event_present']]
    negatives=[r for r in valid if not r['clip']['event_present']]
    comparison={}
    for name,key in [('immediate','baseline_detected'),('temporal','candidate_detected')]:
        tp=sum(r[key] for r in positives); fp=sum(r[key] for r in negatives)
        comparison[name]={'positive_clips':len(positives),'negative_clips':len(negatives),
            'true_positive_clips':tp,'false_positive_clips':fp,
            'event_recall':tp/len(positives) if positives else None,
            'precision':tp/(tp+fp) if tp+fp else None,
            'false_positive_clip_rate':fp/len(negatives) if negatives else None}
        time_key='baseline_alert_times' if name=='immediate' else 'candidate_times'
        false_events=sum(len(r['metrics'][time_key]) for r in negatives)
        negative_hours=sum(r['metrics']['observed_seconds'] for r in negatives)/3600
        comparison[name]['false_alert_events']=false_events
        comparison[name]['negative_observation_hours']=negative_hours
        comparison[name]['false_alerts_per_negative_hour']=false_events/negative_hours if negative_hours else None
    held_out=bool(clips) and all(c.get('split')=='subject_held_out_no_retuning' for c in clips)
    result={'scope':('reused subject-held-out clips for Phase 1B regression; not unseen generalization' if held_out and args.variant!='baseline' else
                    'small subject-held-out set; original baseline configuration; not medical validation' if held_out
                     else 'small development set; not held-out accuracy or medical validation'),
        'variant':args.variant,
        'run_id':run_id,'configuration':config.model_dump(),'comparison':comparison,'clips':rows,
        'tracking_idf1':None,'tracking_note':'distinct IDs are a fragmentation proxy; no identity annotations',
        'missing_scenarios':['natural multi-person','fall followed by immediate recovery']}
    if clips and all(c.get('split')=='fresh_validation' for c in clips):
        result['scope']='Fresh Phase 1C validation, first measurement of frozen Phase 1B configuration; reserved final test untouched. Sparse localization audit reported separately.'
        result['missing_scenarios']=['real multi-person fall with occlusion and crossing','fall followed by immediate recovery']
        if args.all_views: result['scope']='Paired Phase 1C validation experiment: all three rotation views, confidence unchanged; not untouched test evidence.'
    out=Path(args.output);out.mkdir(exist_ok=True,parents=True)
    (out/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    lines=['# Actual footage evaluation','',result['scope'],'',
        '| Clip | Label | Candidate | Immediate | FPS | p50 ms | p95 ms | IDs |',
        '|---|---|---|---|---|---|---|---|']
    for row in rows:
        if 'error' in row: lines.append(f"Error {row['clip']['id']}: {row['error']}");continue
        m=row['metrics'];lines.append(f"| {row['clip']['id']} | {row['clip'].get('event_present')} | {row['candidate_detected']} | {row['baseline_detected']} | {m['processing_fps']:.2f} | {m['p50_ms']:.1f} | {m['p95_ms']:.1f} | {m['distinct_track_ids']} |")
    lines += ['', '```json',json.dumps(comparison,indent=2),'```','',
        'Candidate detection and human-review alerts are separate outcomes. Refer to JSON for review times.',
        'False-alarm reduction must be interpreted alongside recall; rejecting every clip is not success.',
        'Latency uses publisher onset labels where available; missing labels remain null.']
    (out/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')


if __name__=='__main__':main()
