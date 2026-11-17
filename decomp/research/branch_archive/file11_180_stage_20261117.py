"""Versioned 180-function USA file_11 research adapter: preserve 179-C production.

This is opt-in only. Original-ROM/native object verification must pass before
any candidate is counted; this stage does not promote production.
"""
from __future__ import annotations

from collections import Counter
import copy
import hashlib
import re
from pathlib import Path

from . import file11_179_stage as parent, overlay_file11
from .research.file11_143_candidate.verify_file11_143 import (
    read_relocations, read_symbols, trim_text_object,
)

ROOT = Path(__file__).resolve().parent
STAGE_FORMAT = "goemon-file11-180-camera-reset-v1"
FUNC_NAME = "func_801F97D4_5B56E4"
C_STEM = "camera_reset_usa_5b56e4"
C_PATH = ROOT / "research" / (C_STEM + ".c")
C_SHA256 = "9d47ba199dfd48f5707b7623f45eee5e0853110f725e08bcf4ad7c151f7450c4"
START, A, B, C, END = 0x587370, 0x5B4E1C, 0x5B56E4, 0x5B576C, 0x5B64B8
OLD_PARENT_SHA256 = "929ffae0aa1938d6032fd859574dac1f9fd6149eabdfd1606b0378967ce69e10"
NEW_CHUNKS = (
    (A, B, "asm", None,
     "879d67d5e71d9095c9060302c6bfb5db31d287d4b69c8982692b436a650b856d",
     "5d5796c691bd98450bbc4f256c03b5e9b787af6e60d58e816ecc7f0d444ae66c"),
    (B, C, "c", C_STEM,
     "f6266809ac26ff75f44d5f23cab8c15ae338e6185b88b69ec85bd83dfb7c0b8a",
     "1e404dc0f374ffa2d7b1e2f21e8d468014af9ab132f044e90e9a49a99d728c81"),
    (C, END, "asm", None,
     "5a2ed4b2bba700248a88e1fa93473d1ae101a691b936b610bd40bd02625e7106",
     "64f5b4cfc95ac0be408ab21423132e26873077a8dda3834a4053b89ead185444"),
)

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def _source() -> str:
    raw = C_PATH.read_bytes()
    if sha(raw) != C_SHA256 or b"GLOBAL_ASM" in raw or b"__asm" in raw:
        raise ValueError("Unreviewed original-ID0 camera C source")
    return raw.decode("utf-8")

def load_fixture() -> dict:
    original = parent.load_fixture()
    chunks = original["chunks"]
    matches = [(i, c) for i, c in enumerate(chunks)
               if c["rom_start"] == A and c["rom_end"] == END]
    if len(matches) != 1:
        raise ValueError("Unique original camera ASM owner not found")
    index, owner = matches[0]
    if owner["kind"] != "asm" or owner.get("name") is not None or (
        owner["original_sha256"] != OLD_PARENT_SHA256 or owner["size"] != END-A
    ):
        raise ValueError("Previously verified 179-file11 owner has changed")
    result = copy.deepcopy(original)
    source = _source()
    replacements = []
    for start, end, kind, name, original_sha, object_sha in NEW_CHUNKS:
        c = {"rom_start": start, "rom_end": end, "kind": kind, "name": name,
             "size": end-start, "original_sha256": original_sha,
             "trimmed_obj_sha256": object_sha}
        if kind == "c":
            c.update(source=source, source_sha256=C_SHA256,
                     functions=[{"name": FUNC_NAME, "off": B,
                                 "vma": 0x801F97D4, "size": 136}])
        replacements.append(c)
    result["chunks"][index:index+1] = replacements
    result["format"] = "goemon-file11-180-camera-reset-source-fixture-v1"
    result["total_represented_functions"] = 180
    result["unique_new_C"] = 28
    result["unique_new_C_bytes"] = 1044
    result["new_covered_functions_beyond_existing_50"] = 130
    result["all_C_text_bytes"] = 5320
    result["production_promotion_count"] = 0
    return result

def entries() -> list[dict]:
    return [{"name": f["name"], "rom_offset": f["off"],
             "vma": f["vma"], "size": f["size"]}
            for c in load_fixture()["chunks"] if c["kind"] == "c"
            for f in c["functions"]]

