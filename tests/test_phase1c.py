import unittest
from unittest.mock import Mock
import numpy as np
from evaluation.localization_audit import match,summarize
from vision.detection import YoloXDetector
from vision.schemas import Config,Motion,State
from vision.temporal_v2 import SequenceEstimator
from vision.tracking import Track,PersonTracker
from vision.tools import EvidenceTools
from vision.schemas import WindowRequest
from test_perception import detection


class FreshAuditTests(unittest.TestCase):
    def test_matching_does_not_reuse_one_box_for_two_people(self):
        box=[0,0,40,100]
        self.assertEqual(len(match([box,box],[box],.5)),1)

    def test_reference_relative_jitter_ignores_real_translation(self):
        samples=[]
        for t,x in enumerate([0,50,100]):
            box=[x,0,x+40,100]
            samples.append({'timestamp':t,'references':[{'box':box,'identity':1,'phase':'walk'}],
                'predictions':[{'box':box,'track_id':1}]})
        result=summarize(samples)
        self.assertEqual(result['recall_iou50'],1)
        self.assertEqual(result['mean_reference_relative_center_jitter'],0)
        self.assertEqual(result['mean_reference_relative_log_area_change'],0)

    def test_missed_span_is_lower_bound_and_fragment_is_explicit(self):
        box=[0,0,40,100];samples=[]
        for t,identity in [(0,1),(.2,None),(.4,None),(.6,2)]:
            samples.append({'timestamp':t,'references':[{'box':box,'identity':1,'phase':'ground'}],
                'predictions':[] if identity is None else [{'box':box,'track_id':identity}]})
        result=summarize(samples)
        self.assertAlmostEqual(result['longest_missed_sample_span_seconds'],.2)
        self.assertEqual(result['id_switches'],1)
        self.assertEqual(result['fragments_after_missing'],1)

    def test_rotation_experiment_does_not_skip_when_original_person_visible(self):
        detector=object.__new__(YoloXDetector);detector.rotation_fallback=True;detector.all_views=True;detector.threshold=.3
        detector._detect_single=Mock(side_effect=[[detection(0)],[detection(0,x=20,y=150,w=40,h=80)],[]])
        found=detector.detect(np.zeros((200,300,3),np.uint8),0,0)
        self.assertEqual(detector._detect_single.call_count,3)
        self.assertEqual(len(found),2)
        self.assertEqual(found[1].inference_view,'clockwise')
        self.assertFalse(Config().rotation_all_views)

    def test_partial_movement_preserves_fall_but_resets_stationarity(self):
        estimator=SequenceEstimator(Config())
        def step(t,**kw):return estimator.update(Track(1,detection(t,**kw)),Motion(reliable=True,flow_px_s=0),'CAM-01')
        step(0);self.assertTrue(step(.2,y=90,w=110,h=40).fall_event_detected)
        step(.4,y=90,w=110,h=40)
        moved=estimator.update(Track(1,detection(.6,y=90,w=110,h=40)),Motion(reliable=True,flow_px_s=20),'CAM-01')
        self.assertTrue(moved.fall_candidate);self.assertEqual(moved.stationary_duration,0)
        self.assertNotEqual(moved.state,State.RECOVERY)

    def test_initial_ground_is_not_a_fall(self):
        estimator=SequenceEstimator(Config())
        for t in [0,.2,.4,.6]:
            o=estimator.update(Track(1,detection(t,y=90,w=110,h=40)),Motion(reliable=True,flow_px_s=0),'CAM-01')
            self.assertFalse(o.fall_candidate)

    def test_ambiguous_short_overlap_experiment_does_not_transfer_history(self):
        tracker=PersonTracker(max_gap=1.5,improved=True,reject_short_ambiguity=True)
        original=tracker.update([detection(0,x=30),detection(0,x=50)],0)
        estimator=SequenceEstimator(Config());tools=EvidenceTools()
        # A has a fall history; B has none. Identical visible geometry cannot resolve ownership.
        estimator.update(Track(1,detection(0)),Motion(),'CAM-01')
        a=estimator.update(Track(1,detection(.1,y=90,w=110,h=40)),Motion(),'CAM-01');tools.add(a)
        found=tracker.update([detection(.2,x=40)],.2)
        self.assertNotIn(found[0].track_id,[t.track_id for t in original])
        self.assertEqual(found[0].velocity,(0.,0.))
        self.assertEqual(len(found[0].history),1)
        b=estimator.update(found[0],Motion(),'CAM-01');tools.add(b)
        self.assertFalse(b.fall_candidate);self.assertNotEqual(b.state,State.RECOVERY)
        window=tools.analyze_temporal_window(WindowRequest(track_id=b.track_id,start=0,end=.2))
        self.assertTrue(all(o.track_id==b.track_id for o in window.observations))
        self.assertTrue(estimator.memory[1].candidate)

    def test_seated_compact_transition_is_documented_geometry_limit(self):
        estimator=SequenceEstimator(Config())
        estimator.update(Track(1,detection(0,w=74,h=109)),Motion(),'CAM-01')
        o=estimator.update(Track(1,detection(.4,y=50,w=108,h=67)),Motion(),'CAM-01')
        self.assertFalse(o.fall_event_detected)  # insufficient net center descent, despite changed posture
        self.assertEqual(o.decision_reason,'insufficient_net_downward_displacement')

    def test_falling_person_occluded_while_neighbor_walks_keeps_ownership(self):
        tracker=PersonTracker(max_gap=1.5,improved=True);estimator=SequenceEstimator(Config());tools=EvidenceTools()
        for t,detections in [(0,[detection(0),detection(0,x=180)]),
                (.2,[detection(.2,y=90,w=110,h=40),detection(.2,x=170)]),
                (.4,[detection(.4,x=160)]),(.6,[detection(.6,x=150)])]:
            observed=[]
            for track in tracker.update(detections,t):
                o=estimator.update(track,Motion(),'CAM-01');tools.add(o);observed.append(o)
            if t==.2:
                self.assertTrue(next(o for o in observed if o.track_id==1).fall_candidate)
            if t>=.4:
                self.assertEqual([o.track_id for o in observed],[2])
                self.assertFalse(observed[0].fall_candidate)
                self.assertNotEqual(observed[0].state,State.RECOVERY)
                self.assertAlmostEqual(tracker.tracks[2].velocity[0],-50)
                self.assertTrue(estimator.memory[1].candidate)
        window=tools.analyze_temporal_window(WindowRequest(track_id=2,start=0,end=.6))
        self.assertTrue(all(not o.fall_candidate and o.track_id==2 for o in window.observations))

    def test_intention_is_not_observable_from_identical_box_trajectories(self):
        # A safety limitation: intentional rapid lying can satisfy exactly the same geometry.
        outcomes=[]
        for _semantic_label in ('fall','intentional_lie'):
            estimator=SequenceEstimator(Config())
            estimator.update(Track(1,detection(0)),Motion(),'CAM-01')
            outcomes.append(estimator.update(Track(1,detection(.2,y=90,w=110,h=40)),Motion(),'CAM-01').fall_event_detected)
        self.assertEqual(outcomes,[True,True])

if __name__=='__main__':unittest.main()
