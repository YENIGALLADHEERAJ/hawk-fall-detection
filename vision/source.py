"""File replay and explicitly requested camera capture with bounded recovery."""
from dataclasses import dataclass
import multiprocessing as mp
import queue
import time
import cv2
import numpy as np


@dataclass
class Sample:
    status: str
    frame: object = None
    timestamp: float = 0.
    index: int = 0


def camera_worker(device, messages):
    """Isolate native open/read calls so the parent can terminate a stuck backend."""
    capture = None
    try:
        capture = cv2.VideoCapture(device)
        if not capture.isOpened():
            messages.put(('open_failed', None, time.monotonic()))
            return
        while True:
            ok, frame = capture.read()
            if not ok:
                messages.put(('disconnected', None, time.monotonic()))
                return
            if frame is None or frame.dtype != np.uint8 or frame.ndim != 3 or frame.shape[2] != 3:
                messages.put(('corrupt_frame', None, time.monotonic()))
                return
            h, w = frame.shape[:2]
            if max(h, w) > 1280:
                scale = 1280 / max(h, w)
                frame = cv2.resize(frame, (round(w * scale), round(h * scale)))
            message = ('frame', frame, time.monotonic())
            try:
                messages.put_nowait(message)
            except queue.Full:
                # Prefer current evidence to a growing inference backlog.
                try:
                    messages.get_nowait()
                except queue.Empty:
                    pass
                try:
                    messages.put_nowait(message)
                except queue.Full:
                    pass
    except Exception:
        try:
            messages.put_nowait(('capture_error', None, time.monotonic()))
        except queue.Full:
            pass
    finally:
        if capture is not None:
            capture.release()


class VideoSource:
    def __init__(self, source, timeout=2., retries=2, worker=camera_worker):
        self.live = isinstance(source, int)
        self.source, self.timeout, self.retries = source, timeout, retries
        self.worker = worker
        self.origin = time.monotonic()
        self.index = 0
        self.attempts = 0
        self.process = self.messages = self.capture = None
        self.closed = False
        if self.live:
            if source < 0 or not 0 < timeout <= 10 or not 0 <= retries <= 5:
                raise ValueError('invalid camera limits')
            self.fps = None
            self.expected_frames = 0
            self._start()
        else:
            self.capture = cv2.VideoCapture(str(source))
            if not self.capture.isOpened():
                self.capture.release()
                raise ValueError(f'cannot open video: {source}')
            self.fps = self.capture.get(cv2.CAP_PROP_FPS)
            self.expected_frames = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
            if not np.isfinite(self.fps) or self.fps <= 0:
                self.capture.release()
                raise ValueError('file must expose a valid frame rate')

    @property
    def elapsed(self):
        return time.monotonic() - self.origin if self.live else self.index / self.fps

    def _start(self):
        context = mp.get_context('spawn')
        self.messages = context.Queue(maxsize=2)
        self.process = context.Process(target=self.worker, args=(self.source, self.messages), daemon=True)
        self.process.start()

    def _stop(self):
        if self.process:
            if self.process.is_alive():
                self.process.terminate()
            self.process.join(timeout=1)
            if self.process.is_alive():
                self.process.kill()
                self.process.join(timeout=1)
        if self.messages:
            self.messages.cancel_join_thread()
            self.messages.close()

    def read(self):
        if self.closed:
            return Sample('closed', timestamp=self.elapsed)
        if not self.live:
            ok, frame = self.capture.read()
            if not ok:
                status = 'decode_failure' if self.expected_frames > 0 and self.index < self.expected_frames - 1 else 'eof'
                return Sample(status, timestamp=self.elapsed, index=self.index)
            result = Sample('frame', frame, self.index / self.fps, self.index)
            self.index += 1
            return result
        try:
            status, frame, stamp = self.messages.get(timeout=self.timeout)
        except queue.Empty:
            status, frame, stamp = 'capture_timeout', None, time.monotonic()
        if status == 'frame':
            self.index += 1
            return Sample(status, frame, stamp - self.origin, self.index - 1)
        self._stop()
        if self.attempts < self.retries:
            self.attempts += 1
            self._start()
            return Sample('reconnecting:' + status, timestamp=stamp - self.origin, index=self.index)
        self.closed = True
        return Sample('source_failed:' + status, timestamp=stamp - self.origin, index=self.index)

    def release(self):
        if self.capture:
            self.capture.release()
        if not self.closed and self.live:
            self._stop()
        self.closed = True
