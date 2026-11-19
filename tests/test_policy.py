import unittest
from vision.policy import disposition
from vision.schemas import Config, Motion, WindowResult
from vision.temporal import TemporalEstimator
from vision.tracking import Track
from test_perception import detection


class PolicyTests(unittest.TestCase):
    def test_old_recovery_cannot_dismiss_current_event(self):
        obs=TemporalEstimator(Config()).update(Track(1,detection(2)),Motion(),'CAM-01')
        obs.action='request_temporal_evidence'
        result=WindowResult(status='ok',observations=[obs],coverage_seconds=1,
            stationary_seconds=0,recovery_observed=True,latency_ms=0,reason='earlier recovery in window')
        self.assertEqual(disposition(obs,result,None,2.5),'investigating')
        obs.action='dismiss'
        self.assertEqual(disposition(obs,result,None,2.5),'dismissed')

    def test_stale_tool_evidence_cannot_dismiss(self):
        obs=TemporalEstimator(Config()).update(Track(1,detection(2)),Motion(),'CAM-01')
        obs.action='dismiss'
        stale=obs.model_copy(update={'timestamp':1})
        result=WindowResult(status='ok',observations=[stale],coverage_seconds=1,
            stationary_seconds=0,recovery_observed=True,latency_ms=0,reason='stale')
        self.assertEqual(disposition(obs,result,None,2.5),'investigating')
