"""Bounded range extraction from CC BY 4.0 Ivan Ursul dataset v2.

Reads central directory; only explicitly selected members are downloaded. No
untrusted archive paths are extracted. See datasets/README.md for attribution.
"""
import argparse
import io
import json
import urllib.request
import zipfile
from pathlib import Path

URL = 'https://ndownloader.figshare.com/files/52990358'
SIZE = 2529520868


class RemoteZip(io.RawIOBase):
    def __init__(self, url=URL, size=SIZE): self.pos, self.url, self.size = 0, url, size
    def seekable(self): return True
    def readable(self): return True
    def tell(self): return self.pos
    def seek(self, offset, whence=0):
        self.pos = offset if whence == 0 else self.pos+offset if whence == 1 else self.size+offset
        return self.pos
    def read(self, n=-1):
        n = self.size-self.pos if n < 0 else min(n,self.size-self.pos)
        if not n: return b''
        if n > 30_000_000: raise ValueError('download exceeds 30 MB per request')
        req = urllib.request.Request(self.url,headers={'Range':f'bytes={self.pos}-{self.pos+n-1}'})
        with urllib.request.urlopen(req,timeout=60) as r:
            if r.status != 206: raise RuntimeError('server must support byte ranges')
            # CDN range caching must not return a different segment.
            if not r.headers.get('Content-Range','').startswith(f'bytes {self.pos}-'):
                raise RuntimeError('incorrect HTTP range')
            result=r.read(n+1)
        if len(result) != n: raise RuntimeError('short range')
        self.pos += n
        return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--member')
    parser.add_argument('--output')
    args=parser.parse_args()
    with zipfile.ZipFile(RemoteZip()) as z:
        if not args.member:
            members=[{'name':i.filename,'size':i.file_size,'compressed':i.compress_size} for i in z.infolist()]
            Path('data/sources/zip-index.json').write_text(json.dumps(members,indent=2))
            print(json.dumps(members[:40],indent=2))
        else:
            info=z.getinfo(args.member)
            if info.file_size > 30_000_000: raise ValueError('member too large')
            target=Path(args.output).resolve()
            root=Path('data').resolve()
            if not target.is_relative_to(root): raise ValueError('output must be within data/')
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(z.read(info))
            print(target,info.file_size)


if __name__=='__main__': main()
