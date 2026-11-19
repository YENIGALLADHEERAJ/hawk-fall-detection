"""Counterfactual association only, using recorded real detections; no FPS claim."""
import json
from pathlib import Path
import numpy as np
from evaluation.localization_audit import summarize,xyxy
from vision.tracking import PersonTracker
from vision.schemas import Detection


def main():
    result=json.loads(Path('evaluation/phase1c/baseline/results.json').read_text())
    path=Path('data/evaluation')/result['run_id']/'fresh_mot17_09'/'diagnostics.jsonl'
    rows=[json.loads(s) for s in path.read_text().splitlines()]
    gt=np.loadtxt('data/sources/mot17-09-audit/gt.txt',delimiter=',')
    mapping=json.loads(Path('data/sources/mot17-09-audit/mapping.json').read_text());output={}
    for guard in (False,True):
        tracker=PersonTracker(1.5,improved=True,reject_short_ambiguity=guard);samples=[]
        for row in rows:
            tracks=tracker.update([Detection.model_validate(d) for d in row['detections']],row['timestamp'])
            if not guard:
                assert [t.track_id for t in tracks]==[t['track_id'] for t in row['tracks']]
            refs=[]
            for v in gt[gt[:,0]==mapping[row['frame_index']]['original_frame']]:
                if v[6]!=1 or v[7]!=1 or v[8]<=0:continue
                x,y,w,h=v[2:6]/3;b=[max(0,x),max(0,y),min(640,x+w),min(360,y+h)]
                if b[2]<=b[0] or b[3]<=b[1]:continue
                refs.append({'box':b,'identity':int(v[1]),'phase':'visibility_low' if v[8]<.5 else 'visibility_high'})
            samples.append({'timestamp':row['timestamp'],'references':refs,'predictions':[{'box':xyxy(t.detection.bbox.model_dump()),'track_id':t.track_id} for t in tracks]})
        output['short_gap_guard' if guard else 'baseline']=summarize(samples)
    Path('evaluation/phase1c/association-experiment.json').write_text(json.dumps({'scope':'Counterfactual tracking on recorded real MOT detections. Baseline ID sequence asserted identical. No new DNN, motion, fall or throughput benchmark.', 'run_id':result['run_id'],'results':output},indent=2))

if __name__=='__main__':main()
