# HAWK Phase 1 perception contract

Status: local research interface, not approved for Phase 2. `vision/schemas.py` is authoritative; exported schemas are in `docs/schemas/`. Observations are validated Pydantic records with unknown fields forbidden and finite numerical values. No agent or cloud consumer is connected.

## Transport and identity

`observations.jsonl` contains one `Observation` per actually detected, associated person per sampled frame. An empty sample emits no observation; inspect `diagnostics.jsonl` and `trace.json` for missing evidence and source failures. Silence never means normal or safe. Retained tracks are internal hypotheses, not observed people. No predicted box is emitted as a detection.

The external identity key must be **run directory + camera_id + track_id**. IDs are positive local integers, not biometric identities. `CAM-01` is currently a fixed label for this single-source executable, not a globally unique camera identifier. Incident IDs likewise require the run namespace. Association is appearance-independent box/velocity matching and can fragment or switch identities during overlap. There is no tracking-confidence probability. Detector confidence must not be substituted for it.

## Observation fields

| Field | Meaning |
|---|---|
| `timestamp`, `frame_index` | Nonnegative source-relative seconds and zero-based source frame index. File time is frame index / reported FPS; variable-frame-rate presentation timestamps are not decoded. These are not wall-clock UTC. |
| `camera_id`, `track_id` | Local source label and association ID, scoped as above. |
| `detection` | `bbox`, `confidence`, `class_name=person`, `inference_view`, source timestamp/index. |
| `detection.bbox` | Positive width/height rectangle `{x,y,w,h}` in resized processing-frame pixels. Origin top left, x right, y down. Longest side capped at `max_width` (default 640), aspect ratio retained with rounded dimensions. Not source-resolution or normalized coordinates. |
| `detection.inference_view` | `original`, `clockwise`, or `counterclockwise`; rotation results mapped back to the processing frame. Rotation fallback only runs when earlier views produce no person, so a standing companion can suppress prone-person fallback. |
| `motion.vx_px_s`, `vy_px_s` | Box-center displacement per source second from association; positive y means downward. Sensitive to box changes and ID errors. |
| `motion.speed_heights_s` | Center speed normalized by box height. |
| `motion.flow_px_s`, `difference` | Dense flow magnitude in a normalized ROI and normalized frame difference; nullable if unavailable. Flow is not full-frame physical velocity. |
| `motion.reliable`, `quality_reason` | Measurement eligibility flag and explanation, not a probability. Track gaps, low texture and insufficient history can invalidate motion. |
| `posture` | Aspect ratio, horizontal/upright flags, `method=bbox_geometry_proxy`; not joints or true physical posture. |
| `state` | `NORMAL`, `RAPID_DESCENT`, `GROUND_STATE`, `IMMOBILE`, `RECOVERY`, `UNKNOWN`. `NORMAL` means no supported candidate in the current history, not proof of safety. Ground can be a bed or mat; no floor model exists. |
| `fall_event_detected` | A new supported transition on this observation only. |
| `fall_candidate` | Latched fall hypothesis until observed recovery or history expiry; distinct from a new event. |
| `ground_observed` | Low/horizontal box proxy, not proof of a fall. |
| `stationary_duration` | Continuous supported low-motion duration in seconds. Missing/unreliable motion resets it; source time, not processing wall time. |
| `decision_reason`, `transition_signals` | Rule explanation and named finite numbers/null. Current keys: observed gap, reference timestamp, net drop in reference heights, average descent heights/s, height ratio, width ratio. Keys may be absent when no anchor exists. |
| `evidence_score`, `score_semantics` | Heuristic evidence strength, **not calibrated probability**, diagnosis, injury severity, or tracking confidence. Current candidate base .55 plus up to .35 for supported immobility. |
| `action` | `observe`, `request_temporal_evidence`, `request_additional_evidence`, `human_review`, `dismiss`; requests to the local evidence policy, not autonomous emergency actions. |

## Temporal and evidence semantics

Selected configuration uses a recent upright reference (1.5 s), net descent and horizontal height loss to detect a fall. Prolonged immobility is not required for that event. A person initially lying down has no upright transition and does not automatically become a fall. Intentional rapid lying can nevertheless resemble a fall. Recovery requires upright geometry plus observed upward center motion; box jitter can undermine this inference.

Tracks are retained for at most 1.5 s, with motion prediction capped at .25 s for association only. A gap over .5 s resets the stationary clock. Expiry destroys temporal history. Reconnection clears tracks, temporal memory and tool history. The bounded evidence history is 300 observations globally across tracks and at most 10 s, so crowded scenes can shorten available per-person history. The frame ring is bounded by configured history/sample rate. Packet creation is capped (default 10 per run); candidate counts derived from packets are therefore not an unlimited event counter.

`IncidentCandidate` contains incident/camera IDs, owning track IDs, timestamp, event type (`potential_fall`, with legacy `potential_fall_immobility` accepted), evidence score, recommended action, structured observation evidence and status (`investigating`, `human_review`, `dismissed`). Review requires supporting temporal/region tool results. Recovery dismissal must refer to the current matching track and timestamp; historical recovery alone is insufficient. A missing or expired person is not automatically dismissed.

`WindowRequest` requires an existing track and a positive window <=10 s; future windows are rejected. `WindowResult` reports `ok`, `insufficient_evidence`, or `error`, actual observations/coverage/stationarity, recovery flag, reason and tool latency. `RegionRequest` identifies track, timestamp and box; `RegionResult` reports brightness/texture/sharpness evidence and `ok` or `insufficient_evidence`. Region quality is not person localization verification.

## Provenance and failures

Keep each observation stream with `metrics.json` (source SHA-256 for files, config, OpenCV version, source FPS, timings, exit reason), `diagnostics.jsonl` (including empty samples), `trace.json` (tools and state changes), and incident evidence. Evaluation manifests provide source URLs, licensing and labels. Current runtime metrics do not embed model/code hashes: reproducible evaluations must additionally retain those hashes and the exact source revision. An observation copied without its run metadata loses provenance and must not be consumed as standalone authoritative evidence.

File EOF, decode errors, duration limits, camera timeout/reconnect exhaustion and exceptions are not negative detections. Live timestamps and source statuses are defined by `vision/source.py`; physical-camera behavior remains unvalidated. Source loss must surface as unknown/unavailable, not as a zero-confidence normal observation. The system has no calibrated uncertainty distribution, guaranteed identity ownership, floor-plane localization, or medical severity model. A future consumer must preserve these limitations and must not convert scores to probabilities or missing records to safe states.

## Profiling

Stage profiles are sampled-frame wall times: preprocessing, detector (including tensor preparation and rotations), tracking, motion, temporal/logging, evidence tools/packet I/O, and visualization/debug-video writing. Decode/startup/final serialization are outside these buckets but included as applicable in end-to-end elapsed time. CPU percent is relative to one core and may exceed 100%. Process memory includes runtime/model allocations. Source sampling at 5 Hz does not imply 5 FPS processing throughput.
