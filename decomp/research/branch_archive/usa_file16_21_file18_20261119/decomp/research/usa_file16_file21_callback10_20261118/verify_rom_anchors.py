"""Verify original USA expanded-ROM identities without publishing code bytes."""
import argparse
import hashlib
import json
from pathlib import Path

EXPECTED_SHA1 = '6ea0ed71032ce08fc2745f412d84936382197494'
EXPECTED_SIZE = 33_554_432

def verify(rom_path: Path, manifest_path: Path) -> None:
    rom = rom_path.read_bytes()
    if len(rom) != EXPECTED_SIZE or hashlib.sha1(rom).hexdigest() != EXPECTED_SHA1:
        raise SystemExit('FAIL: not the authenticated original 32 MiB USA expanded ROM')
    data = json.loads(manifest_path.read_text())
    for item in data:
        offset = int(item['rom_offset'],16)
        exact = hashlib.sha256(rom[offset:offset+item['size']]).hexdigest()
        if exact != item['original_bytes_sha256']:
            raise SystemExit(f"FAIL: original ROM anchor mismatch: {item['name']}")
    print(f"PASS: {len(data)} original-USA ROM anchors, {sum(item['size'] for item in data)} bytes")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--usa-expanded',type=Path,required=True)
    parser.add_argument('--manifest',type=Path,default=Path(__file__).with_name('candidate_manifest.json'))
    args = parser.parse_args()
    verify(args.usa_expanded,args.manifest)
