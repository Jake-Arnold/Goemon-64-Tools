"""ROM-free local CI for Goemon decomp. No GitHub Actions or private ROMs required."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def build_steps(host_binary: Path, *, quick: bool = False):
    """Return the fail-fast commands; all run from the repository root."""
    steps = [
        ("Decomp Python tests", [sys.executable, "-m", "unittest", "discover", "-s", "decomp", "-p", "test_*.py", "-q"]),
        ("Verifier / ledger Python tests", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_decomp_*.py", "-q"]),
        ("Task and evidence validation", [sys.executable, "-m", "decomp.skill_context", "--validate"]),
    ]
    if not quick:
        compiler = shlex.split(os.environ.get("CC", "cc"))
        if not compiler:
            raise ValueError("CC must name a C compiler")
        steps.extend([
            ("Display emitter host sanitizer build", compiler + [
                "-std=c11", "-O1", "-g", "-Wall", "-Wextra", "-Werror",
                "-fsanitize=address,undefined", "-fno-sanitize-recover=all",
                "-fno-omit-frame-pointer", "-Idecomp",
                "decomp/test_vm_display_emitters.c", "-o", str(host_binary),
            ]),
            ("Display emitter host sanitizer test", [str(host_binary)]),
            ("Native87 actual-source sanitizer build", compiler + [
                "-std=c11", "-O1", "-g", "-Wall", "-Wextra", "-Werror",
                "-Wno-unused-parameter", "-Wno-unused-function",
                "-fsanitize=address,undefined", "-fno-sanitize-recover=all",
                "-fno-omit-frame-pointer",
                "decomp/research/usa_main_overlay_87_20261118/test_actual87.c",
                *[str(path.relative_to(ROOT)) for path in sorted(
                    (ROOT / "decomp/research/usa_main_overlay_87_20261118/sources").glob("*.c"))],
                "-o", str(host_binary.with_name("native87-actual-host")),
            ]),
            ("Native87 actual-source sanitizer test", [str(host_binary.with_name("native87-actual-host"))]),
            ("File27 promoted C host sanitizer build", compiler + [
                "-std=gnu11", "-O1", "-g", "-Wall", "-Wextra", "-Werror",
                "-Wno-unused-parameter", "-Wno-unused-function",
                "-fsanitize=address,undefined", "-fno-sanitize-recover=all",
                "-fno-omit-frame-pointer",
                "decomp/research/file27_adjacent21_20261117/test_adjacent27.c",
                *[str(f.relative_to(ROOT)) for f in sorted(
                    (ROOT / "decomp/research/file27_promotion_20261118/sources").glob("*.c"))],
                "-o", str(host_binary.with_name("file27-promoted-host")),
            ]),
            ("File27 promoted C host sanitizer test", [str(host_binary.with_name("file27-promoted-host"))]),
        ])
    return steps


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quick", action="store_true", help="Run the Python gates only (skip the C sanitizer fixture)")
    args = parser.parse_args(argv)
    with tempfile.TemporaryDirectory(prefix="goemon-local-ci-") as tmp:
        try:
            steps = build_steps(Path(tmp) / "vm-display-host", quick=args.quick)
        except ValueError as exc:
            parser.error(str(exc))
        environment = os.environ.copy()
        environment.setdefault("ASAN_OPTIONS", "detect_leaks=1:halt_on_error=1")
        environment.setdefault("UBSAN_OPTIONS", "halt_on_error=1")
        for label, command in steps:
            print(f"[local-ci] {label}", flush=True)
            try:
                result = subprocess.run(command, cwd=ROOT, env=environment, check=False)
            except OSError as exc:
                print(f"[local-ci] ERROR: {exc}", file=sys.stderr)
                return 127
            if result.returncode:
                print(f"[local-ci] FAIL: {label} (exit {result.returncode})", file=sys.stderr)
                return result.returncode if result.returncode > 0 else 1
    print("[local-ci] PASS: all selected ROM-free checks. Not a native IDO or full-ROM G2 proof.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
