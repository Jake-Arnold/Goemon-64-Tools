"""Unpack the exact original-ID0 C research sources from the compressed catalogue."""
from pathlib import Path
import argparse
import gzip
import hashlib
import re

CATALOG_SHA256 = '2135ade4ae21af39c5963f446f109a9add3673d7eb48b95646114da34d6c9970'
INDEX_SHA256 = '2e81f4e5e2fe68d72b5eeadeed8eea1ff9a724e6ea5ac2ac0f53a3526193a086'

def unpack(root: Path, output: Path):
    catalog = gzip.decompress((root/'source_catalog.txt.gz').read_bytes())
    index = gzip.decompress((root/'candidate_index.tsv.gz').read_bytes())
    if hashlib.sha256(catalog).hexdigest() != CATALOG_SHA256:
        raise ValueError('source catalogue SHA-256 mismatch')
    if hashlib.sha256(index).hexdigest() != INDEX_SHA256:
        raise ValueError('candidate index SHA-256 mismatch')
    content = catalog.decode('utf-8')
    matches = list(re.finditer(r'^### (b109_[0-9A-F]+\.c)\n', content, re.M))
    if len(matches) != 71 or len(index.decode('utf-8').splitlines())-1 != 109:
        raise ValueError('research catalogue count mismatch')
    output.mkdir(parents=True, exist_ok=True)
    for i,m in enumerate(matches):
        source = content[m.end():matches[i+1].start() if i+1<len(matches) else len(content)]
        if not source.endswith('\n\n'):
            raise ValueError('unexpected C source boundary')
        (output/m.group(1)).write_bytes(source[:-1].encode('utf-8'))
    print('PASS: restored 71 original C source units; index contains 109 functions')

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    p.add_argument('--output',type=Path,default=Path(__file__).resolve().parent/'sources')
    a=p.parse_args()
    unpack(a.root,a.output)
