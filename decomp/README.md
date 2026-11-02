# Matching C reconstruction track

This directory contains reconstructed C and repeatable matching evidence. It is
separate from the Python companion, autosplitter and existing portable C core.
No game assets, ROMs, generated assembly, object files or saves are included.

Current verified total: **15 functions / 1,076 function bytes across two units**.
The combined baseline/C-replacement whole-ROM match is recorded in
[combined result metadata](results/combined.json).

## System initialization and byte-memory unit

`system_memory.c` replaces ROM `0x4D70..0x4E40` with three matching functions:
system initialization, byte zeroing and forward byte copying. It uses the pinned
upstream `SYS_W` type and preserves the system-buffer size `0xCF908`, global
system-pointer assignment, loading-byte reset and initial renderer-field values.

The byte helpers support nonnegative lengths and retain original forward-copy
behavior; they are **not memmove** and provide no general overlap/negative-length
safety. Zero-length operations make no accesses. The host test checks length 0,
1 and other boundaries, guards, source preservation, same/overlapping pointers,
and initialization against an opaque synthetic system layout with checked offsets.
No system initialization was executed against live game RAM.

## First verified unit

`event_flags.c` replaces upstream assembly unit ROM `0x249F0..0x24D60`:

- **12 functions / 876 function bytes**: set, clear, masked test and 100-byte reset
  operations for each of three flag banks. The unit also includes alignment.
- Additional banks begin at guest `0x80168E90` and `0x80168EF8`; their complete
  gameplay lifecycle/meaning has not been established. The known persistent
  event bank starts at `0x8015C608`.
- Test functions return the **mask**, not a normalized boolean. Set operations
  are idempotent ORs; clear operations retain unrelated bits. Signed division,
  byte casts and shift narrowing are preserved for instruction matching.
- These engine routines are unchecked. Host semantic tests cover the 800 valid
  primary-field bit IDs for each bank, not negative/arbitrary IDs or a new public
  memory-edit API. No companion controls are wired to this code.

The full upstream baseline rebuild and the candidate with this C unit both
produce **the same complete 32 MiB decompressed ROM**:

```text
SHA-1: 6ea0ed71032ce08fc2745f412d84936382197494
```

All 12 linked function ranges and guest addresses match; their assembly-placeholder
markers are absent from the candidate ELF. The C object is present in the link
map. [Observed result metadata](results/event_flags.json) includes source hashes,
tool versions, whole-image identity and per-function matching hashes. It is local
build evidence, not independent third-party verification or an upstream merge.

## Provenance and scope

Pinned [mnsg](https://github.com/klorfmorf/mnsg/tree/7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee)
is the upstream layout/build baseline. Its supplied IDO 5.3 compiler and canonical
Makefile flags are retained. Function/global names are the upstream disassembler's
address-derived labels, not recovered original Nintendo/Konami source names.

The initial draft was assisted by upstream-pinned
[m2c](https://github.com/matt-kempster/m2c/tree/a21c1dcd7255b176c032bb932f521846e98d4372),
then reviewed, typed and adjusted against original instruction output. Draft
decompiler output is not itself counted as matching. Existing mn64rando annotations
and our earlier flag traces inform interpretation; they do not replace compiler
comparison. No third-party code/label dictionary is bundled by this directory.

This is a real matching-C increment, **not full game decompilation**. All untouched
upstream code/data still comes from its existing reconstructed sources, original
assembly or extracted assets. The whole-ROM match proves this replacement did
not change that binary; it does not mean the entire ROM has become C. No new
in-game behavior, playable port or published executable is claimed.

## Rebuild from a fresh local work directory

Run inside Linux/WSL with Git, build-essential/GCC, MIPS binutils and uv installed.
The upstream README documents its toolchain requirements. Tested here with WSL
Ubuntu, uv 0.13.6 and the pinned dependency lock using managed Python 3.12.
The verifier creates fresh baseline and candidate clones; it never resets or
deletes the supplied upstream checkout and refuses to reuse a work directory.

```bash
python3 decomp/verify.py \
  --upstream /path/to/pinned-mnsg-clone \
  --workdir /path/to/NEW-local-build-directory \
  --retail-rom /path/to/your-original-US-ROM.z64 \
  --report practice/diagnostics/NEW-matching-result.json \
  --uv /path/to/uv
```

The upstream clone must be at manifest commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`.
The original retail SHA-1 must be `df8083a54296b8c151917c5333e1c85f014a2a66`.
Keep the work directory and result report local/ignored. Python, tools and locked
dependencies may be downloaded by uv. On Windows invoke this Python script
through WSL; it deliberately refuses native Windows builds. No ROM is uploaded.

`manifest.json` selects the exact assembly/C configuration replacement and function
bounds. The verifier builds baseline first, checks its complete output, then
builds the C replacement, checks symbol identity and per-function bytes, and
requires another whole-ROM match. Reports are exclusively created; failed builds
retain logs/workspaces and record failure without claiming success. The verifier
does not run the game, merge changes or submit anything to upstream maintainers.

## Semantic and verifier checks

```bash
gcc -std=c11 -Wall -Wextra -Werror -fsanitize=address,undefined \
  -Idecomp/test_support decomp/event_flags.c decomp/test_event_flags.c \
  -o practice/diagnostics/test_event_flags
practice/diagnostics/test_event_flags
python -m unittest tests.test_decomp_verify -q
```

The host C test uses synthetic banks and verifies all 800 flags in each bank,
set/clear idempotence, exact test-mask returns, adjacent-byte/other-bank isolation
and exact 100-byte reset boundaries with sentinel bytes. It is not an in-game
test. Python tests reject bad manifest bounds, source collisions, changed output,
wrong symbols/reference identity and remaining assembly markers. The existing
Python application suite is run separately.

The second unit's host check is:

```bash
gcc -std=c11 -Wall -Wextra -Werror -fsanitize=address,undefined \
  -Idecomp/test_support decomp/system_memory.c decomp/test_system_memory.c \
  -o practice/diagnostics/test_system_memory
practice/diagnostics/test_system_memory
```

## Next units

Continue with small, well-bounded engine translation units and retain the same
full-ROM comparison gate. Resource/state accessors are the next candidate,
followed by the event VM. Actor and
script exports from the existing randomizer remain useful semantic context;
native reconstruction still requires compiler matching and tests. Do not rename
unknown fields or infer state-transition safety from a matching helper alone.
