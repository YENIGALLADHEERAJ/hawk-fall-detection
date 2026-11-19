import itertools
import unittest
import numpy as np
from vision.schemas import Box, Detection, Config
from vision.tracking import PersonTracker, appearance_feature, appearance_distance, optimal_assignment


def det(t, x, y=20, w=40, h=100):
    return Detection(bbox=Box(x=x, y=y, w=w, h=h), confidence=.9, timestamp=t, frame_index=round(t * 10))


def frame_with(color_by_box):
    frame = np.full((200, 400, 3), 128, np.uint8)
    for (x, y, w, h), bgr in color_by_box:
        frame[y:y + h, x:x + w] = bgr
    return frame


class AssignmentTests(unittest.TestCase):
    def test_matches_brute_force_including_rectangular(self):
        rng = np.random.default_rng(3)
        for n, m in [(3, 3), (2, 4), (4, 2), (5, 5), (1, 3)]:
            for _ in range(20):
                cost = rng.random((n, m))
                pairs = optimal_assignment(cost)
                got = sum(cost[r, c] for r, c in pairs)
                k = min(n, m)
                best = min(sum(cost[r, c] for r, c in zip(rows, cols))
                           for rows in itertools.combinations(range(n), k)
                           for cols in itertools.permutations(range(m), k))
                self.assertEqual(len(pairs), k)
                self.assertAlmostEqual(got, best, places=9)
                self.assertEqual(len({r for r, _ in pairs}), k); self.assertEqual(len({c for _, c in pairs}), k)

    def test_empty(self):
        self.assertEqual(optimal_assignment(np.zeros((0, 3))), [])


class AppearanceTests(unittest.TestCase):
    def test_distance_separates_colours_and_is_symmetric(self):
        box = Box(x=50, y=20, w=40, h=100)
        red = appearance_feature(frame_with([((50, 20, 40, 100), (0, 0, 255))]), box)
        red2 = appearance_feature(frame_with([((50, 20, 40, 100), (0, 0, 250))]), box)
        blue = appearance_feature(frame_with([((50, 20, 40, 100), (255, 0, 0))]), box)
        self.assertLess(appearance_distance(red, red2), .2)
        self.assertGreater(appearance_distance(red, blue), .8)
        self.assertAlmostEqual(appearance_distance(red, blue), appearance_distance(blue, red))
        self.assertIsNone(appearance_distance(None, red))

    def test_small_or_offscreen_box_has_no_feature(self):
        frame = np.zeros((100, 100, 3), np.uint8)
        self.assertIsNone(appearance_feature(frame, Box(x=0, y=0, w=5, h=5)))
        self.assertIsNone(appearance_feature(frame, Box(x=300, y=300, w=40, h=100)))


class TrackerTests(unittest.TestCase):
    def crossing(self, tracker, use_features):
        red = appearance_feature(frame_with([((100, 20, 40, 100), (0, 0, 255))]), Box(x=100, y=20, w=40, h=100))
        blue = appearance_feature(frame_with([((140, 20, 40, 100), (255, 0, 0))]), Box(x=140, y=20, w=40, h=100))
        first = tracker.update([det(0, 100), det(0, 140)], 0, [red, blue] if use_features else None)
        ids = {round(t.detection.bbox.x): t.track_id for t in first}
        # Equidistant detections that swap sides: geometry alone cannot tell who is who.
        second = tracker.update([det(.2, 120), det(.2, 121)], .2, [blue, red] if use_features else None)
        return ids, {round(t.detection.bbox.x): t.track_id for t in second}

    def test_appearance_keeps_identity_when_geometry_is_ambiguous(self):
        tracker = PersonTracker(1.5, improved=True, appearance_weight=2., optimal=True)
        ids, after = self.crossing(tracker, True)
        red_id, blue_id = ids[100], ids[140]
        self.assertEqual(after[121], red_id)   # the red-feature detection continues the red track
        self.assertEqual(after[120], blue_id)

    def test_defaults_ignore_features_and_stay_greedy(self):
        a = PersonTracker(1.5, improved=True); b = PersonTracker(1.5, improved=True)
        dets = [[det(0, 100), det(0, 140)], [det(.2, 104), det(.2, 143)], [det(.4, 108), det(.4, 146)]]
        feats = [np.ones(128, np.float32) / 128] * 2
        for t, d in zip((0, .2, .4), dets):
            ra = [x.track_id for x in a.update(d, t)]
            rb = [x.track_id for x in b.update(d, t, feats)]
            self.assertEqual(ra, rb)

    def test_config_option_off_by_default(self):
        c = Config()
        self.assertFalse(c.identity_tracking)


if __name__ == '__main__': unittest.main()