def reviewed_plan(manifest: dict, original_rom: bytes | None = None) -> dict:
    if manifest.get("overlay_file11_stage") != {"format": STAGE_FORMAT}:
        raise ValueError("Only an explicitly opted-in 180-file11 manifest is accepted")
    prior_manifest = copy.deepcopy(manifest)
    prior_manifest["overlay_file11_stage"] = {"format": parent.STAGE_FORMAT}
    old_plan = parent.reviewed_plan(prior_manifest, original_rom)
    current = load_fixture()
    old = parent.load_fixture()["chunks"]
    new = current["chunks"]
    if (len(old) != 126 or len(new) != 128 or
        len(entries()) != 180 or current["all_C_text_bytes"] != 5320 or
        sum(c["kind"] == "c" for c in new) != 77 or
        sum(c["kind"] == "asm" for c in new) != 51):
        raise ValueError("180-function camera stage extent changed")
    original_functions = {(f["name"], f["rom_offset"], f["size"])
                          for f in parent.entries()}
    actual_functions = {(f["name"], f["rom_offset"], f["size"])
                        for f in entries()}
    if (not original_functions.issubset(actual_functions) or
        actual_functions - original_functions != {(FUNC_NAME, B, 136)}):
        raise ValueError("Duplicate, missing or displaced production C function")
    if new[0]["rom_start"] != START or new[-1]["rom_end"] != parent.END:
        raise ValueError("Overlay boundary changed")
    if any(x["rom_end"] != y["rom_start"] for x, y in zip(new, new[1:])):
        raise ValueError("Overlapping or missing camera overlay text")
    old_unchanged = [c for c in old if not
                     (c["rom_start"] == A and c["rom_end"] == END)]
    new_unchanged = [c for c in new if not (A <= c["rom_start"] < END)]
    if new_unchanged != old_unchanged:
        raise ValueError("Existing production C/ASM ownership changed")
    if original_rom is not None:
        if (len(original_rom) != 33554432 or
            hashlib.sha1(original_rom).hexdigest() != overlay_file11.ROM_SHA1):
            raise ValueError("Not the authenticated complete original-USA ROM")
        for c in new:
            if sha(original_rom[c["rom_start"]:c["rom_end"]]) != c["original_sha256"]:
                raise ValueError("Wrong original 180-file11 ROM slice")
    old_plan.update(
        ordered_segments=[(c["rom_start"], c["kind"], c["name"]) for c in new],
        c_sources={c["name"]: c["source"] for c in new if c["kind"] == "c"},
        chunks=128, c_units=77, asm_slices=51,
        file11_c_total=180, file11_c_instruction_bytes=5320,
        prospective_usa_c=343,
    )
    return old_plan

def stage_splat(original: str, plan: dict) -> str:
    overlay_file11.stage_config(original)
    matches = list(re.finditer(r"(?m)^  - name: (\S+)\s*$", original))
    names = [m.group(1) for m in matches]
    pos = names.index("file_11")
    i, j = matches[pos].start(), matches[pos+1].start()
    chunk = original[i:j]
    if chunk.count(parent.OLD_SPLAT) != 1 or len(plan["ordered_segments"]) != 128:
        raise ValueError("Pristine overlay/Splat layout differs")
    inserted = "\n".join(
        f"    - [0x{offset:X}, {kind}" +
        (f", {stem}" if kind == "c" else "") + "]"
        for offset, kind, stem in plan["ordered_segments"]
    ) + "\n    - [0x5B8500, data]"
    return original[:i] + chunk.replace(parent.OLD_SPLAT, inserted, 1) + original[j:]

def source_payloads(checkout: Path, plan: dict):
    result = []
    for stem, source in plan["c_sources"].items():
        if not re.fullmatch("[a-z][a-z0-9_]*", stem):
            raise ValueError("Unsafe C filename")
        path = Path(checkout) / "src" / (stem + ".c")
        if path.exists():
            raise FileExistsError("Existing C source in verification checkout: " + str(path))
        result.append((path, source))
    if len(result) != 77 or len({p for p, _ in result}) != 77:
        raise ValueError("Wrong C source count")
    return result

