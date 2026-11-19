"""Reconstruct 50 original-address IDO C units from the authenticated source catalog."""
from pathlib import Path
import argparse
import hashlib

CATALOG_SHA256 = "2b2f5f49ad89935ba7312a49b2aee4af3e6ffb8b041167895382acf13cf9b57f"
HEADER = "typedef unsigned char u8;typedef unsigned short u16;typedef unsigned int u32;typedef signed int s32;\n"

def generate(root, output):
    raw = (root / "source_catalog.txt").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == CATALOG_SHA256, "catalog hash mismatch"
    lines = raw.decode("utf-8").splitlines()
    assert len(lines) == 50, "expected 50 translation units"
    output.mkdir(parents=True, exist_ok=True)
    count = 0
    for index, line in enumerate(lines):
        unit, sep, definitions = line.partition(" ")
        assert sep and unit == "batch53_%03d" % index and definitions.endswith("|")
        (output / (unit + ".c")).write_bytes((HEADER + definitions.replace("|", "\n")).encode("utf-8"))
        count += definitions.count("|")
    assert count == 53, "expected 53 functions"
    return count

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "sources")
    a = p.parse_args()
    print("Generated %d exact C function sources" % generate(Path(__file__).resolve().parent, a.output))
