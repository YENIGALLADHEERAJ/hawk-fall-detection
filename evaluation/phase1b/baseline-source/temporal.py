from dataclasses import dataclass
from vision.schemas import State, Posture, Observation


def posture(box, config):
    ratio = box.w/box.h
    return Posture(aspect_ratio=ratio, horizontal=ratio >= config.horizontal_ratio,
                   upright=ratio <= config.upright_ratio)


@dataclass
class Memory:
    state: State = State.NORMAL
    last: float = -1
    upright_at: float = -100
    upright_height: float = 1
    descent_at: float = -100
    stationary_since: float | None = None
    candidate: bool = False


class TemporalEstimator:
    def __init__(self, config):
        self.config = config
        self.memory = {}

    def update(self, track, motion, camera_id):
        c, d = self.config, track.detection
        t, box = d.timestamp, d.bbox
        m = self.memory.setdefault(track.track_id, Memory())
        if m.state==State.RECOVERY: m.state=State.NORMAL
        if m.last >= 0 and t-m.last > c.max_gap_seconds:
            m = self.memory[track.track_id] = Memory(state=State.UNKNOWN)
        p = posture(box,c)
        previous_upright = t-m.upright_at <= c.transition_seconds
        descent = motion.vy_px_s/max(m.upright_height,1) > c.descent_heights_s
        if previous_upright and descent:
            m.descent_at = t
            m.state = State.DESCENT
        if p.horizontal and previous_upright and t-m.descent_at <= c.transition_seconds:
            m.candidate = True
            m.state = State.GROUND
        action = 'observe'
        if m.candidate:
            action = 'request_temporal_evidence'
            if p.upright:
                m.state = State.RECOVERY
                m.candidate = False
                m.stationary_since = None
                action = 'dismiss'
            elif p.horizontal and motion.reliable and motion.speed_heights_s < c.stationary_heights_s and motion.flow_px_s < c.stationary_flow_px_s:
                if m.stationary_since is None: m.stationary_since = t
                m.state = State.GROUND
            else:
                m.stationary_since = None
                m.state = State.GROUND if p.horizontal else State.UNKNOWN
        duration = 0 if m.stationary_since is None else t-m.stationary_since
        if duration >= c.immobile_seconds:
            m.state = State.IMMOBILE
            action = 'request_additional_evidence'
        if duration >= c.review_seconds:
            action = 'human_review'
        if p.upright:
            m.upright_at, m.upright_height = t, box.h
            if not m.candidate and m.state != State.RECOVERY: m.state = State.NORMAL
        elif not m.candidate and t-m.descent_at > c.transition_seconds:
            m.state = State.NORMAL
        m.last = t
        score = min(1., (.35 if m.candidate else 0) + (.2 if p.horizontal and m.candidate else 0)
                    + (.35*min(duration/c.review_seconds,1) if m.candidate else 0))
        return Observation(timestamp=t,frame_index=d.frame_index,camera_id=camera_id,track_id=track.track_id,
            detection=d,motion=motion,posture=p,state=m.state,stationary_duration=duration,
            fall_candidate=m.candidate,evidence_score=score,action=action)

    def prune(self, active_ids):
        self.memory = {k:v for k,v in self.memory.items() if k in active_ids}
