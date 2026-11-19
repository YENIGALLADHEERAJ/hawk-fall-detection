import json
from pathlib import Path
import cv2


def annotate(frame, observations, trajectories=None):
    out = frame.copy()
    cv2.putText(out,'HAWK | potential safety events | geometry proxy',(10,20),cv2.FONT_HERSHEY_SIMPLEX,.45,(255,255,255),1)
    for o in observations:
        b = o.detection.bbox
        color = (0,165,255) if o.fall_candidate else (100,220,80)
        cv2.rectangle(out,(int(b.x),int(b.y)),(int(b.x+b.w),int(b.y+b.h)),color,2)
        label=f'#{o.track_id} {o.state} score={o.evidence_score:.2f} still={o.stationary_duration:.1f}s'
        cv2.putText(out,label,(max(0,int(b.x)),max(40,int(b.y)-18)),cv2.FONT_HERSHEY_SIMPLEX,.4,color,1)
        cv2.putText(out,o.action,(max(0,int(b.x)),max(55,int(b.y)-4)),cv2.FONT_HERSHEY_SIMPLEX,.38,color,1)
        if trajectories:
            points=trajectories.get(o.track_id,[])
            for a,bp in zip(points,points[1:]): cv2.line(out,a,bp,color,1)
    return out


def save_packet(root, candidate, frame, annotated, window, fps):
    # Incident IDs are generated internally; never accept a caller-supplied path.
    target = Path(root)/candidate.incident_id
    target.mkdir(parents=True,exist_ok=True)
    for name,img in [('frame.jpg',frame),('annotated.jpg',annotated)]:
        if not cv2.imwrite(str(target/name),img): raise OSError('snapshot encode failed')
    (target/'evidence.json').write_text(candidate.model_dump_json(indent=2),encoding='utf-8')
    metadata={'frames':len(window),'sample_fps':fps,'timestamps':[t for t,_ in window],
              'privacy':'local raw evidence; no identity inference; delete after review',
              'window':'bounded observed pre-trigger frames only'}
    (target/'metadata.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
    if window:
        h,w=frame.shape[:2]
        writer=cv2.VideoWriter(str(target/'window.avi'),cv2.VideoWriter_fourcc(*'MJPG'),fps,(w,h))
        if not writer.isOpened(): raise OSError('evidence video writer unavailable')
        try:
            for _,f in window: writer.write(f)
        finally: writer.release()
    return str(target)
