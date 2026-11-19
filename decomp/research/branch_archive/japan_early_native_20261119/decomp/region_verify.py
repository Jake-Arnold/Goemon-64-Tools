"""Region-aware Goemon matching-C verification, preserving the USA verifier.

USA requests forward unchanged to decomp.verify. Japan uses an independent,
strict manifest and existing original-ROM/IDO source-linked build outputs.
No ROMs, build objects, or user-specific paths are written to Git.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile

from . import japan_asm_baseline, japan_first_c, japan_four_c
from .japan_relocation_policy import MODE_SOURCE, WARP_SOURCE, REVIEWED, verify_text_relocations

ROOT = Path(__file__).resolve().parent
JAPAN_MANIFEST = ROOT / "regions/japan_0.json"
PINNED_COMMIT = "7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee"
ROM_START_VRAM_DELTA = 0x7FFFF400
_SHA1 = re.compile(r"[0-9a-f]{40}\Z")
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_NAME = re.compile(r"func_([0-9A-Fa-f]{8})_([0-9A-Fa-f]+)\Z")


def _relative(path: object, prefix: str | None = None) -> Path:
    if not isinstance(path, str) or not path or "\\" in path:
        raise ValueError("Unsafe manifest path")
    parsed = PurePosixPath(path)
    if parsed.is_absolute() or any(part in ("", ".", "..") for part in parsed.parts):
        raise ValueError("Unsafe manifest path")
    if prefix is not None and not path.startswith(prefix):
        raise ValueError("Unexpected manifest path prefix")
    return Path(*parsed.parts)


def load_manifest(path: Path = JAPAN_MANIFEST) -> dict:
    manifest = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or set(manifest) != {
        "format", "region", "upstream_commit", "retail", "expanded",
        "splat_original", "splat_candidate", "link_map", "units"
    }:
        raise ValueError("Invalid region manifest fields")
    if manifest["format"] != "goemon-region-matching-v1" or manifest["region"] != "japan_0":
        raise ValueError("Unsupported region manifest")
    if manifest["upstream_commit"] != PINNED_COMMIT:
        raise ValueError("Unsupported upstream revision")
    for key, sha, length in (
        ("retail", japan_asm_baseline.JAPAN_RETAIL_SHA1, japan_asm_baseline.RETAIL_SIZE),
        ("expanded", japan_asm_baseline.JAPAN_EXPANDED_SHA1, japan_asm_baseline.EXPANDED_SIZE),
    ):
        spec = manifest[key]
        if not isinstance(spec, dict) or set(spec) != {"size", "sha1"} or spec != {"size": length, "sha1": sha}:
            raise ValueError(f"Wrong {key} reference ROM identity")
    pinned_paths = {
        "splat_original": "config/japan_0/splat.yaml",
        "link_map": "build/japan_0/mnsg.map",
    }
    stages = {
        "config/japan_0/splat_four_c.local.yaml": ("jp_bit_array.c", "jp_main_38620.c"),
        "config/japan_0/splat_five_c.local.yaml": ("jp_bit_array.c", "jp_main_38620.c", "jp_motion_12D60.c"),
        "config/japan_0/splat_six_c.local.yaml": ("jp_bit_array.c", "jp_main_38620.c", "jp_motion_12D60.c", "jp_camera_13B70.c"),
        "config/japan_0/splat_nine_c.local.yaml": ("jp_bit_array.c", "jp_main_38620.c", "jp_motion_12D60.c", "jp_camera_13B70.c", "jp_mode_flags.c"),
        "config/japan_0/splat_ten_c.local.yaml": ("jp_bit_array.c", "jp_main_38620.c", "jp_motion_12D60.c", "jp_camera_13B70.c", "jp_mode_flags.c", "jp_warp_call_37900.c"),
        "config/japan_0/splat_eighteen_c.local.yaml": ("jp_bit_array.c", "jp_camera_13B70.c", "jp_main_38620.c", "jp_mode_flags.c", "jp_motion_12D60.c", "jp_state_37D1C.c", "jp_transition_37870.c", "jp_warp_37920.c", "jp_warp_37B58.c", "jp_warp_37C4C.c", "jp_warp_37C84.c", "jp_warp_37CB8.c", "jp_warp_37CE0.c", "jp_warp_call_37900.c"),
    }
    target_sources = stages.get(manifest["splat_candidate"])
    if target_sources is None:
        raise ValueError("Unexpected Japanese splat_candidate path")
    for key, expected in pinned_paths.items():
        if manifest[key] != expected:
            raise ValueError(f"Unexpected Japanese {key} path")
    units = manifest["units"]
    if not isinstance(units, list) or not units:
        raise ValueError("No Japanese C translation units")
    seen_names, seen_sources, ranges = set(), set(), []
    for unit in units:
        if not isinstance(unit, dict) or set(unit) != {
            "source", "staged_source", "source_sha256", "object", "rom_offset", "vram",
            "section_size", "section_sha256", "functions"
        }:
            raise ValueError("Invalid Japanese C unit fields")
        source = _relative(unit["source"], "japan_matching/")
        staged = _relative(unit["staged_source"], "src/")
        obj = _relative(unit["object"], "build/japan_0/src/")
        if staged.name != source.name or obj.name != staged.name + ".o":
            raise ValueError("C source/object ownership mismatch")
        if str(source) in seen_sources:
            raise ValueError("Duplicate Japanese source path")
        seen_sources.add(str(source))
        if not isinstance(unit["source_sha256"], str) or not _SHA256.fullmatch(unit["source_sha256"]):
            raise ValueError("Invalid C source SHA-256")
        if not isinstance(unit["section_sha256"], str) or not _SHA256.fullmatch(unit["section_sha256"]):
            raise ValueError("Invalid C section SHA-256")
        start, vram, size = unit["rom_offset"], unit["vram"], unit["section_size"]
        if any(type(x) is not int for x in (start, vram, size)) or size <= 0 or size % 4 or start % 4 or vram % 4:
            raise ValueError("Misaligned or invalid Japanese C section")
        if start + size > japan_asm_baseline.EXPANDED_SIZE or vram - start != ROM_START_VRAM_DELTA:
            raise ValueError("Japanese ROM offset and VMA disagree")
        funcs = unit["functions"]
        if not isinstance(funcs, list) or not funcs:
            raise ValueError("Japanese C unit lacks function bounds")
        offset = 0
        for fn in funcs:
            if not isinstance(fn, dict) or set(fn) != {"name", "rom_offset", "vram", "size"}:
                raise ValueError("Invalid Japanese function record")
            name = fn["name"]
            found = _NAME.fullmatch(name) if isinstance(name, str) else None
            if found is None or name in seen_names:
                raise ValueError("Invalid or duplicate Japanese function name")
            seen_names.add(name)
            nrom, nvram, nsize = fn["rom_offset"], fn["vram"], fn["size"]
            if (any(type(x) is not int for x in (nrom, nvram, nsize)) or nsize <= 0 or nsize % 4
                or nrom != start + offset or nvram != vram + offset
                or int(found.group(1), 16) != nvram or int(found.group(2), 16) != nrom):
                raise ValueError("Japanese function extent/name mismatch")
            offset += nsize
        if offset > size or size - offset >= 16:
            raise ValueError("Unexpected gap or overlap in Japanese C section")
        ranges.append((start, start + size))
    if sorted(Path(name).name for name in seen_sources) != sorted(target_sources):
        raise ValueError("Japanese selected C source units differ from Splat stage")
    ranges.sort()
    if any(left[1] > right[0] for left, right in zip(ranges, ranges[1:])):
        raise ValueError("Overlapping Japanese C source ranges")
    return manifest


def _sha(data: bytes, algorithm: str) -> str:
    return hashlib.new(algorithm, data).hexdigest()


def _read_image(path: Path, expected: dict, label: str) -> bytes:
    data = path.read_bytes()
    if len(data) != expected["size"] or _sha(data, "sha1") != expected["sha1"]:
        raise ValueError(f"{label} ROM hash/size mismatch")
    return data


def _object_text(objcopy: str, obj: Path) -> bytes:
    with tempfile.TemporaryDirectory() as temp:
        dest = Path(temp) / "section.bin"
        subprocess.run([objcopy, "--dump-section", f".text={dest}", str(obj)],
                       check=True, capture_output=True, text=True)
        return dest.read_bytes()


def _object_symbols(objdump: str, obj: Path) -> dict[str, tuple[int, int]]:
    listing = subprocess.run([objdump, "-t", str(obj)], check=True,
                             capture_output=True, text=True).stdout
    result = {}
    for line in listing.splitlines():
        match = re.fullmatch(r"\s*([0-9a-fA-F]+)\s+g\s+F\s+\.text\s+([0-9a-fA-F]+)\s+(\S+)\s*", line)
        if match:
            if match.group(3) in result:
                raise ValueError("Repeated global function symbol in object")
            result[match.group(3)] = (int(match.group(1), 16), int(match.group(2), 16))
    return result


def _map_section(mapping: str, unit: dict) -> None:
    obj = unit["object"]
    pattern = re.compile(r"(?m)^\s*\.text\s+0x([\da-fA-F]+)\s+0x([\da-fA-F]+)\s+" + re.escape(obj) + r"\s*$")
    rows = list(pattern.finditer(mapping))
    if len(rows) != 1:
        raise ValueError(f"Linked C object section missing or repeated: {obj}")
    address, size = int(rows[0][1], 16), int(rows[0][2], 16)
    if (address, size) != (unit["vram"], unit["section_size"]):
        raise ValueError(f"C object linked at wrong guest address/extent: {obj}")
    for fn in unit["functions"]:
        function_pattern = re.compile(r"(?m)^\s*0x([\da-fA-F]+)\s+" + re.escape(fn["name"]) + r"\s*$")
        funcs = list(function_pattern.finditer(mapping))
        if len(funcs) != 1 or int(funcs[0][1], 16) != fn["vram"]:
            raise ValueError(f"Missing or mismatched original VMA function in link map: {fn['name']}")


def _verify_stage(checkout: Path, manifest: dict | None = None) -> None:
    original = (checkout / japan_asm_baseline.PINNED_CONFIG).read_text(encoding="utf-8")
    expected = japan_four_c.render_config(japan_first_c.render_config(
        japan_asm_baseline.render_asm_config(original)))
    choice = (manifest or {}).get("splat_candidate", "config/japan_0/splat_four_c.local.yaml")
    if choice in ("config/japan_0/splat_five_c.local.yaml", "config/japan_0/splat_six_c.local.yaml",
                  "config/japan_0/splat_nine_c.local.yaml", "config/japan_0/splat_ten_c.local.yaml"):
        from . import japan_five_c
        expected = japan_five_c.render_config(expected)
        if choice in ("config/japan_0/splat_six_c.local.yaml", "config/japan_0/splat_nine_c.local.yaml",
                      "config/japan_0/splat_ten_c.local.yaml"):
            from . import japan_six_c
            expected = japan_six_c.render_config(expected)
        if choice in ("config/japan_0/splat_nine_c.local.yaml", "config/japan_0/splat_ten_c.local.yaml"):
            from . import japan_nine_c
            expected = japan_nine_c.render_config(expected)
        if choice == "config/japan_0/splat_ten_c.local.yaml":
            from . import japan_ten_c
            expected = japan_ten_c.render_config(expected)
    elif choice not in ("config/japan_0/splat_four_c.local.yaml", "config/japan_0/splat_eighteen_c.local.yaml"):
        raise ValueError("Unknown Japanese Splat stage")
    if choice == "config/japan_0/splat_eighteen_c.local.yaml":
        from . import japan_eighteen_c
        expected = japan_eighteen_c.render_config(original)
    staged = (checkout / choice).read_text(encoding="utf-8")
    if staged != expected:
        raise ValueError("Japanese Splat split differs from reviewed region-C variant")


def verify_japan(checkout: Path, retail_output: Path, manifest: dict, *,
                 source_dir: Path = ROOT, objcopy: str = "mips-linux-gnu-objcopy",
                 objdump: str = "mips-linux-gnu-objdump") -> dict:
    root, source_dir, retail_output = checkout.resolve(strict=True), source_dir.resolve(strict=True), retail_output.resolve(strict=True)
    if not root.is_dir() or not source_dir.is_dir():
        raise ValueError("Invalid Japanese build/source checkout")
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    if revision != manifest["upstream_commit"]:
        raise ValueError("Japanese build source commit is not pinned")
    if subprocess.run(["git", "diff", "--quiet"], cwd=root, check=False).returncode != 0:
        raise ValueError("Pinned upstream checkout has modified tracked sources")
    _verify_stage(root, manifest)
    orig_retail = _read_image(root / "config/japan_0/baserom.z64", manifest["retail"], "Original Japanese retail")
    if retail_output == (root / "config/japan_0/baserom.z64").resolve():
        raise ValueError("Retail build output may not be the original ROM")
    built_retail = _read_image(retail_output, manifest["retail"], "Recompressed Japanese retail")
    if built_retail != orig_retail:
        raise ValueError("Full Japanese retail ROM bytes differ")
    original = _read_image(root / "config/japan_0/baserom.decompressed.z64", manifest["expanded"], "Original Japanese expanded")
    rebuilt = _read_image(root / "build/japan_0/mnsg.z64", manifest["expanded"], "Source-linked Japanese expanded")
    if rebuilt != original:
        raise ValueError("Full Japanese expanded ROM bytes differ")
    if not (root / "build/japan_0/mnsg.elf").is_file():
        raise FileNotFoundError("Missing linked Japanese ELF")
    mapping = (root / "build/japan_0/mnsg.map").read_text(encoding="utf-8")
    proof_units = []
    for unit in manifest["units"]:
        source_data = (source_dir / unit["source"]).read_bytes()
        staged_data = (root / unit["staged_source"]).read_bytes()
        if source_data != staged_data or _sha(source_data, "sha256") != unit["source_sha256"]:
            raise ValueError(f"Japanese C source content/ownership mismatch: {unit['source']}")
        _map_section(mapping, unit)
        obj = root / unit["object"]
        extracted = _object_text(objcopy, obj)
        start, size = unit["rom_offset"], unit["section_size"]
        if len(extracted) != size or _sha(extracted, "sha256") != unit["section_sha256"]:
            raise ValueError(f"Japanese IDO object machine code mismatch: {obj}")
        # The mode setter's reviewed HI16/LO16 relocations resolve in the
        # already byte-verified linked image. All other objects remain exact
        # before linking and must not use unreviewed text relocations.
        if unit["source"] not in REVIEWED and extracted != original[start:start + size]:
            raise ValueError(f"Japanese original machine code differs: {obj}")
        syms = _object_symbols(objdump, obj)
        expected_syms = {fn["name"]:(fn["rom_offset"] - start, fn["size"])
                         for fn in unit["functions"]}
        if syms != expected_syms:
            raise ValueError(f"Japanese C object symbols do not match all reviewed functions: {obj}")
        reloc = subprocess.run([objdump, "-r", "-j", ".text", str(obj)],
                               check=True, capture_output=True, text=True).stdout
        relocation_count = verify_text_relocations(unit["source"], reloc)
        proof_units.append({"source":unit["source"], "source_sha256":unit["source_sha256"],
                            "object":unit["object"], "object_text_sha256":unit["section_sha256"],
                            "original_vram":f"0x{unit['vram']:08X}", "original_rom":f"0x{start:X}",
                            "section_bytes":size, "functions":unit["functions"],
                            "text_relocations":relocation_count, "status":"PASS"})
    funcs = [fn for unit in manifest["units"] for fn in unit["functions"]]
    return {"format":"goemon-region-exact-build-result-v1", "region":"japan_0",
            "status":"matched", "upstream_commit":revision,
            "expanded":{"sha1":manifest["expanded"]["sha1"],"bytes":len(rebuilt),"different_bytes":0,"status":"PASS"},
            "retail":{"sha1":manifest["retail"]["sha1"],"bytes":len(built_retail),"different_bytes":0,"status":"PASS"},
            "claims":{"functions":len(funcs),"function_bytes":sum(fn["size"] for fn in funcs),
                      "translation_units":len(proof_units), "note":"Manifest claims only; not whole-game ASM inventory"},
            "c_units":proof_units, "emulator_gameplay":"NOT RUN", "native_pc_runtime":"NOT RUN"}


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    selector = argparse.ArgumentParser(add_help=False)
    selector.add_argument("--region", choices=("usa", "japan_0"), default="usa")
    selection, forwarded = selector.parse_known_args(argv)
    if selection.region == "usa":
        # Retain the original USA CLI semantics, source manifest and build gates.
        from . import verify
        return verify.main(forwarded)
    parser = argparse.ArgumentParser(description="Verify an existing Japanese C source-linked build")
    parser.add_argument("--checkout", required=True, type=Path)
    parser.add_argument("--retail-output", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--manifest", type=Path, default=JAPAN_MANIFEST)
    parser.add_argument("--source-dir", type=Path, default=ROOT)
    parser.add_argument("--objcopy", default="mips-linux-gnu-objcopy")
    parser.add_argument("--objdump", default="mips-linux-gnu-objdump")
    args = parser.parse_args(forwarded)
    if args.report.exists() or args.report.is_symlink():
        parser.error("Report already exists; will not overwrite")
    if args.report.resolve() in (args.retail_output.resolve(), (args.checkout / "config/japan_0/baserom.z64").resolve()):
        parser.error("Report must not overwrite a game ROM")
    manifest = load_manifest(args.manifest)
    report = {"format":"goemon-region-exact-build-result-v1", "region":"japan_0", "status":"failed",
              "started_utc":datetime.now(timezone.utc).isoformat()}
    try:
        with args.report.open("x", encoding="utf-8") as output:
            try:
                result = verify_japan(args.checkout, args.retail_output, manifest,
                                      source_dir=args.source_dir, objcopy=args.objcopy, objdump=args.objdump)
                report.update(result)
            except (OSError, ValueError, subprocess.SubprocessError) as exc:
                report["error"] = str(exc)
            finally:
                report["ended_utc"] = datetime.now(timezone.utc).isoformat()
                json.dump(report, output, indent=2)
                output.write("\n")
    except OSError as exc:
        parser.exit(1, str(exc) + "\n")
    if report["status"] != "matched":
        parser.exit(1, report.get("error", "Japanese verification failed") + "\n")
    print(f"Japan MATCH: {report['claims']['functions']} C functions / "
          f"{report['claims']['function_bytes']} bytes; exact 32 MiB + retail ROMs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
