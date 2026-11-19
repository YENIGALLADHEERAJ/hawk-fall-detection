"""Independent reference matching. Sparse snapshots and MOT subset stay separate."""
import argparse
import json
import math
from collections import defaultdict
from pathlib import Path
import numpy as np


def xyxy(b):
    return [b['x'],b['y'],b['x']+b['w'],b['y']+b['h']]


def iou(a,b):
    inter=max(0,min(a[2],b[2])-max(a[0],b[0]))*max(0,min(a[3],b[3])-max(a[1],b[1]))
    union=(a[2]-a[0])*(a[3]-a[1])+(b[2]-b[0])*(b[3]-b[1])-inter
    return inter/union if union>0 else 0


def match(refs,preds,threshold):
    """Maximum cardinality threshold matching, preferred IoU ordering; not MOTChallenge metrics."""
    owners={}
    def visit(r,seen):
        options=sorted(range(len(preds)),key=lambda p:-iou(refs[r],preds[p]))
        for p in options:
            if p in seen or iou(refs[r],preds[p])<threshold:continue
            seen.add(p)
            if p not in owners or visit(owners[p],seen):owners[p]=r;return True
        return False
    for r in range(len(refs)):visit(r,set())
    return {r:p for p,r in owners.items()}


def summarize(samples):
    total=hit=hit75=unmatched=0;phases=defaultdict(lambda:[0,0]);hist=defaultdict(list);ious=[];centers=[];sizes=[];jitter=[];size_changes=[]
    for sample in samples:
        refs=[r['box'] for r in sample['references']];preds=sample['predictions']
        pairs=match(refs,[p['box'] for p in preds],.5);strict=match(refs,[p['box'] for p in preds],.75)
        total+=len(refs);hit+=len(pairs);hit75+=len(strict)
        unmatched+=len(preds)-len(pairs)
        for r,ref in enumerate(sample['references']):
            phases[ref['phase']][0]+=1;phases[ref['phase']][1]+=r in pairs
            record={'time':sample['timestamp'],'matched':r in pairs,'track_id':None}
            if r in pairs:
                pred=preds[pairs[r]];a=ref['box'];b=pred['box'];h=a[3]-a[1]
                err=[((b[j]+b[j+2])-(a[j]+a[j+2]))/(2*h) for j in (0,1)]
                area=math.log(((b[2]-b[0])*(b[3]-b[1]))/((a[2]-a[0])*(a[3]-a[1])))
                record.update(track_id=pred['track_id'],center_error=err,log_area_error=area)
                ious.append(iou(a,b));centers.append(math.hypot(*err));sizes.append(abs(area))
            hist[ref['identity']].append(record)
    switches=fragments=0;max_gap=0;per_id={}
    for identity,rows in hist.items():
        last_id=None;seen=False;missing=False;miss_times=[];id_switch=frag=0;longest=0
        for n,row in enumerate(rows):
            if not row['matched']:
                missing=True;miss_times.append(row['time']);continue
            if miss_times:longest=max(longest,miss_times[-1]-miss_times[0]);miss_times=[]
            if seen and missing:frag+=1
            if last_id is not None and row['track_id'] is not None and last_id!=row['track_id']:id_switch+=1
            if n and rows[n-1]['matched']:
                prev=rows[n-1]
                jitter.append(math.dist(row['center_error'],prev['center_error']))
                size_changes.append(abs(row['log_area_error']-prev['log_area_error']))
            last_id=row['track_id'];seen=True;missing=False
        if miss_times:longest=max(longest,miss_times[-1]-miss_times[0])
        switches+=id_switch;fragments+=frag;max_gap=max(max_gap,longest)
        per_id[str(identity)]={'reference_samples':len(rows),'missed':sum(not r['matched'] for r in rows),'longest_missed_sample_span_seconds':longest,'id_switches':id_switch,'fragments_after_missing':frag}
    mean=lambda v:float(np.mean(v)) if v else None
    return {'reference_instances':total,'matched_iou50':hit,'matched_iou75':hit75,'recall_iou50':hit/total if total else None,'recall_iou75':hit75/total if total else None,'unmatched_predictions_in_scored_roi':unmatched,'matched_mean_iou':mean(ious),'mean_center_error_heights':mean(centers),'mean_abs_log_area_error':mean(sizes),'mean_reference_relative_center_jitter':mean(jitter),'mean_reference_relative_log_area_change':mean(size_changes),'id_switches':switches,'fragments_after_missing':fragments,'longest_missed_sample_span_seconds':max_gap,'phases':dict(phases),'per_identity':per_id}


