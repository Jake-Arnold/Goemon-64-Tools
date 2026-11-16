"""Reproducible, fail-closed Japanese rev-0 assembly-only N64 ROM baseline.

Runs against a separate pinned klorfmorf/mnsg checkout. Does not store ROMs.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re

JAPAN_RETAIL_SHA1 = "9843ee979b5f6c80f5eda85df0baed9ae7c4e73b"
JAPAN_EXPANDED_SHA1 = "6f8745fecc3a5e7d4918c7a73353eb0726116ded"
RETAIL_SIZE = 0x1000000
EXPANDED_SIZE = 0x2000000
PINNED_CONFIG = Path("config/japan_0/splat.yaml")
ASM_CONFIG = Path("config/japan_0/splat_asm_only.local.yaml")
REGION_ASM = Path("asm/japan_0")
BSS_FILE = Path("asm/japan_0/data/63F080.bss.s")
BSS_ALIASES = ("func_80214604_5CFB94", "func_80214670_5CFC00")
C_SEGMENT = re.compile(r"(?m)^([ \t]*-\s*\[\s*0x[\da-fA-F]+\s*,\s*)c(\s*,)")
LOCAL_SYMBOL = re.compile(r"\.L[0-9A-Fa-f]+_[0-9A-Fa-f]+")
LOCAL_DEFINITION = re.compile(r"(?m)^[ \t]*(\.L[0-9A-Fa-f]+_[0-9A-Fa-f]+):")


def render_asm_config(original: str, count: int = 189) -> str:
    if "sha1: " + JAPAN_EXPANDED_SHA1 not in original:
        raise ValueError("Wrong or unsupported Japanese Splat revision")
    rendered, changed = C_SEGMENT.subn(r"\1asm\2", original)
    if changed != count:
        raise ValueError(f"Expected {count} Japanese C segments, got {changed}")
    return rendered


def stage_config(root: Path) -> Path:
    prepared = render_asm_config((root / PINNED_CONFIG).read_text(encoding="utf-8"))
    target = root / ASM_CONFIG
    if target.exists() and target.read_text(encoding="utf-8") != prepared:
        raise FileExistsError(f"Refusing to overwrite changed local Splat config: {target}")
    target.write_text(prepared, encoding="utf-8")
    return target


def patch_asm(root: Path, expected_cross: int = 22) -> dict[str, int]:
    asm = root / REGION_ASM
    if not (asm / "main_1050.s").is_file():
        raise FileNotFoundError("Japanese assembly-only Splat split has not been run")
    files = sorted(asm.rglob("*.s"))
    contents = {f: f.read_text(encoding="utf-8") for f in files}
    definitions: dict[str, set[Path]] = defaultdict(set)
    occurrences: dict[str, set[Path]] = defaultdict(set)
    for path, body in contents.items():
        for name in set(LOCAL_SYMBOL.findall(body)):
            occurrences[name].add(path)
        for name in set(LOCAL_DEFINITION.findall(body)):
            definitions[name].add(path)
    cross = {name: paths for name, paths in definitions.items() if occurrences[name] - paths}
    if len(cross) != expected_cross:
        raise ValueError(f"Expected {expected_cross} cross-object .L symbols, got {len(cross)}")
    if any(len(paths) != 1 for paths in cross.values()):
        raise ValueError("Ambiguous cross-object label definition")
    promoted = 0
    for name, paths in sorted(cross.items()):
        path = next(iter(paths))
        body = contents[path]
        declaration = f".globl {name}"
        if declaration in body:
            continue
        pattern = re.compile(r"(?m)^([ \t]*)(" + re.escape(name) + r":)")
        body, count = pattern.subn(lambda m: m[1] + declaration + "\n" + m[0], body)
        if count != 1:
            raise ValueError(f"Missing unique definition for {name} in {path}")
        contents[path] = body
        promoted += 1
    bss_path = root / BSS_FILE
    if bss_path not in contents:
        raise FileNotFoundError(f"Expected Japanese BSS file missing: {bss_path}")
    bss = contents[bss_path]
    aliases = 0
    for name in BSS_ALIASES:
        renamed = "D_JP_BSS_" + name
        if bss.count(name) == 2 and renamed not in bss:
            bss = bss.replace(name, renamed)
            aliases += 1
        elif bss.count(renamed) == 2 and bss.count(name) == 2:
            pass
        else:
            raise ValueError(f"Unexpected BSS alias state for {name}")
    contents[bss_path] = bss
    for path, body in contents.items():
        if path.read_text(encoding="utf-8") != body:
            path.write_text(body, encoding="utf-8")
    return {"cross_object_labels": len(cross), "new_global_labels": promoted,
            "renamed_bss_symbols": aliases}


def _image(path: Path, size: int, expected_sha: str) -> bytes:
    data = path.read_bytes()
    actual = hashlib.sha1(data).hexdigest()
    if len(data) != size or actual != expected_sha:
        raise ValueError(f"{path}: image mismatch, len={len(data)} SHA1={actual}; "
                         f"expected len={size} SHA1={expected_sha}")
    return data


def verify(root: Path, retail_output: Path) -> dict[str, object]:
    reference_expanded = _image(root / "config/japan_0/baserom.decompressed.z64",
                                EXPANDED_SIZE, JAPAN_EXPANDED_SHA1)
    rebuilt_expanded = _image(root / "build/japan_0/mnsg.z64",
                             EXPANDED_SIZE, JAPAN_EXPANDED_SHA1)
    reference_retail = _image(root / "config/japan_0/baserom.z64",
                              RETAIL_SIZE, JAPAN_RETAIL_SHA1)
    rebuilt_retail = _image(retail_output, RETAIL_SIZE, JAPAN_RETAIL_SHA1)
    if reference_expanded != rebuilt_expanded or reference_retail != rebuilt_retail:
        raise ValueError("Byte-level mismatch despite equal hashes")
    return {"region":"japan_0",
            "expanded":{"size":EXPANDED_SIZE,"sha1":JAPAN_EXPANDED_SHA1,
                        "different_bytes":0,"status":"PASS"},
            "retail":{"size":RETAIL_SIZE,"sha1":JAPAN_RETAIL_SHA1,
                      "different_bytes":0,"status":"PASS"},
            "method":"assembly-only; no matching-C promotions implied"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for op in ("stage-config", "patch-asm", "verify"):
        cmd = sub.add_parser(op)
        cmd.add_argument("checkout", type=Path)
        if op == "verify":
            cmd.add_argument("--retail-output", type=Path, required=True)
            cmd.add_argument("--report", type=Path)
    args = parser.parse_args(argv)
    root = args.checkout.resolve(strict=True)
    if args.command == "stage-config":
        print(stage_config(root))
    elif args.command == "patch-asm":
        print(json.dumps(patch_asm(root), indent=2))
    else:
        result = verify(root, args.retail_output)
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
