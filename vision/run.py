import argparse
import json
from vision.pipeline import run_video
from vision.schemas import Config


def main():
    p=argparse.ArgumentParser(description='HAWK real OpenCV 5 perception')
    p.add_argument('video',nargs='?'); p.add_argument('--output',required=True)
    p.add_argument('--camera',type=int,help='Explicit local device index; opens the camera only when supplied')
    p.add_argument('--model',default='data/models/yolox.onnx')
    p.add_argument('--fps',type=float,default=5)
    p.add_argument('--max-seconds',type=float,default=60)
    p.add_argument('--view',action='store_true')
    p.add_argument('--variant',choices=['baseline','tracking','temporal','combined'],default='combined')
    p.add_argument('--continuation-threshold',type=float,default=None,
                   help='Experimental low-score association floor; new tracks still use detector threshold')
    p.add_argument('--backend',choices=['opencv','directml'],default='opencv',help='Detector execution: OpenCV CPU or ONNX Runtime DirectML GPU')
    p.add_argument('--device-id',type=int,default=0,help='DirectML adapter index (machine specific)')
    p.add_argument('--threads',type=int,default=2)
    p.add_argument('--identity-tracking',action='store_true',help='Experimental colour-histogram appearance cue in association')
    p.add_argument('--optimal-assignment',action='store_true',help='Experimental global assignment (regressed on unseen footage)')
    p.add_argument('--compact-collapse-ratio',type=float,default=None,help='Experimental: accept horizontal collapse-in-place down to this height ratio (e.g. 0.6)')
    p.add_argument('--pose-evidence',action='store_true',help='Experimental: compute RTMPose keypoint evidence (logged; rules below are separate)')
    p.add_argument('--pose-hip-drop',type=float,default=None,help='Experimental: accept a fall when hip height drops by this much (e.g. 0.2)')
    p.add_argument('--pose-veto-hip-height',type=float,default=None,help='Experimental: veto a box-based fall while hip height is at least this (e.g. 0.28)')
    a=p.parse_args()
    if (a.video is None)==(a.camera is None): p.error('provide a video file OR --camera INDEX')
    config=Config(sample_fps=a.fps,max_seconds=a.max_seconds,continuation_threshold=a.continuation_threshold,
                  improved_tracking=a.variant in ('tracking','combined'),
                  improved_temporal=a.variant in ('temporal','combined'),
                  identity_tracking=a.identity_tracking,optimal_assignment=a.optimal_assignment,compact_collapse_height_ratio=a.compact_collapse_ratio,pose_evidence=a.pose_evidence or a.pose_hip_drop is not None or a.pose_veto_hip_height is not None,pose_hip_drop=a.pose_hip_drop,pose_veto_hip_height=a.pose_veto_hip_height,detector_backend=a.backend,detector_device=a.device_id,threads=a.threads)
    result=run_video(a.camera if a.camera is not None else a.video,a.output,config,a.model,a.view)
    print(json.dumps({k:v for k,v in result.items() if k!='incidents'},indent=2))


if __name__=='__main__': main()
