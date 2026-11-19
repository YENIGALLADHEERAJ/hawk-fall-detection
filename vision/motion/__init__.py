import math
import cv2
import numpy as np
from vision.schemas import Motion


def analyze_pair(previous, current, box, dt, velocity, max_gap=.5):
    vx, vy = velocity
    base = dict(vx_px_s=vx, vy_px_s=vy, speed_heights_s=math.hypot(vx,vy)/box.h)
    if previous is None or not 0 < dt <= max_gap or previous.shape != current.shape:
        return Motion(**base)
    x, y = max(0,int(box.x)), max(0,int(box.y))
    x2, y2 = min(current.shape[1],int(box.x+box.w)), min(current.shape[0],int(box.y+box.h))
    if x2-x < 8 or y2-y < 8:
        return Motion(**base, quality_reason='small_roi')
    a, b = previous[y:y2,x:x2], current[y:y2,x:x2]
    a, b = cv2.resize(a,(96,96)), cv2.resize(b,(96,96))
    diff = float(np.mean(cv2.absdiff(a,b))/255)
    light_change = abs(float(a.mean())-float(b.mean()))
    if b.mean() < 15 or light_change > 35 or b.std() < 3:
        return Motion(**base, difference=diff, quality_reason='lighting_or_texture')
    flow = cv2.calcOpticalFlowFarneback(a,b,None,.5,2,15,2,5,1.2,0)
    magnitude = np.linalg.norm(flow,axis=2)
    # 75th percentile detects residual limb motion better than the background median.
    speed = float(np.percentile(magnitude,75)/dt)
    return Motion(**base, flow_px_s=speed, difference=diff, reliable=True, quality_reason='ok')
