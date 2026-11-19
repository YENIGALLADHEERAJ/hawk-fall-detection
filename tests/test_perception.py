import unittest
import numpy as np
from pydantic import ValidationError
from vision.schemas import Box, Detection, Config, Motion, State, WindowRequest, RegionRequest
from vision.tracking import PersonTracker, Track, iou
from vision.temporal import TemporalEstimator, posture
from vision.motion import analyze_pair
from vision.tools import EvidenceTools


def detection(t,x=30,y=20,w=40,h=100):
    return Detection(bbox=Box(x=x,y=y,w=w,h=h),confidence=.9,timestamp=t,frame_index=round(t*10))


class PerceptionTests(unittest.TestCase):
    def test_schema_rejects_invalid(self):
        for kwargs in ({'x':-1,'y':0,'w':1,'h':2},{'x':0,'y':0,'w':0,'h':2},{'x':0,'y':0,'w':float('nan'),'h':2}):
            with self.assertRaises(ValidationError): Box(**kwargs)
        with self.assertRaises(ValidationError): Config(unknown=3)

    def test_geometry(self):
        b=detection(0).bbox
        self.assertEqual(iou(b,b),1)
        self.assertTrue(posture(b,Config()).upright)
        self.assertFalse(posture(b,Config()).horizontal)

    def test_tracker_velocity_and_expiry(self):
        tracker=PersonTracker()
        a=tracker.update([detection(0)],0)[0]
        b=tracker.update([detection(.1,x=32)],.1)[0]
        self.assertEqual(a.track_id,b.track_id)
        self.assertAlmostEqual(b.velocity[0],20)
        self.assertEqual(tracker.update([],.2),[])
        c=tracker.update([detection(1)],1)[0]
        self.assertNotEqual(c.track_id,b.track_id)
        with self.assertRaises(ValueError): tracker.update([],1)

    def test_multiple_people_one_to_one(self):
        tracker=PersonTracker()
        tracker.update([detection(0,x=0),detection(0,x=200)],0)
        result=tracker.update([detection(.1,x=202),detection(.1,x=2)],.1)
        self.assertEqual(len({t.track_id for t in result}),2)
        self.assertEqual({t.track_id:int(t.detection.bbox.x) for t in result},{1:2,2:202})

    def test_temporal_fall_immobility_recovery(self):
        estimator=TemporalEstimator(Config(immobile_seconds=.3,review_seconds=.5))
        def step(t,box,motion): return estimator.update(Track(1,detection(t,**box)),motion,'CAM-01')
        step(0,{},Motion())
        step(.1,{'y':40},Motion(vy_px_s=200,reliable=True))
        o=step(.2,{'y':70,'w':110,'h':40},Motion(vy_px_s=200,reliable=True,flow_px_s=10))
        self.assertTrue(o.fall_candidate)
        for t in [.3,.4,.5,.6,.7,.8,.9]:
            o=step(t,{'y':70,'w':110,'h':40},Motion(reliable=True,flow_px_s=0))
        self.assertEqual(o.state,State.IMMOBILE)
        self.assertEqual(o.action,'human_review')
        self.assertLessEqual(o.evidence_score,1)
        o=step(1,{},Motion(reliable=True,flow_px_s=0))
        self.assertEqual(o.action,'dismiss')

    def test_horizontal_first_frame_not_fall(self):
        e=TemporalEstimator(Config())
        o=e.update(Track(1,detection(0,w=120,h=40)),Motion(),'CAM-01')
        self.assertFalse(o.fall_candidate)

    def test_missing_history_no_immobility(self):
        e=TemporalEstimator(Config())
        e.update(Track(1,detection(0)),Motion(),'CAM-01')
        o=e.update(Track(1,detection(3,w=120,h=40)),Motion(),'CAM-01')
        self.assertFalse(o.fall_candidate)
        self.assertEqual(o.stationary_duration,0)

    def test_motion_quality_and_translation(self):
        rng=np.random.default_rng(1); a=rng.integers(30,220,(120,160),dtype=np.uint8)
        b=np.roll(a,3,axis=1); box=Box(x=0,y=0,w=160,h=120)
        m=analyze_pair(a,b,box,.1,(0,0))
        self.assertTrue(m.reliable); self.assertGreater(m.flow_px_s,5)
        self.assertFalse(analyze_pair(a,np.zeros_like(a),box,.1,(0,0)).reliable)
        self.assertFalse(analyze_pair(a,b,box,2,(0,0)).reliable)

    def test_tool_bounds_and_empty(self):
        for a,b in [(0,11),(2,1),(1,1)]:
            with self.assertRaises(ValidationError): WindowRequest(track_id=1,start=a,end=b)
        result=EvidenceTools().analyze_temporal_window(WindowRequest(track_id=1,start=0,end=1))
        self.assertEqual(result.status,'insufficient_evidence')

    def test_region_inspection(self):
        tools=EvidenceTools()
        request=RegionRequest(bbox=Box(x=0,y=0,w=20,h=20),timestamp=0,track_id=1)
        result=tools.inspect_region(request,np.zeros((20,20,3),np.uint8))
        self.assertEqual(result.status,'insufficient_evidence')
        with self.assertRaises(ValueError): tools.inspect_region(request,np.zeros((10,10,3),np.uint8))

    def test_bounded_history_and_future(self):
        tools=EvidenceTools(); estimator=TemporalEstimator(Config())
        for i in range(1000):
            observation=estimator.update(Track(1,detection(i*.1)),Motion(),'CAM-01')
            tools.add(observation)
        self.assertLessEqual(len(tools.history),101)
        with self.assertRaises(ValueError): tools.analyze_temporal_window(WindowRequest(track_id=1,start=100,end=101))

    def test_sitting_does_not_trigger(self):
        estimator=TemporalEstimator(Config())
        for i in range(10):
            o=estimator.update(Track(1,detection(i*.1,y=20+i*3,h=100-i*4)),
                Motion(vy_px_s=30,flow_px_s=10,reliable=True),'CAM-01')
            self.assertFalse(o.fall_candidate)

    def test_low_sampling_rate_breaks_continuity(self):
        estimator=TemporalEstimator(Config(sample_fps=1))
        estimator.update(Track(1,detection(0)),Motion(),'CAM-01')
        o=estimator.update(Track(1,detection(1,w=120,h=40)),Motion(vy_px_s=100),'CAM-01')
        self.assertFalse(o.fall_candidate)


if __name__=='__main__': unittest.main()
