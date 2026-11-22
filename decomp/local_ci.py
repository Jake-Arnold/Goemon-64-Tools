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
        ("Canonical proof/inventory validation", [sys.executable, "-m", "decomp.skill_context", "--validate"]),
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
    if not quick:
        wide_host = ROOT / 'decomp/research/usa_wide132_promotion_20261118'
        wide_sources = sorted((wide_host/'host_sources').glob('*.c'))
        if len(wide_sources)!=9:
            raise ValueError('Missing nine original-source wide132 host fixtures')
        compiler = shlex.split(os.environ.get('CC', 'cc'))
        steps.extend([
            ('Wide132 actual-source sanitizer build', compiler + [
                '-std=c11','-O1','-g','-Wall','-Wextra','-Werror',
                '-fsanitize=address,undefined','-fno-sanitize-recover=all',
                '-fno-omit-frame-pointer',
                str((wide_host/'test_host132.c').relative_to(ROOT)),
                *[str(f.relative_to(ROOT)) for f in wide_sources],
                '-o',str(host_binary.with_name('wide132-actual-host'))]),
            ('Wide132 actual-source sanitizer test',
             [str(host_binary.with_name('wide132-actual-host'))]),
        ])
    if not quick:
        w109 = ROOT / 'decomp/research/usa_wide109_promotion_20261118'
        sources = sorted((w109/'sources').glob('*.c'))
        if len(sources) != 68:
            raise ValueError('Missing original-source wide109 68 C translation units')
        compiler=shlex.split(os.environ.get('CC','cc'))
        binary=host_binary.with_name('wide109-actual-host')
        steps.extend([
            ('Wide109 actual-source sanitizer build', compiler + [
                '-std=c11','-O1','-g','-Wall','-Wextra','-Werror',
                '-Wno-unused-parameter','-Wno-unused-function',
                '-fsanitize=address,undefined','-fno-sanitize-recover=all',
                '-fno-omit-frame-pointer',
                str((w109/'test_actual109.c').relative_to(ROOT)),
                *[str(f.relative_to(ROOT)) for f in sources],
                '-o',str(binary)]),
            ('Wide109 actual-source sanitizer test',[str(binary)]),
        ])
    if not quick:
        # All 63 newly promoted original source bodies in the resource18 and
        # callback16/21 batches are executed, not copied into test doubles.
        native18=sorted((ROOT/'decomp/research/pending_file18_53_20261118/sources').glob('*.c'))
        callbacks=sorted((ROOT/'decomp/research/pending_callbacks10_20261118/sources').glob('*.c'))
        if len(native18)!=50 or len(callbacks)!=3:
            raise ValueError('Missing authenticated original 53+10 C source units')
        compiler=shlex.split(os.environ.get('CC','cc'))
        binary=host_binary.with_name('file18-and-callbacks-actual-host')
        steps.extend([
            ('New file18/callbacks actual-C sanitizer build',compiler+[
                '-std=c11','-O1','-g','-Wall','-Wextra','-Werror',
                '-Wno-unused-parameter','-Wno-unused-function',
                '-fsanitize=address,undefined','-fno-sanitize-recover=all',
                '-fno-omit-frame-pointer',
                'decomp/research/pending_batch227_20261118/test_actual_file18_callbacks.c',
                *[str(src.relative_to(ROOT)) for src in (native18+callbacks)],
                '-o',str(binary)]),
            ('New file18/callbacks actual-C sanitizer test',[str(binary)]),
        ])
    if not quick:
        tiny = ROOT / 'decomp/research/pending_tiny9_20261119'
        sources=sorted((tiny/'sources').glob('*.c'))
        if len(sources)!=7:
            raise ValueError('Missing seven original-source tiny9 translation units')
        compiler=shlex.split(os.environ.get('CC','cc'))
        binary=host_binary.with_name('tiny9-actual-host')
        steps.extend([
            ('Tiny9 actual-source sanitizer build',compiler+[
                '-std=c11','-O1','-g','-Wall','-Wextra','-Werror',
                '-fsanitize=address,undefined','-fno-sanitize-recover=all',
                '-fno-omit-frame-pointer',
                str((tiny/'test_actual_tiny9.c').relative_to(ROOT)),
                *[str(src.relative_to(ROOT)) for src in sources],
                '-o',str(binary)]),
            ('Tiny9 actual-source sanitizer test',[str(binary)]),
        ])
    if not quick:
        menu = ROOT / 'decomp/research/pending_menu2_20261119'
        sources = sorted((menu/'sources').glob('*.c'))
        if len(sources)!=2:
            raise ValueError('Missing two authenticated original menu-resource C sources')
        compiler = shlex.split(os.environ.get('CC','cc'))
        binary = host_binary.with_name('menu2-actual-host')
        steps.extend([
            ('Menu2 actual-source sanitizer build',compiler+[
                '-std=gnu11','-O1','-g','-Wall','-Wextra','-Werror',
                '-fsanitize=address,undefined','-fno-sanitize-recover=all',
                '-fno-omit-frame-pointer',
                str((menu/'test_actual_menu2.c').relative_to(ROOT)),
                *[str(src.relative_to(ROOT)) for src in sources],
                '-o',str(binary)]),
            ('Menu2 actual-source sanitizer test',[str(binary)]),
        ])
    if not quick:
        archive = ROOT / 'decomp/research/pending_archive22_20261119'
        sources = sorted((archive/'sources').glob('*.c'))
        if len(sources)!=22:
            raise ValueError('Missing 22 original archived exact C source units')
        compiler=shlex.split(os.environ.get('CC','cc'))
        binary=host_binary.with_name('archive22-actual-host')
        steps.extend([
            ('Archive22 actual-source sanitizer build', compiler+[
                '-std=c11','-O1','-g','-Wall','-Wextra','-Werror',
                '-Wno-unused-parameter','-Wno-unused-function',
                '-fsanitize=address,undefined','-fno-sanitize-recover=all',
                '-fno-omit-frame-pointer',
                str((archive/'test_actual_archive22.c').relative_to(ROOT)),
                *[str(f.relative_to(ROOT)) for f in sources],
                '-lm','-o',str(binary)]),
            ('Archive22 actual-source sanitizer test',[str(binary)]),
        ])
    if not quick:
        # Authenticated 33 original USA C sources are run through ASan/UBSan;
        # the native exact original-MIPS match is a separate required gate.
        archive=ROOT/'decomp/research/pending_archive33_20261120'
        sources=sorted((archive/'sources').glob('*.c'))
        if len(sources)!=33:
            raise ValueError('Missing 33 original archive33 native source translation units')
        compiler=shlex.split(os.environ.get('CC','cc'))
        binary=host_binary.with_name('archive33-actual-host')
        steps.extend([
            ('Archive33 actual-source sanitizer build',compiler+[
                '-std=gnu11','-O1','-g','-Wall','-Wextra','-Werror',
                '-Wno-unused-parameter','-Wno-unused-function',
                '-Wno-int-conversion','-Wno-int-to-pointer-cast','-Wno-pointer-to-int-cast',
                '-fsanitize=address,undefined','-fno-sanitize-recover=all',
                '-fno-omit-frame-pointer',
                str((archive/'test_actual_archive33.c').relative_to(ROOT)),
                *[str(f.relative_to(ROOT)) for f in sources],
                '-lm','-o',str(binary)]),
            ('Archive33 actual-source sanitizer test',[str(binary)]),
        ])
    if not quick:
        # Compile all 61 original native-verified C translation units with
        # ASan/UBSan, then execute ten independently safe original bodies.
        sources=sorted((ROOT/'decomp/research/pending_archive61_20261120/sources').glob('archive61_*.c'))
        if len(sources)!=61:
            raise ValueError('Missing the original 61 archive native source files')
        steps.append(('Archive61 actual-original-source sanitizer compile and host cases',[
            sys.executable,'-m','decomp.research.pending_archive61_20261120.test_actual_sources']))
    if not quick:
        # Exercise the one actually surviving checkpoint500 original C source.
        archive=ROOT/'decomp/research/pending_checkpoint500_20261120'
        source=archive/'sources/checkpoint500_000.c'
        if not source.is_file():
            raise ValueError('Missing authenticated checkpoint500 C source')
        compiler=shlex.split(os.environ.get('CC','cc'))
        binary=host_binary.with_name('checkpoint500-original-host')
        steps.extend([
            ('Checkpoint500 actual-original-source sanitizer build', compiler+[
                '-std=gnu11','-O1','-g','-Wall','-Wextra','-Werror',
                '-Wno-unused-parameter','-Wno-unused-function',
                # Original MIPS ABI has 32-bit pointers. The archived C uses a
                # 0x54 pointer field and GCC/64-bit host UBSan incorrectly
                # asserts 8-byte alignment of the base AND field. Keep
                # address/UB sanitizers, but omit host-only alignment check.
                '-fsanitize=address,undefined','-fno-sanitize=alignment',
                '-fno-sanitize-recover=all',
                '-fno-omit-frame-pointer',
                str((archive/'test_actual_checkpoint500.c').relative_to(ROOT)),
                str(source.relative_to(ROOT)),
                '-o',str(binary)]),
            ('Checkpoint500 original-source 1000-case host sanitizer test',[str(binary)]),
        ])
    if not quick:
        # All five re-discovered, native-matching C implementations execute as
        # authentic compiled source, not host test doubles.
        rediscovery = ROOT / 'decomp/research/pending_rediscovery5_20261120'
        sources = sorted((rediscovery / 'sources').glob('rediscovery5_*.c'))
        if len(sources) != 5:
            raise ValueError('Missing five reviewed rediscovery5 original C units')
        compiler = shlex.split(os.environ.get('CC', 'cc'))
        binary = host_binary.with_name('rediscovery5-original-host')
        steps.extend([
            ('Rediscovery5 authentic original-C sanitizer build', compiler + [
                '-std=gnu11', '-O1', '-g', '-Wall', '-Wextra', '-Werror',
                '-Wno-unused-parameter', '-Wno-unused-function',
                '-fsanitize=address,undefined', '-fno-sanitize-recover=all',
                '-fno-omit-frame-pointer',
                str((rediscovery / 'test_actual_rediscovery5.c').relative_to(ROOT)),
                *[str(src.relative_to(ROOT)) for src in sources],
                '-o', str(binary)]),
            ('Rediscovery5 original-C 5000-case sanitizer test', [str(binary)]),
        ])
    if not quick:
        # Authentic original C source, not an ABI/model stub: ASan/UBSan host
        # coverage of a safe field-update function over 1,000 input cases.
        root=ROOT/'decomp/research/pending_native100_20261120'
        source=ROOT/'decomp/research/pending_native49_20261120/sources/native49_000.c'
        if not source.is_file():
            raise ValueError('Missing original native100 C source')
        compiler=shlex.split(os.environ.get('CC','cc'))
        binary=host_binary.with_name('native100-original-host')
        steps.extend([
          ('Native100 original-C host sanitizer build',compiler+[
              '-std=gnu11','-O1','-g','-Wall','-Wextra','-Werror',
              '-fsanitize=address,undefined','-fno-sanitize-recover=all',
              '-fno-omit-frame-pointer',
              str((root/'test_host_native100.c').relative_to(ROOT)),
              str(source.relative_to(ROOT)),
              '-o',str(binary)]),
          ('Native100 original-C 1000-case host sanitizer test',[str(binary)])
        ])
    if not quick:
        isolated_tests=ROOT/'decomp/research/pending_isolated233_20261120/tests'
        if not (isolated_tests/'test_usa_92f0_a18c_aae8.c').is_file():
            raise ValueError('Missing isolated USA 92F0 actual-source host fixture')
        compiler=shlex.split(os.environ.get('CC','cc'))
        binary=host_binary.with_name('usa-92f0-a18c-aae8-host')
        steps.extend([
            ('USA 92F0 A18C/AAE8/AB30/108BC actual-source sanitizer build',compiler+[
                '-std=gnu11','-O1','-g','-Wall','-Wextra','-Werror',
                # The original MIPS32 C casts a symbol pointer to unsigned;
                # the host fixture intentionally checks its low 32-bit value.
                '-Wno-pointer-to-int-cast',
                '-fsanitize=address,undefined','-fno-sanitize-recover=all',
                '-fno-omit-frame-pointer','-I'+str(isolated_tests.relative_to(ROOT)),
                str((isolated_tests/'test_usa_92f0_a18c_aae8.c').relative_to(ROOT)),
                '-o',str(binary)]),
            ('USA 92F0 A18C/AAE8/AB30/108BC actual-source sanitizer test',[str(binary)]),
        ])
    # The resumable queue and read-only C-Right comparator belong to the
    # same ROM-free acceptance gate as the existing Python/ledger checks.
    # Append them, preserving existing native-host fixture ordering.
    steps.extend([
        ("Resumable task registry validation", [sys.executable, "-m", "decomp.task_registry", "validate"]),
        ("C-Right live-trace comparator tests", [sys.executable, "-m", "unittest", "discover",
         "-s", "decomp/tasks/cright_live_trace", "-p", "test_comparator.py", "-q"]),
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