def source_objects():
    result = []
    for chunk in load_fixture()["chunks"]:
        if chunk["kind"] == "c":
            path = Path("build/usa/src") / (chunk["name"] + ".c.o")
        else:
            path = Path("build/usa/asm/usa") / (f"{chunk['rom_start']:X}.s.o")
        result.append((path, chunk["size"], chunk))
    if len(result) != 128:
        raise ValueError("Wrong object count")
    return result

def object_targets():
    return [p.as_posix() for p, _, _ in source_objects()]

def normalize_added_nop_alias(checkout: Path):
    return parent.normalize_added_nop_alias(checkout)

def _allowed_old_nop(chunk: dict) -> bool:
    return chunk["kind"] == "asm" and chunk["rom_start"] in parent.LEGACY_NOP_ALIAS_ASM_OFFSETS

def prepare_objects(checkout: Path) -> dict:
    checkout = Path(checkout)
    updated = []
    for path, size, chunk in source_objects():
        raw = (checkout / path).read_bytes()
        trimmed = trim_text_object(raw, size)
        if sha(trimmed) != chunk["trimmed_obj_sha256"] and not _allowed_old_nop(chunk):
            raise ValueError("180-file11 original native object differs: " + path.as_posix())
        updated.append((checkout / path, trimmed))
    script = checkout / ".splat/usa/mnsg.ld"
    text = script.read_text(encoding="utf-8")
    if text.count(parent.OLD_LINKER) != 1:
        raise ValueError("Missing original file11 linker alignment")
    for path, raw in updated:
        path.write_bytes(raw)
    script.write_text(text.replace(parent.OLD_LINKER, parent.NEW_LINKER, 1), encoding="utf-8")
    return {"format": "goemon-file11-180-original-object-layout-v1",
            "objects_original_address_exact": 128,
            "original_source_C_objects": 77, "original_source_ASM_objects": 51,
            "expected_file11_semantic_relocations": 8825}

def verify_linked(checkout: Path, expected_rom: bytes, original_elf: Path) -> dict:
    c = Path(checkout)
    image = (c / "build/usa/mnsg.z64").read_bytes()
    if len(expected_rom) != 33554432 or image != expected_rom or (
        hashlib.sha1(image).hexdigest() != overlay_file11.ROM_SHA1
    ):
        raise ValueError("Full 343-C USA ROM does not match the exact original")
    before = read_relocations(Path(original_elf))
    after = read_relocations(c / "build/usa/mnsg.elf")
    if len(before) != 8825 or len(after) != 8825 or Counter(before) != Counter(after):
        raise ValueError("File11 8,825 semantic relocations differ")
    symbols = read_symbols(c / "build/usa/mnsg.elf")
    for function in entries():
        if symbols.get(function["name"]) != (function["vma"], function["size"]):
            raise ValueError("Original linked FUNC identity differs: " + function["name"])
    mapping = (c / "build/usa/mnsg.map").read_text(encoding="utf-8")
    for path, size, chunk in source_objects():
        vma = overlay_file11.VMA_START + chunk["rom_start"] - START
        pattern = (r"(?m)^\s*\.text\s+0x([0-9a-fA-F]+)\s+0x([0-9a-fA-F]+)\s+" +
                   re.escape(path.as_posix()) + r"\s*$")
        matched = re.findall(pattern, mapping)
        if len(matched) != 1 or tuple(int(x, 16) for x in matched[0]) != (vma, size):
            raise ValueError("Original object VMA/size changed: " + path.as_posix())
        if sha((c / path).read_bytes()) != chunk["trimmed_obj_sha256"] and not _allowed_old_nop(chunk):
            raise ValueError("Post-link object identity changed: " + path.as_posix())
        if chunk["kind"] == "c":
            raw = (c / "src" / (chunk["name"] + ".c")).read_bytes()
            if sha(raw) != chunk["source_sha256"]:
                raise ValueError("C source changed after staging: " + chunk["name"])
    return {
        "format": "goemon-file11-180-original-link-v1", "status": "PASS",
        "original_address_matching_c": 180, "file11_C_instruction_bytes": 5320,
        "original_native_object_provenance_checked": 128,
        "original_semantic_file11_relocations": 8825,
        "candidate_semantic_file11_relocations": 8825,
        "complete_rom_bytes_equal": len(image),
        "original_rom_sha1": overlay_file11.ROM_SHA1,
        "full_symbol_inventory": "REQUIRES decomp.inventory after combined G2",
    }
