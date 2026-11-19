"""Original IDO instruction gate. This is NOT the canonical all-C build verifier."""
import argparse, hashlib, re, subprocess, tempfile
from pathlib import Path
from regenerate_sources import generate

ROM_SHA1 = "6ea0ed71032ce08fc2745f412d84936382197494"
FLAGS = "-c -G 0 -non_shared -Xfullwarn -Xcpluscomm -Iinclude -Ilibultra/include -Ilibultra/include/PR -Isrc -I. -Wab,-r4300_mul -woff 649,838,712 -D_LANGUAGE_C -D_FINALROM -DF3DEX_GBI -D__sgi -DNDEBUG -O2 -mips2".split()
RE = re.compile(r"^\s*\d+:\s+([0-9a-fA-F]+)\s+(\d+)\s+FUNC\s+\S+\s+\S+\s+\S+\s+(func_[0-9A-Fa-f]+_([0-9A-Fa-f]+))$", re.M)

def verify(rom_path, upstream, cc, objcopy):
    rom = rom_path.read_bytes()
    assert len(rom) == 33554432 and hashlib.sha1(rom).hexdigest() == ROM_SHA1, "unauthenticated expanded USA ROM"
    count, size_total = 0, 0
    with tempfile.TemporaryDirectory(prefix="goemon-file18-") as temp:
        work = Path(temp)
        generate(Path(__file__).resolve().parent, work / "sources")
        for src in sorted((work / "sources").glob("*.c")):
            obj, raw = work / (src.stem + ".o"), work / (src.stem + ".bin")
            subprocess.run([str(cc), *FLAGS, "-o", str(obj), str(src)], cwd=upstream, check=True)
            subprocess.run([objcopy, "-O", "binary", "-j", ".text", str(obj), str(raw)], check=True)
            compiled = raw.read_bytes()
            syms = subprocess.check_output(["readelf", "-Ws", str(obj)], text=True)
            matches = list(RE.finditer(syms))
            assert matches, "no original function symbols: " + src.name
            for m in matches:
                position, length = int(m.group(1), 16), int(m.group(2))
                offset = int(m.group(4), 16)
                assert length and length % 4 == 0 and position + length <= len(compiled)
                if compiled[position:position + length] != rom[offset:offset + length]:
                    raise ValueError("original native-code mismatch: " + m.group(3))
                count += 1
                size_total += length
    assert count == 53 and size_total == 796, (count, size_total)
    print("PASS: 53 original-USA native-exact functions / 796 bytes")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--usa-expanded", type=Path, required=True)
    p.add_argument("--upstream", type=Path, required=True)
    p.add_argument("--ido", type=Path)
    p.add_argument("--objcopy", default="mips-linux-gnu-objcopy")
    a = p.parse_args()
    upstream = a.upstream.resolve()
    cc = a.ido.resolve() if a.ido else upstream / "tools/ido-5.3/cc"
    verify(a.usa_expanded, upstream, cc, a.objcopy)
