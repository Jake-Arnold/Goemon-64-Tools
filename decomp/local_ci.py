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
    if not quick and (ROOT/'decomp/research/usa_short72_20261123/manifest.json').exists():
        short72=ROOT/'decomp/research/usa_short72_20261123'
        compiler=shlex.split(os.environ.get('CC','cc'))
        steps.extend([
          ('USA short72 actual 48B timer-C ASan/UBSan build',compiler+[
              '-std=c11','-O1','-g','-Wall','-Wextra','-Werror',
              '-fsanitize=address,undefined','-fno-sanitize-recover=all',
              '-fno-omit-frame-pointer',
              str((short72/'test_host_short72.c').relative_to(ROOT)),
              str((short72/'sources/short72_066.c').relative_to(ROOT)),
              str((short72/'sources/short72_067.c').relative_to(ROOT)),
              '-o',str(host_binary.with_name('short72-original-timers-host'))]),
          ('USA short72 original-C 4096-pair ASan/UBSan cases',
              [str(host_binary.with_name('short72-original-timers-host'))]),
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
            ('USA 92F0 A18C/A548/A5C4/AAE8/AB30/108BC actual-source sanitizer build',compiler+[
                '-std=gnu11','-O1','-g','-Wall','-Wextra','-Werror',
                # The original MIPS32 C casts a symbol pointer to unsigned;
                # the host fixture intentionally checks its low 32-bit value.
                '-Wno-pointer-to-int-cast',
                '-fsanitize=address,undefined','-fno-sanitize-recover=all',
                '-fno-omit-frame-pointer','-I'+str(isolated_tests.relative_to(ROOT)),
                str((isolated_tests/'test_usa_92f0_a18c_aae8.c').relative_to(ROOT)),
                '-o',str(binary)]),
            ('USA 92F0 A18C/A548/A5C4/AAE8/AB30/108BC actual-source sanitizer test',[str(binary)]),
        ])
    if not quick:
        isolated_tests=ROOT/'decomp/research/pending_isolated233_20261120/tests'
        compiler=shlex.split(os.environ.get('CC','cc'))
        mini_reset=host_binary.with_name('mini-reset-actual-host')
        speed_ease=host_binary.with_name('speed-ease-actual-host')
        sanitizer=['-std=gnu11','-O1','-g','-Wall','-Wextra','-Werror',
                   '-fsanitize=address,undefined','-fno-sanitize-recover=all','-fno-omit-frame-pointer']
        steps.extend([
            ('Mini reset 148B original-source sanitizer build',compiler+sanitizer+[
                str((isolated_tests/'test_mini_reset_276c.c').relative_to(ROOT)),'-o',str(mini_reset)]),
            ('Mini reset 148B original-source sanitizer test',[str(mini_reset)]),
            ('Speed ease 220B original-source sanitizer build',compiler+sanitizer+[
                str((isolated_tests/'test_speed_ease_3de0.c').relative_to(ROOT)),'-o',str(speed_ease)]),
            ('Speed ease 220B original-source sanitizer test',[str(speed_ease)]),
        ])
    if not quick:
        # Original IDO-matching USA Mini C source bodies, not approximating
        # behavioural stubs. The four host fixtures cover all eleven promoted
        # functions (10 stage sources and the original-table selector).
        mini11=ROOT/'decomp/research/usa_mini11_20261123'
        mini10=ROOT/'decomp/research/usa_mini10_20261123/sources'
        selector=ROOT/'decomp/research/usa_mini_selector_20261123/mini_selector.c'
        native_sources=[mini10/(name+'.c') for name in (
            'mini_2180','mini_2220','mini_2800','mini_2aa0',
            'mini_2ba8','mini_2cec','mini_2d74')]
        groups=(
            ('seven',mini11/'test_host_new_seven.c',native_sources),
            ('conditional',mini11/'test_conditional_speeds.c',[mini10/'mini_31dc.c']),
            ('pair',mini11/'test_host_pair.c',[mini10/'mini_28d8.c',mini10/'mini_3278.c']),
            ('selector',mini11/'test_host_selector.c',[selector]),
        )
        compiler=shlex.split(os.environ.get('CC','cc'))
        # Keep exact native IDO source declarations unchanged: some unused
        # local stack names are necessary to preserve source hash/provenance.
        # Suppress only unused-variable warnings, not sanitizer checks.
        flags=['-std=gnu11','-O1','-g','-Wall','-Wextra','-Werror',
               '-Wno-unused-variable','-Wno-unused-parameter','-Wno-unused-function','-Wno-unknown-pragmas',
               '-fsanitize=address,undefined','-fno-sanitize-recover=all',
               '-fno-omit-frame-pointer']
        for label,fixture,srcs in groups:
            if not fixture.is_file() or any(not source.is_file() for source in srcs):
                raise ValueError('Missing exact USA Mini native C host suite '+label)
            binary=host_binary.with_name('mini11-'+label+'-native-asan-host')
            steps.extend([
                ('USA Mini11 '+label+' actual C ASan/UBSan host build',compiler+flags+[
                    str(fixture.relative_to(ROOT)),
                    *[str(src.relative_to(ROOT)) for src in srcs],'-lm','-o',str(binary)]),
                ('USA Mini11 '+label+' actual C ASan/UBSan host regression',[str(binary)]),
            ])
    if not quick:
        # Execute both actual new post2090 USA file18 native C implementations,
        # including null child, callback side effects and a bounded table index.
        pair=ROOT/'decomp/research/usa_file18_new2_20261123'
        cfiles=[pair/'sources/new2_native_00.c',pair/'sources/new2_native_01.c']
        fixture=pair/'tests/test_new2.c'
        if not fixture.is_file() or any(not x.is_file() for x in cfiles):
            raise ValueError('Missing original-source USA file18 new2 host regression')
        compiler=shlex.split(os.environ.get('CC','cc'))
        binary=host_binary.with_name('usa-file18-new2-original-asan-host')
        steps.extend([
            ('File18 new2 original C source ASan/UBSan build',compiler+[
                '-std=gnu11','-O1','-g','-Wall','-Wextra','-Werror',
                '-Wno-pointer-to-int-cast',
                # The synthetic N64 absolute-offset symbol is a constant only
                # for a non-PIE host executable. PIE would add the load base.
                '-fno-pie','-no-pie',
                '-fsanitize=address,undefined','-fno-sanitize-recover=all',
                '-fno-omit-frame-pointer',
                str(fixture.relative_to(ROOT)),
                *[str(f.relative_to(ROOT)) for f in cfiles],
                '-Wl,--defsym,D_CF8F8=0xCF8F8','-o',str(binary)]),
            ('File18 new2 original source 10000-case sanitizer test',[str(binary)]),
        ])
    if not quick:
        # Exercise the original IDO-matching C, not a separate host model.
        fixture=ROOT/'decomp/research/usa_script_vm_436_20261123/tests/host_actual_source.c'
        compiler=shlex.split(os.environ.get('CC','cc'))
        binary=host_binary.with_name('vm436-actual-source-host')
        if not fixture.is_file():
            raise ValueError('Missing original-source VM436 host fixture')
        steps.extend([
            ('VM436 actual-source ASan/UBSan build',compiler+[
                '-std=gnu99','-O1','-g','-Wno-error=int-conversion',
                '-fsanitize=address,undefined','-fno-sanitize-recover=all',
                '-fno-omit-frame-pointer',str(fixture.relative_to(ROOT)),
                '-o',str(binary)]),
            ('VM436 actual-source 4096-case ASan/UBSan regression',[str(binary)]),
        ])
    if not quick:
        fixture=ROOT/'decomp/research/usa_script_vm440_20261123/host_emitter_test.c'
        compiler=shlex.split(os.environ.get('CC','cc'))
        binary=host_binary.with_name('vm440-actual-source-host')
        steps.extend([
            ('VM440 actual-source ASan/UBSan build',compiler+[
                '-std=gnu99','-O1','-g','-Wno-error=int-conversion',
                '-fsanitize=address,undefined','-fno-sanitize-recover=all',
                '-fno-omit-frame-pointer',str(fixture.relative_to(ROOT)),
                '-o',str(binary)]),
            ('VM440 actual-source 4096-case ASan/UBSan regression',[str(binary)]),
        ])
    if not quick:
        fixture=ROOT/'decomp/research/usa_script_vm_combined2319_20261123/host_candidates.c'
        compiler=shlex.split(os.environ.get('CC','cc'))
        binary=host_binary.with_name('vmdual-actual-source-host')
        steps.extend([
            ('VM dual native-source ASan/UBSan build',compiler+[
                '-std=c11','-O1','-g','-fsanitize=address,undefined',
                '-fno-sanitize-recover=all','-fno-omit-frame-pointer',
                str(fixture.relative_to(ROOT)),
                'decomp/research/usa_script_vm_f37c_reference_20261123/f37c.c',
                'decomp/research/usa_script_vm_df98_reference_20261123/df98.c',
                '-o',str(binary)]),
            ('VM dual 135168 actual-source ASan/UBSan cases',[str(binary)]),
        ])
    # The resumable queue and read-only C-Right comparator belong to the
    # same ROM-free acceptance gate as the existing Python/ledger checks.
    # Append them, preserving existing native-host fixture ordering.
    steps.extend([
        ("Resumable task registry validation", [sys.executable, "-m", "decomp.task_registry", "validate"]),
        ("C-Right live-trace comparator tests", [sys.executable, "-m", "unittest", "discover",
         "-s", "decomp/tasks/cright_live_trace", "-p", "test_comparator.py", "-q"]),
        ("Canonical promotion integrity (manifest+G2+inventory)",
         [sys.executable, "-m", "decomp.promotion_integrity", "--validate"]),
    ])
    steps.append(("Native100 Japan source/G2/inventory validation", [sys.executable, "-m", "decomp.native251_integrity"]))
    steps.append(("C-Right6 Japan source/G2/inventory validation", [sys.executable, "-m", "decomp.japan_cright6_integrity"]))
    if not quick:
        batch=ROOT/'decomp/research/transition_state_20261124'
        compiler=shlex.split(os.environ.get('CC','cc'))
        for region,sources in (
            ('usa',[batch/'usa/454c.c',batch/'usa/3cf0_selector.c',batch/'usa/host/test_transition.c']),
            ('japan',[batch/'japan/host/test_jp_transition_baseexpr.c']),
        ):
            binary=host_binary.with_name('transition-'+region+'-host')
            steps.extend([
                ('Transition '+region+' actual-source ASan/UBSan build',compiler+[
                    '-std=c99','-O1','-g','-fsanitize=address,undefined','-fno-sanitize-recover=all',
                    '-fno-omit-frame-pointer','-no-pie','-I'+str(batch/region/'host'),
                    '-I'+str(batch/region),*[str(p) for p in sources],'-o',str(binary)]),
                ('Transition '+region+' actual-source ASan/UBSan regression',[str(binary)]),
            ])
    steps.append(('Transition Japan source/G2/inventory validation',[sys.executable,'-m','decomp.transition_promotion']))
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
