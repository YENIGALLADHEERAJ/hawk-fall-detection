"""Recreate licensed local assets; refuse mismatched content."""
import hashlib
import json
import urllib.request
import zipfile
from pathlib import Path
from fetch_footage import RemoteZip


def write_verified(target, payload, expected):
    if hashlib.sha256(payload).hexdigest() != expected:
        raise ValueError(f'checksum mismatch: {target}')
    if not target.resolve().is_relative_to(Path('data').resolve()):
        raise ValueError('destination must be within data')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(payload)


def main():
    model = json.loads(Path('datasets/assets.json').read_text())['model']
    target = Path(model['path'])
    if not target.exists():
        with urllib.request.urlopen(model['url'], timeout=60) as response:
            write_verified(target, response.read(model['bytes'] + 1), model['sha256'])
    elif hashlib.sha256(target.read_bytes()).hexdigest() != model['sha256']:
        raise ValueError('existing model checksum mismatch')
    remote = None
    try:
        clips=json.loads(Path('datasets/manifest.json').read_text())
        if Path('datasets/holdout.json').exists():
            clips.extend(json.loads(Path('datasets/holdout.json').read_text()))
        for clip in clips:
            target = Path(clip['path'])
            if target.exists():
                if hashlib.sha256(target.read_bytes()).hexdigest() != clip['sha256']:
                    raise ValueError(f'existing clip mismatch: {target}')
                continue
            if 'member' in clip:
                if remote is None:
                    remote = zipfile.ZipFile(RemoteZip())
                info = remote.getinfo(clip['member'])
                if info.file_size > 30_000_000:
                    raise ValueError('clip too large')
                payload = remote.read(info)
            else:
                url = clip['source'].replace('https://github.com/', 'https://raw.githubusercontent.com/').replace('/tree/', '/')
                with urllib.request.urlopen(url, timeout=60) as response:
                    payload = response.read(30_000_001)
                if len(payload) > 30_000_000:
                    raise ValueError('clip too large')
            write_verified(target, payload, clip['sha256'])
            print(target, flush=True)
    finally:
        if remote:
            remote.close()


if __name__ == '__main__':
    main()
