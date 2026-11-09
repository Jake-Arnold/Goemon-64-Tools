"""Activate extracted, pinned MIPS binutils without loading bundled glibc.

The archived cross-binutils root has its own ``libc.so.6`` alongside Binutils
DSOs. Adding that entire directory to LD_LIBRARY_PATH can crash the linker on
a different Linux host. This tool makes a small private symlink directory with
only the needed Binutils DSOs and verifies assembler/linker/objcopy readiness.
It does not install software or modify a repository checkout.

Usage (execute shell exports in the caller's shell):
  eval "$(python decomp/prepare_mips_binutils.py --root /path/to/extracted \
         --runtime-dir /tmp/goemon-binutils-libs)"
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import shlex
import subprocess

# Do not add system C runtime, libstdc++, libz or whole extracted /usr/lib.
# The selected DSOs are supplied by the pinned GNU MIPS archive itself.
BINUTILS_LIBRARIES = (
    "libbfd-2.45.90-mips.20260125.so",
    "libopcodes-2.45.90-mips.20260125.so",
    "libctf-mips.so.0",
    "libctf-nobfd-mips.so.0",
    "libsframe.so.3",
)
TOOLS = ("as", "ld", "objcopy", "objdump")
VERSION = "2.45.90.20260125"


def configure(root: Path, runtime: Path) -> dict[str, str]:
    root = root.resolve(strict=True)
    bin_dir = root / "usr/bin"
    library_dir = root / "usr/lib/x86_64-linux-gnu"
    if not bin_dir.is_dir() or not library_dir.is_dir():
        raise ValueError("Extracted archive must contain usr/bin and usr/lib/x86_64-linux-gnu")
    for tool in TOOLS:
        binary = bin_dir / f"mips-linux-gnu-{tool}"
        if not binary.is_file() or not os.access(binary, os.X_OK):
            raise ValueError(f"Missing executable {binary}")
    for name in BINUTILS_LIBRARIES:
        if not (library_dir / name).is_file():
            raise ValueError(f"Missing pinned Binutils DSO {name}")
    runtime.mkdir(parents=True, exist_ok=True)
    for name in BINUTILS_LIBRARIES:
        link = runtime / name
        target = (library_dir / name).resolve(strict=True)
        if link.is_symlink():
            if link.resolve() != target:
                raise ValueError(f"Refusing to replace preexisting different symlink {link}")
        elif link.exists():
            raise ValueError(f"Refusing to overwrite existing file {link}")
        else:
            link.symlink_to(target)
    # Never let a copied glibc or arbitrary library into the curated directory.
    names = {p.name for p in runtime.iterdir()}
    if names != set(BINUTILS_LIBRARIES):
        raise ValueError("Runtime DSO directory must contain only pinned Binutils libraries")
    env = dict(os.environ)
    env["PATH"] = str(bin_dir) + os.pathsep + env.get("PATH", "")
    env["LD_LIBRARY_PATH"] = str(runtime.resolve())
    for tool in TOOLS:
        exe = bin_dir / f"mips-linux-gnu-{tool}"
        result = subprocess.run([str(exe), "--version"], env=env, capture_output=True,
                                text=True, timeout=15, check=False)
        if result.returncode or VERSION not in result.stdout:
            raise RuntimeError(f"Pinned MIPS {tool} failed version smoke test: {result.returncode}, {result.stderr[:200]}")
    return env


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--runtime-dir", type=Path, required=True)
    args = parser.parse_args()
    env = configure(args.root, args.runtime_dir)
    print("export PATH=" + shlex.quote(env["PATH"]))
    print("export LD_LIBRARY_PATH=" + shlex.quote(env["LD_LIBRARY_PATH"]))


if __name__ == "__main__":
    main()
