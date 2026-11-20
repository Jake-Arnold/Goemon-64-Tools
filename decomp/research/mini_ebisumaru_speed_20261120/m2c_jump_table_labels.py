"""Research-only input normalization: writes scratch m2c inputs, never original ASM."""
from pathlib import Path
import argparse
import re

TARGETS = ("801CD450", "801CD484", "801CD420", "801CD3CC",
           "801CD3F0", "801E1DDC", "801E1DE4", "801E1DEC", "801E1DF4")
TABLES = ("jtbl_8020A85C_5C676C", "jtbl_8020B2E0_5C71F0")

def normalize(asm: str, data: str):
    for vma in TARGETS:
        found = re.search(r"(?m)^\s*(\.L" + vma + r"_[A-Za-z0-9]+):", asm)
        if found:
            label = found.group(1)
        else:
            label = ".L" + vma + "_M2C"
            pos = re.search(r"(?m)^\s*/\* [0-9A-F]{6} " + vma + r" ", asm)
            if pos is None:
                raise ValueError(f"missing code for VMA 0x{vma}")
            asm = asm[:pos.start()] + "\n" + label + ":\n" + asm[pos.start():]
        for table in TABLES:
            block = re.search(r"(?ms)^(?:nonmatching )?" + table + r"\s*$.*?^enddlabel " + table + r"\s*$", data)
            if block:
                normalized = re.sub(r"(?<=\.word )0x" + vma + r"\b", label, block.group(0))
                data = data[:block.start()] + normalized + data[block.end():]
    for table in TABLES:
        block = re.search(r"(?ms)^dlabel " + table + r"\s*$(.*?)^enddlabel " + table + r"\s*$", data)
        if not block or ".word 0x801CD450" in block.group(1) or ".word 0x801E1DDC" in block.group(1):
            raise ValueError(f"missing or unnormalized table {table}")
    return asm, data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    root = args.upstream / "asm/usa"
    asm, data = normalize((root/"587370.s").read_text(), (root/"data/5B8500.data.s").read_text())
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out/"file11_symbolic_m2c.s").write_text(asm)
    (args.out/"file11_data_symbolic_m2c.s").write_text(data)
    print("Temporary m2c input copies written. Original game ASM/ROM unchanged.")

if __name__ == "__main__":
    main()
