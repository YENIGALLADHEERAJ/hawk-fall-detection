"""Endpoint-supported fall transitions; missing frames never imply immobility."""
from dataclasses import dataclass, field
from vision.schemas import State, Observation
from vision.temporal import posture


@dataclass
class SequenceMemory:
    history: list = field(default_factory=list)
    last: float = -1
    candidate: bool = False
    stationary_since: float | None = None
    state: State = State.NORMAL
    ref_h: float = 0.
    hips: list = field(default_factory=list)   # (timestamp, hip height in reference heights)


class SequenceEstimator:
    def __init__(self, config):
        self.config = config
        self.memory = {}

    def prune(self, active_ids):
        self.memory = {k:v for k,v in self.memory.items() if k in active_ids}

    def update(self, track, motion, camera_id, pose=None):
        c,d=self.config,track.detection
        t,b=d.timestamp,d.bbox
        m=self.memory.setdefault(track.track_id,SequenceMemory())
        if m.last>=0 and t<=m.last: raise ValueError('track timestamps must increase')
        gap=t-m.last if m.last>=0 else None
        if gap is not None and gap>c.track_hold_seconds:
            m=self.memory[track.track_id]=SequenceMemory()
        if gap is not None and gap>c.max_gap_seconds: m.stationary_since=None
        if m.state==State.RECOVERY: m.state=State.NORMAL
        if not m.candidate: m.state=State.NORMAL
        p=posture(b,c)
        m.history=[v for v in m.history if 0<t-v.timestamp<=c.transition_seconds]
        anchors=[v for v in m.history if posture(v.bbox,c).upright]
        anchor=max(anchors,key=lambda v:v.bbox.h) if anchors else None
        signals={'observed_gap_seconds':gap}
        m.ref_h=max(m.ref_h,b.h)
        hip=None
        if pose is not None and pose.hip_ankle_px is not None and m.ref_h>0:
            hip=pose.hip_ankle_px/m.ref_h
        m.hips=[v for v in m.hips if 0<t-v[0]<=c.transition_seconds]
        transition=False;low=False
        reason='no_recent_upright_reference'
        if anchor:
            a=anchor.bbox;dt=t-anchor.timestamp
            drop=(b.center[1]-a.center[1])/a.h
            speed=drop/dt
            height_ratio=b.h/a.h;width_ratio=b.w/a.w
            # Height loss and widening alone also describe an ordinary squat.
            # Require horizontal geometry in addition to net descent, speed and height loss.
            low=height_ratio<=c.maximum_ground_height_ratio and p.horizontal
            signals.update(reference_timestamp=anchor.timestamp,net_drop_heights=drop,
                average_descent_heights_s=speed,height_ratio=height_ratio,width_ratio=width_ratio)
            transition=(low and drop>=c.minimum_drop_heights and speed>=c.minimum_average_descent)
            if (not transition and low and c.compact_collapse_height_ratio is not None
                    and height_ratio<=c.compact_collapse_height_ratio
                    and drop>=0):
                transition=True
                signals['compact_collapse']=True
            reason=('net_descent_and_posture_transition' if transition else
                    'insufficient_net_downward_displacement' if drop<c.minimum_drop_heights else
                    'descent_too_slow' if speed<c.minimum_average_descent else 'no_low_posture_transition')
            if not m.candidate and drop>=c.minimum_drop_heights and not low: m.state=State.DESCENT
        if hip is not None:
            signals['hip_height']=hip
            if c.pose_veto_hip_height is not None and transition and hip>=c.pose_veto_hip_height:
                transition=False;low=False;signals['pose_veto']=1.
                reason='pose_hips_still_high'
            if c.pose_hip_drop is not None and not transition and m.hips:
                ref=max(m.hips,key=lambda v:v[1]);drop=ref[1]-hip;rate=drop/(t-ref[0])
                signals.update(hip_drop=drop,hip_drop_rate=rate)
                if (ref[1]>=c.pose_hip_standing_min and hip<=c.pose_hip_low_max
                        and drop>=c.pose_hip_drop and rate>=c.pose_drop_rate):
                    transition=True;low=True;signals['pose_hip_drop']=1.
                    reason='net_descent_and_posture_transition'
        if hip is not None: m.hips.append((t,hip))
        new_event=transition and not m.candidate
        if new_event:
            m.candidate=True;m.stationary_since=None;m.state=State.GROUND
        action='observe'
        if m.candidate:
            action='request_temporal_evidence'
            # Recovery requires observed upward center movement as well as upright geometry.
            prior=m.history[-1] if m.history else None
            rising=prior is not None and b.center[1]<prior.bbox.center[1]
            if p.upright and rising and not new_event:
                m.candidate=False;m.stationary_since=None;m.state=State.RECOVERY
                action='dismiss';reason='observed_upright_upward_recovery'
                m.history=[]
            elif (p.horizontal or low) and motion.reliable and motion.flow_px_s is not None and motion.speed_heights_s<c.stationary_heights_s and motion.flow_px_s<c.stationary_flow_px_s:
                if m.stationary_since is None:m.stationary_since=t
                m.state=State.GROUND
                if not new_event:reason='observed_ground_low_motion'
            else:
                m.stationary_since=None;m.state=State.GROUND if p.horizontal or low else State.UNKNOWN
                if not new_event:reason='fall_retained_but_stationarity_unproven'
        duration=0 if m.stationary_since is None else t-m.stationary_since
        if duration>=c.immobile_seconds:m.state=State.IMMOBILE;action='request_additional_evidence';reason='continuous_observed_immobility'
        if duration>=c.review_seconds:action='human_review';reason='review_duration_reached_requires_tools'
        if not m.candidate and m.state not in (State.RECOVERY,State.DESCENT):m.state=State.NORMAL
        m.last=t;m.history.append(d)
        score=min(1.,(.55 if m.candidate else 0)+(.35*min(duration/c.review_seconds,1) if m.candidate else 0))
        return Observation(timestamp=t,frame_index=d.frame_index,camera_id=camera_id,track_id=track.track_id,
            detection=d,motion=motion,posture=p,state=m.state,stationary_duration=duration,
            fall_candidate=m.candidate,fall_event_detected=new_event,ground_observed=p.horizontal or low,
            evidence_score=score,action=action,decision_reason=reason,transition_signals=signals)
