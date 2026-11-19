"""Authenticate the USA expanded ROM and all 109 original-code anchors."""
from pathlib import Path
import argparse, hashlib, gzip, csv, io
from unpack_sources import CATALOG_SHA256, INDEX_SHA256, unpack

ROM_SHA1 = '6ea0ed71032ce08fc2745f412d84936382197494'

def verify(rom_path: Path, root: Path):
    rom = rom_path.read_bytes()
    if len(rom)!=33554432 or hashlib.sha1(rom).hexdigest()!=ROM_SHA1:
        raise ValueError('wrong original USA expanded ROM')
    raw = gzip.decompress((root/'candidate_index.tsv.gz').read_bytes())
    if hashlib.sha256(raw).hexdigest()!=INDEX_SHA256:
        raise ValueError('candidate manifest hash mismatch')
    records = list(csv.DictReader(io.StringIO(raw.decode('utf-8')),delimiter='\t'))
    if len(records)!=109:
        raise ValueError('expected 109 functions')
    for row in records:
        offset=int(row['rom_offset'],16)
        size=int(row['size'])
        if hashlib.sha256(rom[offset:offset+size]).hexdigest()!=row['original_sha256']:
            raise ValueError('mismatch at '+row['name'])
    print('PASS: %d authenticated original-USA code anchors / %d instruction bytes' %
          (len(records),sum(int(x['size']) for x in records)))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--usa-expanded',type=Path,required=True)
    p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    a=p.parse_args()
    verify(a.usa_expanded,a.root)
