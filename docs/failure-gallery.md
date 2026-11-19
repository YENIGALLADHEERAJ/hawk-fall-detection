# Phase 1 failure gallery

The original examples below document the Phase 1 baseline. Phase 1B now detects
both held-out falls with preserved identity; see the [current ablation report](../evaluation/holdout/report.md).
The set has been reused for development and does not establish unseen accuracy.

## Phase 1B rejected detector experiment

Lowering the continuation floor from 0.30 to 0.15 reduces zero-detection frames,
but at 2.004 seconds of Subject 3 Fall/16 the detector produces a 482x203-pixel
box spanning much of the room (confidence 0.276). The apparent earlier fall alert
depends on this poor localization. It is retained in the measurements and rejected
as the default. More detections do not necessarily mean better person coverage.

![Low-confidence localization failure](../data/evaluation/20261027T154703686849/holdout_s3_Fall_16/contact.jpg)

## Phase 1B compact-posture regression

An initial optional low-posture branch confused a squat (`clip_06`) and ordinary
chair sitting (`gmdcsa_ADL_13`) with falls. Their bounding boxes shrank and widened
without becoming horizontal. That branch was removed; net downward motion, speed,
height loss and horizontal geometry must now agree. Real-inference regression tests
cover both clips. This still leaves foreshortened falls as a known weakness.

![Initial false candidate while sitting](../data/evaluation/20261027T155139115544/gmdcsa_ADL_13/contact.jpg)

These are development examples, not a clinical or population-level assessment.
Footage attribution is in [datasets/README](../datasets/README.md).

## Seated/foreshortened fall missed

`clip_05` contains a seated fall toward the camera. The bounding box does not become
wide enough to satisfy the geometry rule. A person is tracked but no candidate is
created. This is a false negative, not a successful uncertainty rejection.

![Seated fall contact sheet](../data/clip_05.jpg)

## Prone detection lost without alternate views

On `gmdcsa_Fall_11`, original-view YOLOX stops detecting the prone person. The
clockwise/counterclockwise fallback recovers detections and preserves one track,
but substantially increases processing latency. Same-camera rotations provide
additional computation, not independent confirmation from another camera.

![Prone detection and motion evidence](../data/runs/proof-rotation/incidents/incident-0001-000060/annotated.jpg)

## Intentional lying down

The immediate horizontal-box baseline can alert on intentional bed use. The temporal
policy rejects several such examples, but this does not establish robustness across
camera angles, fast intentional lying down, or slow real falls.

![Intentional bed use](../data/gmdcsa_ADL_01.jpg)

## Insufficient clip duration

Ursul clips are approximately 1.9 seconds. Some show a transition but no long enough
post-fall observation. They cannot support prolonged-immobility or review claims.
No frames were frozen, looped or synthetically extended to fill the missing time.

## Unresolved coverage

Natural multi-person interactions and real fall-followed-by-recovery clips remain
unvalidated. Recovery and multi-person association have unit tests, which do not
replace footage tests. Camera shake may contaminate ROI flow. Dedicated poor-light
footage and physical-camera disconnect/reconnect tests remain open. Capture transport
reconnect and timeout tests now pass using fixtures. Low sampling rates
beyond the configured continuity gap intentionally lose temporal evidence.

## Held-out fall loses temporal identity

`holdout_s2_Fall_13` reaches RAPID_DESCENT on track 1 at 3.21 seconds, then the next
observed horizontal box belongs to a new track at 3.81 seconds. The 0.60-second gap
exceeds the configured 0.50-second continuity limit. Later prone detections cannot
inherit the earlier descent, and no candidate is created. Eight distinct track IDs
appear in the clip; this count includes possible extra detections and is not an
identity-switch metric. The immediate baseline alerts, including before the labeled
fall onset. Clip-level baseline recall therefore does not establish correct event
timing. No thresholds were adjusted after seeing this failure.

`holdout_s3_Fall_16` also produces no candidate. Track 1's last observation is at
1.80 seconds; the next observed person is horizontal at 3.01 seconds as track 3.
The transition is unobserved. Five distinct IDs and only 17 detections across 31
sampled frames indicate weak detection/association continuity, not successful
rejection of a non-event. Both held-out falls are counted as false negatives.

![Held-out recordings, four sampled frames per clip](../data/holdout-contact.jpg)
