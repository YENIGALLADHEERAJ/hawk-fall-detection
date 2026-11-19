from enum import StrEnum
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator

Nonnegative = Annotated[float, Field(ge=0, allow_inf_nan=False)]
Finite = Annotated[float, Field(allow_inf_nan=False)]
Score = Annotated[float, Field(ge=0, le=1, allow_inf_nan=False)]


class Schema(BaseModel):
    model_config = ConfigDict(extra='forbid', validate_assignment=True)


class Box(Schema):
    x: Nonnegative
    y: Nonnegative
    w: Annotated[float, Field(gt=0, allow_inf_nan=False)]
    h: Annotated[float, Field(gt=0, allow_inf_nan=False)]

    @property
    def center(self):
        return (self.x + self.w / 2, self.y + self.h / 2)


class Detection(Schema):
    bbox: Box
    confidence: Score
    class_name: Literal['person'] = 'person'
    inference_view: Literal['original', 'clockwise', 'counterclockwise'] = 'original'
    timestamp: Nonnegative
    frame_index: Annotated[int, Field(ge=0)]


class State(StrEnum):
    NORMAL = 'NORMAL'
    DESCENT = 'RAPID_DESCENT'
    GROUND = 'GROUND_STATE'
    IMMOBILE = 'IMMOBILE'
    RECOVERY = 'RECOVERY'
    UNKNOWN = 'UNKNOWN'


class Motion(Schema):
    vx_px_s: Finite = 0
    vy_px_s: Finite = 0
    speed_heights_s: Nonnegative = 0
    flow_px_s: Nonnegative | None = None
    difference: Score | None = None
    reliable: bool = False
    quality_reason: str = 'insufficient_history'


class Posture(Schema):
    aspect_ratio: Nonnegative
    horizontal: bool
    upright: bool
    method: Literal['bbox_geometry_proxy'] = 'bbox_geometry_proxy'


class Observation(Schema):
    timestamp: Nonnegative
    frame_index: Annotated[int, Field(ge=0)]
    camera_id: str
    track_id: Annotated[int, Field(gt=0)]
    detection: Detection
    motion: Motion
    posture: Posture
    state: State
    stationary_duration: Nonnegative
    fall_candidate: bool
    evidence_score: Score
    score_semantics: str = 'heuristic evidence strength, not calibrated probability'
    action: Literal['observe', 'request_temporal_evidence', 'request_additional_evidence', 'human_review', 'dismiss']


class IncidentCandidate(Schema):
    incident_id: str
    camera_id: str
    track_ids: list[int]
    timestamp: Nonnegative
    event_type: Literal['potential_fall_immobility'] = 'potential_fall_immobility'
    evidence_score: Score
    recommended_action: str
    evidence: list[Observation]
    status: Literal['investigating', 'human_review', 'dismissed']


class WindowRequest(Schema):
    track_id: Annotated[int, Field(gt=0)]
    start: Nonnegative
    end: Nonnegative

    @model_validator(mode='after')
    def bounds(self):
        if not 0 < self.end - self.start <= 10:
            raise ValueError('window must be >0 and <=10 seconds')
        return self


class WindowResult(Schema):
    status: Literal['ok', 'insufficient_evidence', 'error']
    observations: list[Observation]
    coverage_seconds: Nonnegative
    stationary_seconds: Nonnegative
    recovery_observed: bool
    latency_ms: Nonnegative
    reason: str


class RegionRequest(Schema):
    bbox: Box
    timestamp: Nonnegative
    track_id: Annotated[int, Field(gt=0)]


class RegionResult(Schema):
    status: Literal['ok', 'insufficient_evidence']
    brightness: Nonnegative
    texture_std: Nonnegative
    laplacian_variance: Nonnegative
    latency_ms: Nonnegative
    reason: str


class Config(Schema):
    detector_size: Literal[320, 416, 640] = 640
    rotation_fallback: bool = True
    sample_fps: Annotated[float, Field(ge=1, le=30)] = 5
    max_seconds: Annotated[float, Field(gt=0, le=600)] = 60
    max_width: Annotated[int, Field(ge=160, le=1280)] = 640
    detector_threshold: Score = .3
    horizontal_ratio: Annotated[float, Field(gt=1)] = 1.15
    upright_ratio: Annotated[float, Field(gt=0, lt=1)] = .8
    descent_heights_s: Annotated[float, Field(gt=0)] = .25
    transition_seconds: Annotated[float, Field(gt=0)] = 1.5
    stationary_heights_s: Annotated[float, Field(gt=0)] = .12
    stationary_flow_px_s: Annotated[float, Field(gt=0)] = 6
    immobile_seconds: Annotated[float, Field(gt=0)] = 1.5
    review_seconds: Annotated[float, Field(gt=0)] = 2.5
    max_gap_seconds: Annotated[float, Field(gt=0, le=2)] = .5
    history_seconds: Annotated[float, Field(gt=0, le=10)] = 5
    max_evidence_packets: Annotated[int, Field(ge=1, le=100)] = 10
    threads: Annotated[int, Field(ge=1, le=8)] = 2

    @model_validator(mode='after')
    def temporal_budget(self):
        if not self.immobile_seconds <= self.review_seconds <= self.history_seconds:
            raise ValueError('require immobile_seconds <= review_seconds <= history_seconds')
        return self
