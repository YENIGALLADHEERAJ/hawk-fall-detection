import tempfile
import unittest
import json
from pathlib import Path
from vision.pipeline import run_video
from vision.schemas import Config


class RealIntegration(unittest.TestCase):
    @unittest.skipUnless(Path('data/models/yolox.onnx').exists() and Path('data/clips/gmdcsa_ADL_13.mp4').exists(),
                         'licensed compact sitting clip unavailable')
    def test_combined_real_compact_sitting_is_not_fall(self):
        with tempfile.TemporaryDirectory(dir='data') as output:
            result=run_video('data/clips/gmdcsa_ADL_13.mp4',output,Config())
            self.assertEqual(result['candidate_times'],[])

    @unittest.skipUnless(Path('data/models/yolox.onnx').exists() and Path('data/clips/clip_06.mp4').exists(),
                         'licensed squat clip unavailable')
    def test_combined_real_squat_is_not_fall(self):
        with tempfile.TemporaryDirectory(dir='data') as output:
            result=run_video('data/clips/clip_06.mp4',output,Config())
            self.assertEqual(result['candidate_times'],[])

    @unittest.skipUnless(Path('data/models/yolox.onnx').exists() and Path('data/clips/gmdcsa_Fall_11.mp4').exists(),
                         'licensed long fall clip unavailable')
    def test_combined_real_fall_to_immobility(self):
        with tempfile.TemporaryDirectory(dir='data') as output:
            result=run_video('data/clips/gmdcsa_Fall_11.mp4',output,
                             Config(improved_tracking=True,improved_temporal=True))
            rows=[json.loads(line) for line in (Path(output)/'observations.jsonl').read_text().splitlines()]
            self.assertTrue(result['candidate_times'])
            self.assertTrue(any(row['fall_event_detected'] for row in rows))
            self.assertTrue(any(row['state']=='IMMOBILE' for row in rows))

    @unittest.skipUnless(Path('data/models/yolox.onnx').exists() and Path('data/clips/clip_00.mp4').exists(),
                         'licensed short fall clip unavailable')
    def test_combined_real_short_fall(self):
        with tempfile.TemporaryDirectory(dir='data') as output:
            result=run_video('data/clips/clip_00.mp4',output,
                             Config(improved_tracking=True,improved_temporal=True))
            self.assertTrue(result['candidate_times'])

    @unittest.skipUnless(Path('data/models/yolox.onnx').exists() and Path('data/clips/clip_00.mp4').exists(),
                         'download licensed model and clip_00 for actual DNN integration')
    def test_real_video_to_candidate(self):
        with tempfile.TemporaryDirectory(dir='data') as output:
            result=run_video('data/clips/clip_00.mp4',output,Config(sample_fps=5))
            self.assertGreater(result['detections'],0)
            self.assertEqual(result['distinct_track_ids'],1)
            self.assertTrue(result['candidate_times'])
            self.assertGreater(result['tool_calls'],0)
            self.assertTrue(list(Path(output).glob('incidents/*/annotated.jpg')))
            self.assertTrue(list(Path(output).glob('incidents/*/window.avi')))
            self.assertEqual(result['exit_reason'],'eof')

    def test_bad_input(self):
        if not Path('data/models/yolox.onnx').exists(): self.skipTest('model unavailable')
        with tempfile.TemporaryDirectory(dir='data') as output:
            with self.assertRaises(ValueError): run_video('data/no-such-video.mp4',output)

    @unittest.skipUnless(Path('data/models/yolox.onnx').exists() and Path('data/clips/gmdcsa_Fall_11.mp4').exists(),
                         'licensed long fall clip unavailable')
    def test_real_fall_to_immobility(self):
        with tempfile.TemporaryDirectory(dir='data') as output:
            result=run_video('data/clips/gmdcsa_Fall_11.mp4',output,Config(sample_fps=5))
            self.assertTrue(result['candidate_times'])
            rows=[json.loads(line) for line in (Path(output)/'observations.jsonl').read_text().splitlines()]
            self.assertTrue(any(row['state']=='IMMOBILE' for row in rows))
            trace=json.loads((Path(output)/'trace.json').read_text())
            names={call['tool'] for call in trace['tools']}
            self.assertIn('analyze_temporal_window',names)
            self.assertIn('inspect_region',names)
            self.assertEqual(result['distinct_track_ids'],1)
