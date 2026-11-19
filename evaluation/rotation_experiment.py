"""Paired detector-only snapshot experiment, not an end-to-end fall benchmark."""
import hashlib
import json
import time
from pathlib import Path
import cv2
import numpy as np
from evaluation.localization_audit import summarize,xyxy
from vision.detection import YoloXDetector
from vision.telemetry import process_memory


def main():
    cv2.setNumThreads(2)
    annotations=json.loads(Path('datasets/phase1c/annotations.json').read_text())['clips']
    clips={c['id']:c for c in json.loads(Path('datasets/phase1c/validation.json').read_text())}
    detector=YoloXDetector();results={};outputs={}
    for all_views in (False,True):
        detector.all_views=all_views;samples=[];times=[];cpu=time.process_time();start=time.perf_counter()
        for clip in annotations:
            source=clips[clip['clip_id']];cap=cv2.VideoCapture(source['path'])
            for f in clip['frames']:
                cap.set(cv2.CAP_PROP_POS_FRAMES,f['frame_index']);ok,frame=cap.read()
                if not ok:raise RuntimeError('snapshot decode failed')
                h,w=frame.shape[:2];sc=min(1,640/max(h,w));frame=cv2.resize(frame,(round(w*sc),round(h*sc)))
                tick=time.perf_counter();found=detector.detect(frame,f['timestamp'],f['frame_index']);times.append((time.perf_counter()-tick)*1000)
                scale=sc/f['scale'];roi=[v*scale for v in clip['main_view_preview_roi']];preds=[]
                for d in found:
                    b=xyxy(d.bbox.model_dump());cx=(b[0]+b[2])/2;cy=(b[1]+b[3])/2
                    if roi[0]<=cx<=roi[2] and roi[1]<=cy<=roi[3]:preds.append({'box':b,'track_id':None})
                refs=[{'box':[v*scale for v in f['box_preview_xyxy']],'identity':clip['clip_id'],'phase':f['phase']}] if f['box_preview_xyxy'] else []
                samples.append({'timestamp':f['timestamp'],'references':refs,'predictions':preds,'clip_id':clip['clip_id'],'frame_index':f['frame_index']})
            cap.release()
            print('all_views',all_views,clip['clip_id'],flush=True)
        elapsed=time.perf_counter()-start;name='all_views' if all_views else 'fallback'
        results[name]={'localization':summarize(samples),'detector_only_fps':len(times)/(sum(times)/1000),'p50_ms':float(np.percentile(times,50)),'p95_ms':float(np.percentile(times,95)),'cpu_one_core_percent_including_decode':100*(time.process_time()-cpu)/elapsed,'memory':process_memory(),'frames':len(times)}
        results[name]['localization']['id_switches']=None
        for value in results[name]['localization']['per_identity'].values():value['id_switches']=None
        outputs[name]=samples
    out=Path('evaluation/phase1c/rotation-experiment.json')
    out.write_text(json.dumps({'scope':'Paired 84 preselected raw snapshots; detector only, no temporal, tracker or evidence evaluation. Same .3 confidence, same model and 640 input; do not compare throughput with full pipeline FPS. No selection on final reserve.', 'model_sha256':hashlib.sha256(Path('data/models/yolox.onnx').read_bytes()).hexdigest(),'results':results,'samples':outputs},indent=2))

if __name__=='__main__':main()
