import unittest
import numpy as np
from vision.pose import evidence
from vision.schemas import Config, Motion, PoseEvidence
from vision.temporal_v2 import SequenceEstimator
from vision.tracking import Track
from test_perception import detection


def pose(hip_height_px):
    return PoseEvidence(hip_ankle_px=hip_height_px, torso_angle_deg=5., keypoints=17)


class PoseEvidenceTests(unittest.TestCase):
    def kp(self, **joints):
        k = np.zeros((17, 3), np.float32)
        for name, (x, y, s) in joints.items(): k[int(name[1:])] = [x, y, s]
        return k

    def test_missing_joints_give_none_not_a_guess(self):
        e = evidence(self.kp(j11=(50, 60, .9), j12=(60, 60, .9)))   # hips only, no ankles or shoulders
        self.assertIsNone(e.hip_ankle_px); self.assertIsNone(e.torso_angle_deg); self.assertEqual(e.keypoints, 2)

    def test_hip_ankle_and_torso_angle(self):
        e = evidence(self.kp(j5=(50, 20, .9), j6=(60, 20, .9), j11=(50, 50, .9), j12=(60, 50, .9), j15=(50, 90, .9), j16=(60, 90, .9)))
        self.assertAlmostEqual(e.hip_ankle_px, 40); self.assertAlmostEqual(e.torso_angle_deg, 0)
        flat = evidence(self.kp(j5=(10, 50, .9), j6=(10, 50, .9), j11=(60, 50, .9), j12=(60, 50, .9)))
        self.assertAlmostEqual(flat.torso_angle_deg, 90)

    def test_low_confidence_keypoints_are_dropped(self):
        e = evidence(self.kp(j11=(50, 60, .1), j12=(60, 60, .1), j15=(50, 90, .9), j16=(60, 90, .9)))
        self.assertIsNone(e.hip_ankle_px)


class PoseRuleTests(unittest.TestCase):
    def estimator(self, **config):
        return SequenceEstimator(Config(improved_temporal=True, **config))

    def step(self, e, t, hip_px, **box):
        return e.update(Track(1, detection(t, **box)), Motion(), 'CAM-01', pose(hip_px))

    def stand(self, e, ts=(0, .2)):
        for t in ts: self.step(e, t, 35)     # hip height 0.35 of the 100 px reference box

    def test_off_by_default_no_pose_rule(self):
        e = self.estimator(); self.stand(e)
        o = self.step(e, .6, 3, y=60, w=45, h=50)   # compact, hips on the floor; box gate does not fire
        self.assertFalse(o.fall_event_detected)

    def test_hip_drop_makes_candidate_when_box_gate_cannot(self):
        e = self.estimator(pose_hip_drop=.2); self.stand(e)
        o = self.step(e, .6, 5, y=60, w=45, h=50)
        self.assertTrue(o.fall_event_detected); self.assertEqual(o.transition_signals['pose_hip_drop'], 1.)

    def test_slow_hip_drop_is_not_a_fall(self):
        e = self.estimator(pose_hip_drop=.2); e.update(Track(1, detection(0)), Motion(), 'CAM-01', pose(35))
        o = e.update(Track(1, detection(1.4, y=60, w=45, h=50)), Motion(), 'CAM-01', pose(5))   # .30 in 1.4 s = .21/s
        self.assertTrue(o.fall_event_detected)   # just above the rate gate
        e2 = self.estimator(pose_hip_drop=.2, pose_drop_rate=.3)
        e2.update(Track(1, detection(0)), Motion(), 'CAM-01', pose(35))
        self.assertFalse(e2.update(Track(1, detection(1.4, y=60, w=45, h=50)), Motion(), 'CAM-01', pose(5)).fall_event_detected)

    def test_hips_that_stay_high_never_trigger_the_drop_rule(self):
        e = self.estimator(pose_hip_drop=.2); self.stand(e)
        o = self.step(e, .6, 33, y=60, w=45, h=50)
        self.assertFalse(o.fall_event_detected)

    def test_no_pose_means_no_pose_rule(self):
        e = self.estimator(pose_hip_drop=.2)
        for t in (0, .2): e.update(Track(1, detection(t)), Motion(), 'CAM-01')
        self.assertFalse(e.update(Track(1, detection(.6, y=60, w=45, h=50)), Motion(), 'CAM-01').fall_event_detected)

    def test_veto_blocks_box_fall_while_hips_stay_high(self):
        box = dict(y=90, w=110, h=40)    # box gate alone detects this (horizontal, big drop)
        plain = self.estimator(); self.stand(plain)
        self.assertTrue(self.step(plain, .4, 33, **box).fall_event_detected)
        vetoed = self.estimator(pose_veto_hip_height=.28); self.stand(vetoed)
        o = self.step(vetoed, .4, 33, **box)
        self.assertFalse(o.fall_event_detected); self.assertEqual(o.decision_reason, 'pose_hips_still_high')

    def test_veto_does_not_block_when_hips_are_low(self):
        e = self.estimator(pose_veto_hip_height=.28); self.stand(e)
        self.assertTrue(self.step(e, .4, 5, y=90, w=110, h=40).fall_event_detected)

    def test_config_validation(self):
        self.assertFalse(Config().pose_evidence); self.assertIsNone(Config().pose_hip_drop); self.assertIsNone(Config().pose_veto_hip_height)
        with self.assertRaises(Exception): Config(pose_hip_drop=0)


if __name__ == '__main__': unittest.main()
