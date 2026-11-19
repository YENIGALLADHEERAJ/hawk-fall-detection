"""Diagnose existing recorded associations before changing their implementation."""
import json
import math
from pathlib import Path
import cv2
import numpy as np
from evaluation.localization_audit import match,xyxy,iou


def references(frame):
    gt=np.loadtxt('data/sources/mot17-09-audit/gt.txt',delimiter=',')
    refs=[]
    for v in gt[gt[:,0]==frame*6+1]:
        if v[6]!=1 or v[7]!=1 or v[8]<=0:continue
        x,y,w,h=v[2:6]/3;b=[max(0,x),max(0,y),min(640,x+w),min(360,y+h)]
        if b[2]>b[0] and b[3]>b[1]:refs.append({'identity':int(v[1]),'box':b,'visibility':v[8]})
    return refs


def diagnose(run_id,output):
    root=Path('data/evaluation')/run_id/'fresh_mot17_09';out=Path(output);out.mkdir(parents=True,exist_ok=True)
    rows=[json.loads(s) for s in (root/'diagnostics.jsonl').read_text().splitlines()]
    previous={};owners={};by_ref={};events=[];all_records=[];panels=[]
    for row in rows:
        refs=references(row['frame_index']);tracks=row['tracks']
        pairs=match([r['box'] for r in refs],[xyxy(t['bbox']) for t in tracks],.5)
        assigned={p:refs[r] for r,p in pairs.items()}
        for i,tr in enumerate(tracks):
            tid=tr['track_id'];prior=previous.get(tid);box=tr['bbox'];b=xyxy(box);o=tr['observation']
            rec={'frame':row['frame_index'],'timestamp':row['timestamp'],'track_id':tid,'detection_id':next((j for j,d in enumerate(row['detections']) if iou(b,xyxy(d['bbox']))>.999),None),
                'bbox':box,'previous_association':None if prior is None else {'time':prior['time'],'bbox':prior['track']['bbox'],'track_id':tid},
                'track_state':o['state'],'fall_history':o['fall_candidate'],'recovery_history':o['action']=='dismiss',
                'incident_state':'none (MOT has no incident packets)','association_score':None,'association_reason':'new_track' if prior is None else 'reconstructed legacy gated geometry; no validated continuation token',
                'reference_identity':assigned[i]['identity'] if i in assigned else None}
            if prior:
                p=prior['track'];pb=p['bbox'];dt=row['timestamp']-prior['time'];horizon=min(dt,.25)
                predicted=[p['center'][j]+p['velocity_px_s'][j]*horizon for j in (0,1)]
                distance=math.dist(predicted,tr['center'])/max(pb['h'],pb['w'],box['h'],box['w'])
                overlap=iou(xyxy(pb),b);rec.update(association_score=distance+.3*(1-overlap),gap=dt,overlap=overlap,predicted_distance=distance)
            if i in assigned:
                ref=assigned[i]['identity'];old_owner=owners.get(tid);old_id=by_ref.get(ref)
                if old_owner is not None and old_owner!=ref:
                    event={**rec,'failure':'same_track_id_different_reference_owner','old_reference_identity':old_owner}
                    events.append(event)
                    if len(panels)<8:
                        image=cv2.imread(f'data/sources/mot17-09-audit/{row["frame_index"]*6+1:06d}.jpg');image=cv2.resize(image,(640,360))
                        for rr in refs:
                            a=list(map(round,rr['box']));cv2.rectangle(image,tuple(a[:2]),tuple(a[2:]),(0,255,0),1);cv2.putText(image,f'GT {rr["identity"]}',tuple(a[:2]),cv2.FONT_HERSHEY_SIMPLEX,.4,(0,255,0),1)
                        a=list(map(round,b));cv2.rectangle(image,tuple(a[:2]),tuple(a[2:]),(0,0,255),2)
                        cv2.putText(image,f't={row["timestamp"]:.1f} track {tid}: GT {old_owner} -> {ref}',(5,350),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),1)
                        cv2.imwrite(str(out/f'ownership-{len(panels):02d}.jpg'),image);panels.append(image)
                if old_id is not None and old_id!=tid:events.append({**rec,'failure':'reference_identity_track_id_change','old_track_id':old_id})
                owners[tid]=ref;by_ref[ref]=tid
            previous[tid]={'track':tr,'time':row['timestamp']};all_records.append(rec)
    if panels:
        while len(panels)%2:panels.append(np.zeros_like(panels[0]))
        cv2.imwrite(str(out/'contact.jpg'),np.vstack([np.hstack(panels[i:i+2]) for i in range(0,len(panels),2)]))
    summary={'run_id':run_id,'same_track_reference_owner_changes':sum(e['failure']=='same_track_id_different_reference_owner' for e in events),
        'reference_track_id_changes':sum(e['failure']=='reference_identity_track_id_change' for e in events),
        'actual_incident_transfers':0,'actual_incident_transfer_note':'MOT has no falls/incident packets: zero is vacuous, not proof of incident safety.',
        'method':'One-to-one IoU .5 matches against publisher references; associations reconstructed from logged boxes and velocity. Reference ambiguity can affect owner-change counts. These are visual tracks, not identified people.'}
    (out/'summary.json').write_text(json.dumps(summary,indent=2));(out/'events.json').write_text(json.dumps(events,indent=2));(out/'associations.json').write_text(json.dumps(all_records,indent=2));print(summary)

if __name__=='__main__':diagnose('20261028T144937925673','evaluation/phase1d/before')
