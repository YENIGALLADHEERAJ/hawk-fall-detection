"""Deterministic incident disposition from current, validated tool evidence."""
def disposition(observation, temporal, region, review_seconds):
    if not temporal.observations:
        return 'investigating'
    latest = temporal.observations[-1]
    if latest.track_id != observation.track_id or latest.timestamp != observation.timestamp:
        return 'investigating'
    # A recovery in a previous incident's history must never dismiss a new fall.
    if observation.action == 'dismiss' and latest.action == 'dismiss':
        return 'dismissed'
    if (observation.action == 'human_review' and temporal.status == 'ok'
            and temporal.stationary_seconds >= review_seconds
            and region is not None and region.status == 'ok'):
        return 'human_review'
    return 'investigating'
