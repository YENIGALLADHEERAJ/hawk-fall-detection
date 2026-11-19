"""Bounded MOT17 identity-validation extract: publisher frames 1..301 every 6th and ground truth.

Same method as fetch_mot_audit.py (HTTP range reads of the official zip, no full archive) for any
sequence. Does not modify datasets/phase1c/validation.json. CC BY-NC-SA 3.0, local research only.
Usage: python scripts/fetch_mot_sequence.py MOT17-02-FRCNN
"""
import hashlib
import json
import sys
import time
import zipfile
from pathlib import Path
import cv2
import numpy as np
from fetch_footage import RemoteZip as _RemoteZip


class RemoteZip(_RemoteZip):
    """Adds 2 MiB read-ahead blocks: zipfile asks for ~4 KiB at a time, i.e. one HTTP round trip each."""
    BLOCK = 2 * 1024 * 1024

    def __init__(self, *a, **k):
        super().__init__(*a, **k); self._cache = (0, b'')

    def read(self, n=-1):
        n = self.size - self.pos if n < 0 else min(n, self.size - self.pos)
        if not n: return b''
        start, data = self._cache
        if not (start <= self.pos and self.pos + n <= start + len(data)):
            fetch_at = self.pos; length = max(n, self.BLOCK) if n <= 30_000_000 else n
            length = min(length, self.size - fetch_at, 30_000_000)
            real = self.pos; self.pos = fetch_at
            data = _RemoteZip.read(self, length); self._cache = (fetch_at, data); self.pos = real
            start = fetch_at
        out = data[self.pos - start:self.pos - start + n]; self.pos += n
        return out


def retry(fn, tries=6):
    for n in range(tries):
        try: return fn()
        except Exception as exc:
            if n == tries - 1: raise
            print('retry', n + 1, type(exc).__name__, exc, flush=True); time.sleep(3 * (n + 1))


def main(sequence):
    short = sequence.lower().replace('-frcnn', '').replace('mot17-', 'mot17_')
    folder = Path(f'data/sources/{sequence.lower()}-identity'); folder.mkdir(parents=True, exist_ok=True)
    url = 'https://motchallenge.net/data/MOT17.zip'
    archive = retry(lambda: zipfile.ZipFile(RemoteZip(url, 5860214001)), 10)
    prefix = [n for n in archive.namelist() if n.endswith(f'{sequence}/gt/gt.txt')]
    if len(prefix) != 1: raise RuntimeError('unexpected archive layout')
    prefix = prefix[0][:-len('gt/gt.txt')]
    (folder / 'gt.txt').write_bytes(retry(lambda: archive.read(prefix + 'gt/gt.txt')))
    (folder / 'seqinfo.ini').write_bytes(retry(lambda: archive.read(prefix + 'seqinfo.ini')))
    output = Path(f'data/clips/identity_{short}.avi'); output.parent.mkdir(parents=True, exist_ok=True); mapping = []
    for i, original in enumerate(range(1, 302, 6)):
        path = folder / f'{original:06d}.jpg'
        if not path.exists() or cv2.imread(str(path)) is None:  # resumable: keep verified frames
            info = archive.getinfo(prefix + f'img1/{original:06d}.jpg')
            if info.file_size > 3_000_000: raise ValueError('frame too large')
            def get():
                nonlocal archive
                try: return archive.read(info)
                except Exception:
                    archive = zipfile.ZipFile(RemoteZip(url, 5860214001)); info2 = archive.getinfo(info.filename)
                    raise
            path.write_bytes(retry(get, 12))
        payload = path.read_bytes()
        mapping.append({'frame_index': i, 'original_frame': original, 'timestamp': i / 5,
                        'sha256': hashlib.sha256(payload).hexdigest()})
    writer = None
    for entry in mapping:
        frame = cv2.imread(str(folder / f"{entry['original_frame']:06d}.jpg"))
        if frame is None: raise ValueError('frame decode failed')
        if writer is None:
            h, w = frame.shape[:2]; print('frame size', w, h, flush=True)
            writer = cv2.VideoWriter(str(output), cv2.VideoWriter_fourcc(*'MJPG'), 5, (w, h))
            if not writer.isOpened(): raise OSError('writer failed')
        writer.write(frame)
    writer.release()
    (folder / 'mapping.json').write_text(json.dumps(mapping, indent=2))
    print('ready', output, len(mapping), 'frames', sum(p.stat().st_size for p in folder.glob('*.jpg')) // 1024, 'KiB of frames')


if __name__ == '__main__': main(sys.argv[1])
