"""Read-only original-USA and Japan-0 ROM anchors for actor/graphics research.

Input must be *decompressed 32 MiB* images. No ROM bytes are emitted.
"""
import argparse
import hashlib
import json
from pathlib import Path

USA_SHA1 = '6ea0ed71032ce08fc2745f412d84936382197494'
JP_SHA1 = '6f8745fecc3a5e7d4918c7a73353eb0726116ded'
TARGETS = (
    ('func_80019160_19D60', 0x19D60, 108,
     '9de12852d3db1d6254a898ec8d3130f26de26eecc4da9da0eb4a062c4cf3b0b8'),
    ('func_8001E2BC_1EEBC', 0x1EEBC, 196,
     '04f8e30635d170d59c6541e6cc4b91f9f2b0285b830ea6c3c6b16eefb0082ad0'),
    ('func_8001E380_1EF80', 0x1EF80, 100,
     'd8b6f95d1f6e1baf976d2cd8b630afcad968584e77f7b3e9ecb6e1afe8f78dd4'),
)
# Independently observed JP equivalent in original 32 MiB ROM at 0x1EB80.
EXPECTED_CHANGED_WORDS = (0x28, 0x2C, 0x48, 0x4C, 0x68, 0x6C, 0xA8)
EXPECTED_JP_HALFWORD_STORE_OFFSETS = (0xE1D0, 0xE1D0, 0xE1D2, 0xE1D2, 0xE1D4, 0xE1D4)

def verify(usa, japan):
    if len(usa) != 33_554_432 or hashlib.sha1(usa).hexdigest() != USA_SHA1:
        raise ValueError('Unverified original expanded USA ROM')
    if len(japan) != 33_554_432 or hashlib.sha1(japan).hexdigest() != JP_SHA1:
        raise ValueError('Unverified original expanded Japan-0 ROM')
    for name, start, size, expected in TARGETS:
        if hashlib.sha256(usa[start:start + size]).hexdigest() != expected:
            raise ValueError('Original-USA graphics function fingerprint changed: ' + name)
    usa_fn = usa[0x1EEBC:0x1EEBC + 196]
    jp_fn = japan[0x1EB80:0x1EB80 + 196]
    differences = tuple(i for i in range(0,196,4) if usa_fn[i:i+4] != jp_fn[i:i+4])
    if differences != EXPECTED_CHANGED_WORDS:
        raise ValueError('Unexpected regional graphics function differences')
    store_offsets = tuple(int.from_bytes(jp_fn[i+2:i+4],'big') for i in differences[:6])
    if store_offsets != EXPECTED_JP_HALFWORD_STORE_OFFSETS:
        raise ValueError('Japanese counterpart store addresses differ')
    return {'status': 'PASS', 'usa_functions': len(TARGETS),
            'japan_equivalent_rom_offset': '0x1EB80',
            'usa_equivalent_rom_offset': '0x1EEBC',
            'counterpart_original_word_differences': len(differences),
            'usa_global_u16': ['0x801689F0','0x801689F2','0x801689F4'],
            'jp_global_u16': ['0x8016E1D0','0x8016E1D2','0x8016E1D4'],
            'offset_displacement': '+0x57E0 (not +0x57F0)',
            'jp_gameplay_proof': 'NOT_RUN'}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--usa-expanded',type=Path,required=True)
    p.add_argument('--japan-expanded',type=Path,required=True)
    args=p.parse_args()
    print(json.dumps(verify(args.usa_expanded.read_bytes(),args.japan_expanded.read_bytes()),indent=2))

if __name__=='__main__':main()