def run(result_path):
    results=json.loads(Path(result_path).read_text());root=Path('data/evaluation')/results['run_id']
    annotations=json.loads(Path('datasets/phase1c/annotations.json').read_text())
    reports={};all_samples=[]
    for clip in annotations['clips']:
        records={r['frame_index']:r for r in map(json.loads,(root/clip['clip_id']/'diagnostics.jsonl').read_text().splitlines())}
        samples=[]
        for f in clip['frames']:
            row=records[f['frame_index']];scale=min(1,640/max(f['source_width'],f['source_height']))/f['scale']
            box=f['box_preview_xyxy'];roi=[v*scale for v in clip['main_view_preview_roi']]
            refs=[{'box':[v*scale for v in box],'identity':1,'phase':f['phase']}] if box else []
            preds=[]
            for d in row['detections']:
                b=xyxy(d['bbox']);cx=(b[0]+b[2])/2;cy=(b[1]+b[3])/2
                if not (roi[0]<=cx<=roi[2] and roi[1]<=cy<=roi[3]):continue
                ids=[t['track_id'] for t in row['tracks'] if iou(b,xyxy(t['bbox']))>.999]
                preds.append({'box':b,'track_id':ids[0] if ids else None})
            sample={'timestamp':f['timestamp'],'references':refs,'predictions':preds};samples.append(sample)
            all_samples.append({**sample,'references':[{**r,'identity':clip['clip_id']} for r in refs]})
        reports[clip['clip_id']]=summarize(samples)
    mapping=json.loads(Path('data/sources/mot17-09-audit/mapping.json').read_text())
    gt=np.loadtxt('data/sources/mot17-09-audit/gt.txt',delimiter=',');mot=[];ignored=0
    records=list(map(json.loads,(root/'fresh_mot17_09'/'diagnostics.jsonl').read_text().splitlines()))
    for row in records:
        original=mapping[row['frame_index']]['original_frame'];current=gt[gt[:,0]==original]
        refs=[]
        for v in current:
            if v[6]!=1 or v[7]!=1 or v[8]<=0:ignored+=1;continue
            x,y,w,h=v[2:6]/3
            # Clip annotation to the resized image boundaries, matching detector coordinates.
            b=[max(0,x),max(0,y),min(640,x+w),min(360,y+h)]
            if b[2]<=b[0] or b[3]<=b[1]:continue
            refs.append({'box':b,'identity':int(v[1]),'phase':'visibility_low' if v[8]<.5 else 'visibility_high'})
        preds=[]
        for d in row['detections']:
            b=xyxy(d['bbox']);ids=[t['track_id'] for t in row['tracks'] if iou(b,xyxy(t['bbox']))>.999]
            preds.append({'box':b,'track_id':ids[0] if ids else None})
        mot.append({'timestamp':row['timestamp'],'references':refs,'predictions':preds})
    output={'run_id':results['run_id'],'method':annotations['method'],
        'limitations':'Miss spans are time between first/last missed samples (single miss=0), lower bounds, not continuous video gaps. Sparse boxes cannot establish complete identity continuity. Jitter is consecutive matched reference residual change, no velocity claim. MOT scored at 5Hz, clipped publisher boxes; unmatched MOT predictions include ignored classes and MUST NOT be interpreted as false positives. No official MOTA/IDF1/HOTA.',
        'sparse_combined':summarize(all_samples),'clips':reports,'mot':summarize(mot),'mot_ignored_reference_instances':ignored}
    target=Path(result_path).parent/'localization.json';target.write_text(json.dumps(output,indent=2));print(target)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('results');run(p.parse_args().results)
