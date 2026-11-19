"""Blind-to-model raw-frame annotation sheets in a documented 320x240 coordinate plane."""
import json
from pathlib import Path
import cv2
import numpy as np


def main():
    root=Path('data/phase1c-annotation');root.mkdir(exist_ok=True)
    clips=json.loads(Path('datasets/phase1c/validation.json').read_text());index=[]
    for clip in clips:
        if clip['id']=='fresh_mot17_09':continue
        cap=cv2.VideoCapture(clip['path']);fps=cap.get(cv2.CAP_PROP_FPS);count=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        sampled=[];next_t=0
        for i in range(count):
            t=i/fps
            if t+1e-6>=next_t:sampled.append((i,t));next_t=t+.2
        onset=clip['incident_onset'];duration=count/fps
        targets=[duration*f for f in [.05,.2,.4,.6,.8,.95]] if onset is None else [max(0,onset-.4),onset,onset+.4,onset+.8,duration*.8,duration*.95]
        chosen=sorted({min(sampled,key=lambda v:abs(v[1]-t)) for t in targets})
        tiles=[];entries=[]
        for i,t in chosen:
            cap.set(cv2.CAP_PROP_POS_FRAMES,i);ok,frame=cap.read()
            if not ok:raise RuntimeError('decode failed')
            h,w=frame.shape[:2];scale=min(320/w,240/h);dw,dh=round(w*scale),round(h*scale)
            raw=np.zeros((240,320,3),np.uint8);raw[:dh,:dw]=cv2.resize(frame,(dw,dh))
            cv2.imwrite(str(root/f"{clip['id']}-{i}.jpg"),raw)
            tile=np.zeros((266,320,3),np.uint8);tile[:240]=raw
            for x in range(40,320,40):cv2.line(tile,(x,0),(x,240),(90,90,90),1)
            for y in range(40,240,40):cv2.line(tile,(0,y),(320,y),(90,90,90),1)
            cv2.putText(tile,f"f={i} t={t:.2f}",(4,258),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,255,255),1)
            tiles.append(tile);entries.append({'frame_index':i,'timestamp':t,'preview_width':dw,'preview_height':dh,
                'source_width':w,'source_height':h,'scale':scale})
        while len(tiles)%3:tiles.append(np.zeros_like(tiles[0]))
        cv2.imwrite(str(root/(clip['id']+'-sheet.jpg')),np.vstack([np.hstack(tiles[i:i+3]) for i in range(0,len(tiles),3)]))
        # Coarse full-sequence sheet for independent event/recovery review, no model boxes.
        frames=[]
        for t in np.arange(0,duration,.8):
            cap.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,f=cap.read()
            if not ok:continue
            h,w=f.shape[:2];sc=min(240/w,180/h);a=np.zeros((205,240,3),np.uint8);a[:round(h*sc),:round(w*sc)]=cv2.resize(f,(round(w*sc),round(h*sc)))
            cv2.putText(a,f'{t:.1f}s',(3,199),cv2.FONT_HERSHEY_SIMPLEX,.45,(255,255,255),1);frames.append(a)
        while len(frames)%4:frames.append(np.zeros_like(frames[0]))
        cv2.imwrite(str(root/(clip['id']+'-sequence.jpg')),np.vstack([np.hstack(frames[i:i+4]) for i in range(0,len(frames),4)]))
        cap.release();index.append({'clip_id':clip['id'],'frames':entries})
    (root/'index.json').write_text(json.dumps(index,indent=2))


if __name__=='__main__':main()
