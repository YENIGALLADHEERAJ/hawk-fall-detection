"""Mechanism regressions, using synthetic boxes only in unit tests."""
import unittest
from vision.schemas import Config, Motion, State, WindowRequest
from vision.tracking import PersonTracker, Track
from vision.temporal_v2 import SequenceEstimator
from vision.tools import EvidenceTools
from test_perception import detection


class TrackingRecoveryTests(unittest.TestCase):
    def tracker(self):
        return PersonTracker(max_gap=1.5,improved=True)

    def test_missing_frames_reassociate_without_emitting_boxes(self):
        tracker=self.tracker(); first=tracker.update([detection(0)],0)[0].track_id
        for t in [.2,.4,.6,.8,1.]:self.assertEqual(tracker.update([],t),[])
        found=tracker.update([detection(1.2,y=90,w=110,h=40)],1.2)
        self.assertEqual(found[0].track_id,first)
        self.assertEqual([d.timestamp for d in found[0].history],[0,1.2])

    def test_retention_boundary_and_expiry(self):
        for t,same in [(1.5,True),(1.50001,False)]:
            tracker=self.tracker();tracker.update([detection(0)],0)
            self.assertEqual(tracker.update([detection(t)],t)[0].track_id==1,same)

    def test_prediction_does_not_run_away_after_missing_frames(self):
        tracker=self.tracker();tracker.update([detection(0)],0)
        tracker.update([detection(.1,x=40)],.1)
        tracker.update([],.8)
        self.assertEqual(tracker.update([detection(1,x=40)],1)[0].track_id,1)

    def test_two_people_one_missing_does_not_take_other_identity(self):
        tracker=self.tracker();tracker.update([detection(0),detection(0,x=300)],0)
        for t in [.2,.4,.6]:tracker.update([detection(t,x=300)],t)
        found=tracker.update([detection(.8,x=302),detection(.8,y=90,w=110,h=40)],.8)
        self.assertEqual({t.track_id:round(t.detection.bbox.x) for t in found},{1:30,2:302})

    def test_ambiguous_return_gets_new_id(self):
        tracker=self.tracker();tracker.update([detection(0,x=30),detection(0,x=50)],0)
        self.assertNotIn(tracker.update([detection(.8,x=40)],.8)[0].track_id,[1,2])

    def test_low_confidence_only_continues_existing_tracks(self):
        tracker=PersonTracker(1.5,improved=True,new_track_threshold=.3)
        low=detection(0).model_copy(update={'confidence':.2})
        self.assertEqual(tracker.update([low],0),[])
        tracker.update([detection(.1)],.1)
        matched=detection(.2).model_copy(update={'confidence':.2})
        distant=detection(.2,x=300).model_copy(update={'confidence':.2})
        found=tracker.update([matched,distant],.2)
        self.assertEqual([t.track_id for t in found],[1])

    def test_low_confidence_cannot_steal_high_confidence_match(self):
        tracker=PersonTracker(1.5,improved=True,new_track_threshold=.3)
        tracker.update([detection(0)],0)
        low=detection(.1).model_copy(update={'confidence':.2})
        high=detection(.1,x=32)
        found=tracker.update([low,high],.1)
        self.assertEqual(len(found),1)
        self.assertEqual(found[0].detection.confidence,.9)


