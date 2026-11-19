"""Small bounded MOT17 research audit, using publisher frames and ground truth."""
import hashlib
import json
import zipfile
from pathlib import Path
import cv2
import numpy as np
from fetch_footage import RemoteZip


def main():
    folder=Path('data/sources/mot17-09-audit');folder.mkdir(parents=True,exist_ok=True)
    url='https://motchallenge.net/data/MOT17.zip'
    with zipfile.ZipFile(RemoteZip(url,5860214001)) as archive:
        names=archive.namelist()
        candidates=[n for n in names if n.endswith('MOT17-09-FRCNN/gt/gt.txt')]
        if len(candidates)!=1:raise RuntimeError('unexpected archive layout')
        prefix=candidates[0][:-len('gt/gt.txt')]
        print('selected',prefix,flush=True)
        (folder/'gt.txt').write_bytes(archive.read(candidates[0]))
        (folder/'seqinfo.ini').write_bytes(archive.read(prefix+'seqinfo.ini'))
        indices=list(range(1,302,6));mapping=[];writer=None
        output=Path('data/clips/fresh_mot17_09.avi')
        try:
            for i,original in enumerate(indices):
                name=prefix+f'img1/{original:06d}.jpg';info=archive.getinfo(name)
                if info.file_size>3_000_000:raise ValueError('frame too large')
                payload=archive.read(info);(folder/f'{original:06d}.jpg').write_bytes(payload)
                frame=cv2.imdecode(np.frombuffer(payload,np.uint8),cv2.IMREAD_COLOR)
                if frame is None:raise ValueError('frame decode failed')
                if writer is None:
                    h,w=frame.shape[:2];writer=cv2.VideoWriter(str(output),cv2.VideoWriter_fourcc(*'MJPG'),5,(w,h))
                    if not writer.isOpened():raise OSError('writer failed')
                writer.write(frame);mapping.append({'frame_index':i,'original_frame':original,'timestamp':i/5,
                    'member':name,'sha256':hashlib.sha256(payload).hexdigest()})
                if i%10==0:print('frame',original,flush=True)
        finally:
            if writer:writer.release()
    (folder/'mapping.json').write_text(json.dumps(mapping,indent=2))
    manifest=Path('datasets/phase1c/validation.json');clips=json.loads(manifest.read_text())
    entry={'id':'fresh_mot17_09','path':str(output).replace('\\','/'),'source':url,
        'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'event_present':False,'incident_onset':None,
        'split':'fresh_validation','scenario':'multiple pedestrians, crossing and overlap; no staged fall',
        'dataset':'MOT17-09-FRCNN','license':'CC-BY-NC-SA-3.0; local noncommercial research only',
        'derivation':'publisher JPEG frames 1..301 every 6 frames; MJPG at 5 FPS; 10.2 seconds; no detector output used',
        'label_provenance':'pedestrian benchmark; visual non-fall audit required','ground_truth':str(folder/'gt.txt').replace('\\','/')}
    clips=[c for c in clips if c['id']!=entry['id']]+[entry];manifest.write_text(json.dumps(clips,indent=2))
    print('MOT validation clip ready')


if __name__=='__main__':main()
