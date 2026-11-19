"""Read-only USA expanded-ROM anchors for eight dracam research C routines."""
import argparse
import hashlib
from pathlib import Path

SHA1 = "6ea0ed71032ce08fc2745f412d84936382197494"
ANCHORS = (
    ("func_800125D0_131D0", 0x131D0, 32, "7abe3e7fff0963bfcb4e6b333fa738d03ddb1d3147b3ca02f8573f4f34fbdf55"),
    ("func_800125F0_131F0", 0x131F0, 56, "ac878d351b008d3cceab74f04549b02c1bf66807463ae88fff3930d20b3877bc"),
    ("func_80012878_13478", 0x13478, 136, "e0b15f25722e152961d45bb72ae751004c01b0552a70413872f9f09a78d60c0b"),
    ("func_80012900_13500", 0x13500, 56, "8b39c71444408f6bd8f7b20011c6daf3d4ca5ba155c050d15865a4bcf3707026"),
    ("func_80012938_13538", 0x13538, 8, "9da6c79208c17fe1f1a131bde1f22ad091012ee963b41f9f1b5b73d51ee9322c"),
    ("func_800133D4_13FD4", 0x13FD4, 12, "3e09d863e4735eab26aa2dc3321f40f0e54ca61228fa275a3924d256bf05484a"),
    ("func_800133E0_13FE0", 0x13FE0, 32, "5ac8c04bfd5044d48649fa29217ef11385d853508fcff5445d9376620cec3ca5"),
    ("func_80013508_14108", 0x14108, 20, "ee48a3d93e5ceb8995eb80cddfce7cc0884f4e9c34dc8546c18d5ecb121a05f2"),
)

def verify(path: Path) -> None:
    rom = path.read_bytes()
    if len(rom) != 33_554_432 or hashlib.sha1(rom).hexdigest() != SHA1:
        raise SystemExit("FAIL: unexpected expanded-USA ROM size or SHA-1")
    for name, address, length, expected in ANCHORS:
        actual = hashlib.sha256(rom[address:address + length]).hexdigest()
        if actual != expected:
            raise SystemExit(f"FAIL: original code anchor mismatch: {name}")
    print(f"PASS: {len(ANCHORS)} original-USA ROM anchors, {sum(x[2] for x in ANCHORS)} bytes")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--usa-expanded", type=Path, required=True)
    verify(parser.parse_args().usa_expanded)
