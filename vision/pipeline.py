import hashlib
import json
import time
from collections import deque
from pathlib import Path
import cv2
import numpy as np
from vision.detection import YoloXDetector
from vision.tracking import appearance_feature
from vision.tracking import PersonTracker
from vision.motion import analyze_pair
from vision.temporal import TemporalEstimator
from vision.schemas import Config, IncidentCandidate, WindowRequest, RegionRequest
from vision.tools import EvidenceTools
from vision.evidence import annotate, save_packet
from vision.telemetry import process_memory
from vision.source import VideoSource
from vision.policy import disposition
from vision.diagnostics import sample_record
from vision.temporal_v2 import SequenceEstimator
from vision.pose import PoseEstimator


def run_video(source, output, config=None, model='data/models/yolox.onnx', viewer=False):
    config = config or Config()
    output=Path(output)
    output.mkdir(parents=True,exist_ok=True)
    if (output/'observations.jsonl').exists(): raise FileExistsError('choose a fresh output directory')
    cv2.setNumThreads(config.threads)
    detector=YoloXDetector(model,config.continuation_threshold if config.continuation_threshold is not None else config.detector_threshold,
                          config.detector_size,config.rotation_fallback,config.rotation_all_views,
                          config.detector_backend,config.detector_device,config.threads)
    tracker=PersonTracker(config.track_hold_seconds if config.improved_tracking else config.max_gap_seconds,
                          config.history_seconds,config.improved_tracking,config.prediction_horizon_seconds,
                          config.detector_threshold if config.continuation_threshold is not None else 0,
                          appearance_weight=config.appearance_weight if config.identity_tracking else 0.,
                          optimal=config.optimal_assignment and config.improved_tracking)
    temporal=SequenceEstimator(config) if config.improved_temporal else TemporalEstimator(config)
    pose_estimator=None
    if config.pose_evidence:
        if not config.improved_temporal: raise ValueError('pose evidence needs the improved temporal estimator')
        pose_estimator=PoseEstimator(config.pose_model,config.detector_backend,config.detector_device)
    tools=EvidenceTools()
    cap=VideoSource(source)
    source_fps=cap.fps
    ring=deque(maxlen=int(config.sample_fps*config.history_seconds)+1)
    previous=None; last_t=None; next_t=0.; frame_index=0; writer=None
    timings=[]; detections_count=0; candidate_times=[]; review_times=[]; baseline_times=[]
    stage_times={k:[] for k in ('preprocessing','detector','tracking','motion','pose','temporal_and_logging','evidence','visualization')}
    baseline_active=set(); packets={}; completed=[]; events=[]; all_ids=set(); last_actions={}; packet_actions={}; last_tool={}
    start=time.perf_counter(); cpu=time.process_time(); exit_reason='eof'; last_processed=0
    with (output/'observations.jsonl').open('w',encoding='utf-8') as log, (output/'diagnostics.jsonl').open('w',encoding='utf-8') as diagnostic_log:
        try:
            while cap.elapsed < config.max_seconds:
                sample=cap.read()
                if sample.status.startswith('reconnecting:'):
                    events.append({'timestamp':sample.timestamp,'action':sample.status,'state':'UNKNOWN'})
                    tracker.tracks.clear(); temporal.memory.clear(); tools.history.clear(); ring.clear()
                    previous=None; last_t=None
                    continue
                if sample.status!='frame':
                    exit_reason=sample.status
                    events.append({'timestamp':sample.timestamp,'action':sample.status,'state':'UNKNOWN'})
                    break
                frame,t,index=sample.frame,sample.timestamp,sample.index
                frame_index=index+1
                if t+1e-6 < next_t: continue
                next_t=t+1/config.sample_fps
                tick=time.perf_counter()
                stages={k:0. for k in stage_times}
                if frame is None or frame.ndim!=3: exit_reason='corrupt_frame'; break
                h,w=frame.shape[:2]
                if max(h,w)>config.max_width:
                    scale=config.max_width/max(h,w)
                    frame=cv2.resize(frame,(max(1,round(w*scale)),max(1,round(h*scale))))
                gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                stages['preprocessing']=time.perf_counter()-tick
                stage_start=time.perf_counter()
                found=detector.detect(frame,t,index)
                stages['detector']=time.perf_counter()-stage_start
                detections_count+=len(found)
                stage_start=time.perf_counter()
                tracks=tracker.update(found,t,[appearance_feature(frame,d.bbox) for d in found] if config.identity_tracking else None)
                stages['tracking']=time.perf_counter()-stage_start
                if not tracks:
                    events.append({'timestamp':t,'action':'missing_visual_evidence','state':'UNKNOWN'})
                temporal.prune(tracker.tracks.keys())
                observations=[]
                for tr in tracks:
                    all_ids.add(tr.track_id)
                    stage_start=time.perf_counter()
                    motion=analyze_pair(previous,gray,tr.detection.bbox,t-last_t if last_t is not None else 0,
                                        tr.velocity,config.max_gap_seconds)
                    stages['motion']+=time.perf_counter()-stage_start
                    stage_start=time.perf_counter()
                    # Missing track observations must not count toward stationary duration.
                    if len(tr.history)<2 or (last_t is not None and tr.history[-2].timestamp != last_t):
                        motion.reliable=False; motion.quality_reason='track_gap'
                        if tr.track_id in temporal.memory:
                            temporal.memory[tr.track_id].stationary_since=None
                    if tr.detection.confidence<config.detector_threshold:
                        motion.reliable=False;motion.quality_reason='low_detection_confidence'
                    pose=None
                    if pose_estimator is not None:
                        pose_start=time.perf_counter()
                        pose=pose_estimator.estimate(frame,tr.detection.bbox)
                        stages['pose']+=time.perf_counter()-pose_start
                    obs=temporal.update(tr,motion,'CAM-01',pose) if pose_estimator is not None else temporal.update(tr,motion,'CAM-01')
                    if pose is not None: obs.pose=pose
                    tools.add(obs); observations.append(obs)
                    log.write(obs.model_dump_json()+'\n')
                    if obs.posture.horizontal:
                        if tr.track_id not in baseline_active: baseline_times.append(t)
                        baseline_active.add(tr.track_id)
                    else: baseline_active.discard(tr.track_id)
                    if obs.action != last_actions.get(tr.track_id):
                        events.append({'timestamp':t,'track_id':tr.track_id,'state':obs.state.value,
                                       'action':obs.action,'score':obs.evidence_score,
                                       'reason':obs.decision_reason,'transition_signals':obs.transition_signals})
                    last_actions[tr.track_id]=obs.action
                    stages['temporal_and_logging']+=time.perf_counter()-stage_start
                stage_start=time.perf_counter()
                ring.append((t,frame.copy()))
                while ring and t-ring[0][0]>config.history_seconds: ring.popleft()
                trajectories={tr.track_id:[tuple(map(int,d.bbox.center)) for d in tr.history] for tr in tracks}
                annotated=annotate(frame,observations,trajectories)
                stages['visualization']+=time.perf_counter()-stage_start
                stage_start=time.perf_counter()
                for obs in observations:
                    if obs.action=='observe': continue
                    changed = obs.action != packet_actions.get(obs.track_id)
                    if not changed and t-last_tool.get(obs.track_id,-100) < .5: continue
                    last_tool[obs.track_id]=t
                    # Execute a genuine history analysis before updating investigation status.
                    result=tools.analyze_temporal_window(WindowRequest(track_id=obs.track_id,
                        start=max(0,t-(config.review_seconds if obs.action=='human_review' else config.history_seconds)),end=max(t,.001)))
                    region=None
                    if obs.action in ('request_additional_evidence','human_review'):
                        region=tools.inspect_region(RegionRequest(bbox=obs.detection.bbox,timestamp=t,track_id=obs.track_id),frame)
                    key=obs.track_id
                    if key in packets and packets[key].status=='dismissed' and obs.fall_candidate:
                        completed.append(packets.pop(key))
                    if key not in packets and obs.fall_candidate and len(packets)+len(completed)<config.max_evidence_packets:
                        ident=f'incident-{key:04d}-{index:06d}'
                        packets[key]=IncidentCandidate(incident_id=ident,camera_id=obs.camera_id,
                            track_ids=[key],timestamp=t,evidence_score=obs.evidence_score,
                            recommended_action=obs.action,evidence=result.observations,status='investigating')
                        candidate_times.append(t)
                    if key in packets:
                        packet=packets[key]
                        old=packet.status
                        packet.evidence=result.observations
                        packet.evidence_score=obs.evidence_score
                        packet.recommended_action=obs.action
                        decision=disposition(obs,result,region,config.review_seconds)
                        if decision!='investigating': packet.status=decision
                        if packet.status=='human_review' and old!='human_review': review_times.append(t)
                        # Overwrite bounded packet only on meaningful actions; no unbounded video archive.
                        if old!=packet.status or changed:
                            snapshot_start=time.perf_counter()
                            path=save_packet(output/'incidents',packet,frame,annotated,list(ring),config.sample_fps)
                            tools.calls.append({'tool':'generate_evidence_snapshot','input':{'incident_id':packet.incident_id},
                                'output':{'path':path,'latency_ms':(time.perf_counter()-snapshot_start)*1000,'status':'ok'}})
                    packet_actions[obs.track_id]=obs.action
                stages['evidence']=time.perf_counter()-stage_start
                stage_start=time.perf_counter()
                if writer is None:
                    h,w=frame.shape[:2]
                    writer=cv2.VideoWriter(str(output/'debug.avi'),cv2.VideoWriter_fourcc(*'MJPG'),config.sample_fps,(w,h))
                    if not writer.isOpened(): raise OSError('debug writer unavailable')
                writer.write(annotated)
                stages['visualization']+=time.perf_counter()-stage_start
                for name,value in stages.items(): stage_times[name].append(value*1000)
                previous,last_t=gray,t
                measured_ms=(time.perf_counter()-tick)*1000
                diagnostic_log.write(json.dumps(sample_record(index,t,found,tracks,observations,measured_ms))+'\n')
                timings.append((time.perf_counter()-tick)*1000); last_processed=t
                if viewer:
                    cv2.imshow('HAWK debug - Q quits',annotated)
                    if cv2.waitKey(1)&255==ord('q'): exit_reason='user_stop'; break
            else: exit_reason='duration_limit'
        finally:
            cap.release()
            if writer: writer.release()
            if viewer: cv2.destroyAllWindows()
    elapsed=time.perf_counter()-start
    result={'source':str(source),'source_kind':'camera' if cap.live else 'file',
        'source_sha256':None if cap.live else hashlib.sha256(Path(source).read_bytes()).hexdigest(),
        'source_reconnect_attempts':cap.attempts,
        'config':config.model_dump(),'opencv':cv2.__version__,'source_fps':source_fps,
        'sampled_frames':len(timings),'observed_seconds':last_processed,'detections':detections_count,
        'distinct_track_ids':len(all_ids),'candidate_times':candidate_times,'human_review_times':review_times,
        'baseline_alert_times':baseline_times,'exit_reason':exit_reason,'wall_seconds':elapsed,
        'processing_fps':len(timings)/elapsed if elapsed else None,
        'cpu_one_core_percent':100*(time.process_time()-cpu)/elapsed,
        'p50_ms':float(np.percentile(timings,50)) if timings else None,
        'p95_ms':float(np.percentile(timings,95)) if timings else None,
        'tool_calls':len(tools.calls),'incidents':[p.model_dump(mode='json') for p in completed+list(packets.values())],
        'frame_latency_ms':timings,
        'stage_profile_ms':{name:{'total':sum(values),'mean':float(np.mean(values)) if values else None,
            'p50':float(np.percentile(values,50)) if values else None,
            'p95':float(np.percentile(values,95)) if values else None} for name,values in stage_times.items()},
        'profile_semantics':'Wall-clock stage timings per sampled frame, summed across people. Detector includes its tensor preprocessing and rotation. Excludes decoding, startup and final serialization; evidence includes tools and packet I/O; visualization includes ring copy and debug video.',
        'dismissed_candidates':sum(p.status=='dismissed' for p in completed+list(packets.values()))}
    result['memory'] = process_memory()
    (output/'metrics.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    (output/'trace.json').write_text(json.dumps({'events':events,'tools':tools.calls},indent=2),encoding='utf-8')
    return result
