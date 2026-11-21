"""Verify sanitized USA overlay fingerprints using the user's private ROM.

The original ROM is only ever read from disk. Its code bytes are never emitted.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from decomp.state_runtime_trace import OVERLAY_READ_LEN, USA_ROM_SHA1, identify_image, load_fingerprints


def verify(rom_path: Path, manifest_path: Path | None = None) -> dict:
    rom = rom_path.read_bytes()
    actual_sha1 = hashlib.sha1(rom).hexdigest()
    if len(rom) != 33554432 or actual_sha1 != USA_ROM_SHA1:
        raise ValueError('Wrong USA reference ROM: expected 32 MiB decompressed original SHA1 '+USA_ROM_SHA1)
    db = load_fingerprints(manifest_path) if manifest_path is not None else load_fingerprints()
    matched = []
    for record in db['records']:
        start=int(record['rom_start'],16)
        end=int(record['rom_code_end'],16)
        if start<0 or start+OVERLAY_READ_LEN>end or end>len(rom):
            raise ValueError('Fingerprint crosses an original overlay code region')
        observed = identify_image(rom[start:start+OVERLAY_READ_LEN],db)
        if observed['image_file_id'] != record['file_id']:
            raise ValueError(f'Overlay fingerprint failed for ID {record["file_id"]}')
        matched.append(record['file_id'])
    return {'format':'goemon-usa-overlay-fingerprint-proof-v1',
            'rom_sha1':actual_sha1, 'rom_bytes':len(rom),
            'verified_image_ids':matched, 'verified_images':len(matched),
            'no_runtime_capture_performed':True}


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--rom',required=True,type=Path)
    ap.add_argument('--report',type=Path,required=True)
    args=ap.parse_args(argv)
    try:
        result=verify(args.rom)
        if args.report.exists():
            raise FileExistsError('Do not overwrite an existing proof report')
        args.report.parent.mkdir(parents=True,exist_ok=True)
        with args.report.open('x',encoding='utf-8') as f:
            json.dump(result,f,indent=2)
            f.write('\n')
    except (ValueError,OSError) as exc:
        ap.exit(1,str(exc)+'\n')
    print('PASS: '+str(result['verified_images'])+' original USA overlay signatures; no live-game execution claimed')

if __name__=='__main__':main()