class SequenceTests(unittest.TestCase):
    def setUp(self):
        self.e=SequenceEstimator(Config(improved_temporal=True,immobile_seconds=.3,review_seconds=.5))

    def step(self,t,motion=None,track_id=1,**box):
        return self.e.update(Track(track_id,detection(t,**box)),motion or Motion(),'CAM-01')

    def fall(self,t=.2):
        self.step(0)
        return self.step(t,y=90,w=110,h=40)

    def test_gap_can_support_fall_but_not_immobility(self):
        o=self.fall(1.2)
        self.assertTrue(o.fall_event_detected)
        self.assertEqual(o.stationary_duration,0)
        self.assertEqual(o.action,'request_temporal_evidence')

    def test_immediate_recovery_preserves_event_then_dismisses(self):
        o=self.fall();self.assertTrue(o.fall_event_detected)
        recovered=self.step(.3)
        self.assertEqual(recovered.action,'dismiss')
        self.assertFalse(recovered.fall_candidate)
        self.assertFalse(recovered.fall_event_detected)

    def test_new_fall_after_recovery(self):
        self.fall();self.step(.3)
        second=self.step(.5,y=90,w=110,h=40)
        self.assertTrue(second.fall_event_detected)
        self.assertNotEqual(second.action,'dismiss')

    def test_continuous_immobility_separate_from_event(self):
        self.fall()
        for t in [.3,.4,.5,.6,.7,.8,.9]:
            o=self.step(t,Motion(reliable=True,flow_px_s=0),y=90,w=110,h=40)
        self.assertEqual(o.state,State.IMMOBILE)
        self.assertEqual(o.action,'human_review')
        self.assertFalse(o.fall_event_detected)
        self.assertTrue(o.fall_candidate)

    def test_gap_resets_stationary_clock(self):
        self.fall();self.step(.3,Motion(reliable=True,flow_px_s=0),y=90,w=110,h=40)
        o=self.step(1.2,y=90,w=110,h=40)
        self.assertTrue(o.fall_candidate)
        self.assertEqual(o.stationary_duration,0)
        self.assertNotEqual(o.state,State.IMMOBILE)

    def test_sitting_crouching_partial_occlusion(self):
        for box in [dict(y=55,h=65,w=45),dict(y=70,h=50,w=45),dict(y=50,h=70,w=20)]:
            self.setUp();self.step(0)
            self.assertFalse(self.step(.2,**box).fall_candidate)

    def test_compact_squat_with_large_height_loss_and_widening(self):
        self.step(0,w=25,h=100)
        o=self.step(.8,y=70,w=45,h=54)
        self.assertFalse(o.fall_candidate)
        self.assertGreater(o.transition_signals['net_drop_heights'],.18)
        self.assertGreater(o.transition_signals['width_ratio'],1.4)

    def test_aspect_jitter_and_old_velocity_cannot_create_fall(self):
        self.step(0,y=200,w=80,h=120)
        o=self.step(.4,Motion(vy_px_s=300),y=210,w=140,h=100)
        self.assertFalse(o.fall_candidate)
        self.assertEqual(o.decision_reason,'insufficient_net_downward_displacement')

    def test_no_cross_person_fall_history(self):
        self.step(0,track_id=1)
        self.assertFalse(self.step(.2,track_id=2,y=90,w=110,h=40).fall_candidate)

    def test_transition_boundary_and_stale_reference(self):
        self.assertTrue(self.fall(1.5).fall_event_detected)
        self.setUp();self.assertFalse(self.fall(1.50001).fall_event_detected)

    def test_timestamp_order_and_tool_window_boundaries(self):
        tools=EvidenceTools();tools.add(self.step(0));tools.add(self.step(.2,y=90,w=110,h=40))
        result=tools.analyze_temporal_window(WindowRequest(track_id=1,start=0,end=.2))
        self.assertEqual(len(result.observations),2)
        with self.assertRaises(ValueError):self.step(.2)
        with self.assertRaises(ValueError):tools.analyze_temporal_window(WindowRequest(track_id=1,start=0,end=.21))


if __name__=='__main__':unittest.main()


class CompactCollapseTests(unittest.TestCase):
    """Optional collapse-in-place path: box center barely moves, so the center-drop gate cannot fire."""
    def estimator(self, ratio):
        return SequenceEstimator(Config(improved_temporal=True, compact_collapse_height_ratio=ratio))

    def run_collapse(self, e, **box):
        e.update(Track(1, detection(0)), Motion(), 'CAM-01')
        return e.update(Track(1, detection(.2, **box)), Motion(), 'CAM-01')

    def test_off_by_default_so_compact_collapse_is_not_a_candidate(self):
        self.assertIsNone(Config().compact_collapse_height_ratio)
        self.assertFalse(self.run_collapse(self.estimator(None), y=55, w=80, h=50).fall_event_detected)

    def test_enabled_accepts_horizontal_collapse_with_small_center_drop(self):
        o = self.run_collapse(self.estimator(.6), y=55, w=80, h=50)
        self.assertTrue(o.fall_event_detected)
        self.assertTrue(o.transition_signals['compact_collapse'])
        self.assertLess(o.transition_signals['net_drop_heights'], .18)

    def test_enabled_still_requires_horizontal_box(self):
        # Squat-like: large height loss but the box is not wider than tall by the horizontal ratio.
        self.assertFalse(self.run_collapse(self.estimator(.6), y=55, w=50, h=50).fall_event_detected)

    def test_enabled_requires_enough_height_loss(self):
        self.assertFalse(self.run_collapse(self.estimator(.6), y=40, w=90, h=70).fall_event_detected)

    def test_enabled_rejects_rising_center(self):
        self.assertFalse(self.run_collapse(self.estimator(.6), y=10, w=80, h=50).fall_event_detected)
