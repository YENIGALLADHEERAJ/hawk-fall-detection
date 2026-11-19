"""Transport fixtures test failures only; real perception integration is separate."""
import time
import tempfile
import unittest
from pathlib import Path
import cv2
import numpy as np
from vision.source import VideoSource


def disconnected_worker(device, messages):
    messages.put(('disconnected', None, time.monotonic()))


def stalled_worker(device, messages):
    time.sleep(30)


def frame_then_disconnect(device, messages):
    messages.put(('frame', np.zeros((16, 16, 3), np.uint8), time.monotonic()))
    messages.put(('disconnected', None, time.monotonic()))


class SourceTests(unittest.TestCase):
    def test_file_timestamps_and_eof(self):
        with tempfile.TemporaryDirectory(dir='data') as folder:
            path=Path(folder)/'test.avi'
            writer=cv2.VideoWriter(str(path),cv2.VideoWriter_fourcc(*'MJPG'),10,(32,32))
            for _ in range(3): writer.write(np.zeros((32,32,3),np.uint8))
            writer.release()
            source=VideoSource(path)
            try:
                self.assertEqual([source.read().timestamp for _ in range(3)],[0,.1,.2])
                self.assertEqual(source.read().status,'eof')
            finally: source.release()

    def test_reconnect_budget(self):
        source=VideoSource(0,timeout=5,retries=1,worker=disconnected_worker)
        try:
            self.assertEqual(source.read().status,'reconnecting:disconnected')
            self.assertEqual(source.read().status,'source_failed:disconnected')
            self.assertEqual(source.attempts,1)
            self.assertFalse(source.process.is_alive())
        finally: source.release()

    def test_stalled_native_call_can_be_terminated(self):
        source=VideoSource(0,timeout=.25,retries=0,worker=stalled_worker)
        start=time.monotonic()
        try:
            self.assertEqual(source.read().status,'source_failed:capture_timeout')
            self.assertLess(time.monotonic()-start,5)
            self.assertFalse(source.process.is_alive())
        finally: source.release()

    def test_reconnect_does_not_replay_old_frame(self):
        source=VideoSource(0,timeout=5,retries=1,worker=frame_then_disconnect)
        try:
            first=source.read()
            self.assertEqual(first.status,'frame')
            self.assertEqual(source.read().status,'reconnecting:disconnected')
            second=source.read()
            self.assertEqual(second.status,'frame')
            self.assertGreater(second.timestamp,first.timestamp)
            self.assertGreater(second.index,first.index)
        finally: source.release()


if __name__=='__main__': unittest.main()
