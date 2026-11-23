# Japanese short28 original-ROM C integration (23 November 2026)

Scope: 28 original Japanese functions, **1,980 original instruction bytes**,
**124 original symbolic relocations**, 13 original Splat ASM owners (21 active
owner fragments after earlier decomp staging). This source-only research is
strictly independent of the previously merged **72 USA C** functions.

Origin: live `stable/decomp@56e4754255403f012cc9bc88ba39ec1f4fadfb6c`,
source artifact `goemon-source-stable-decomp-56e4754255403f012cc9bc88ba39ec1f4fadfb6c`,
verified `COMMIT.txt` and `SHA256SUMS`; pinned upstream
`mnsg@7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, authentic normalized JP
retail SHA1 `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b` and expanded 32 MiB
SHA1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`.

The 28 C source files and the 28 one-variable negative C controls are copied
byte for byte from `goemon-native100-20261123.zip`. The pinned manifest records
original ROM offsets, VMAs, sizes, original code SHA256, compiler source SHA256,
individually observed original relocation counts and negative control SHA256.
`native_replay_results.json` records a **fresh 28/28 isolated IDO 5.3 positive
and negative replay** against the authenticated source/ROM. Each control differs
in either MIPS instruction bytes, original relocation name/type/offset, or
symbol addend. These are not whole-ROM proof.

Original SGI IDO 5.3 SHA256
`76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0`,
isolated flags `-c -G 0 -non_shared -O2 -mips2`, original full build adds
upstream's original `-Xfullwarn`, include paths and defines. All attempts
classified `NO_NEW_COMPILER_FINDING`; consult `COMPILER_QUIRKS.md` before each.

The private staging adapter `python3 -m decomp.japan_short28_promotion` accepts
only an independently rebuilt **2,370 C** predecessor and refuses already
accepted/duplicate C. It splits original ASM owners into *unchanged source
fragments*, compiles the 28 original native C units, and trims only verified
trailing zero *ELF section* padding (never game opcodes or relocs). The
acceptance gate independently checks the original 32MiB ROM, 7,376 positive
ELF function identities, all Japanese published 80,745 complete semantic
relocations (the previously reviewed two-record C-Right original-reference
distinction is preserved), 2,398 original C ownership markers, complete original
retail ROM, regional inventory and full `decomp.local_ci`.

No ROMs, original assembly, compressed assets, linked ELFs, proprietary tools,
private snapshots, original game machine-byte dumps or game save states are in
the repository. Gameplay not tested.

Run from a complete clean source archive with private pinned upstream checkout:

```sh
python3 -m decomp.japan_short28_promotion plan --checkout /PRIVATE/jp2370
python3 -m decomp.japan_short28_promotion stage --checkout /PRIVATE/jp2370
python3 -m decomp.japan_short28_promotion build --checkout /PRIVATE/jp2370 \
  --deps /PRIVATE/goemon-dependencies --runtime /PRIVATE/goemon-runtime-additions
python3 -m decomp.japan_short28_promotion verify --checkout /PRIVATE/jp2398 \
  --base /PRIVATE/jp2370-baseline
python3 -m decomp.local_ci
```

`stage` and `build` modify their private working checkout; the source archive
and accepted 2,370-C proof must remain separately preserved.

The source-only exact compiler regression is independently rerunnable without
any earlier session artifact. Both `replay_native.py` and
`native_probe_helpers.py` are bundled with the 28 pinned original C sources and
negative controls. Example (from this research directory):

```sh
LD_LIBRARY_PATH=/PRIVATE/goemon-runtime-additions/lib \
python3 replay_native.py \
  --jp-rom /PRIVATE/japan_0/baserom.decompressed.z64 \
  --jp-splat /PRIVATE/clean-pinned-mnsg/asm/japan_0 \
  --ido /PRIVATE/clean-pinned-mnsg/tools/ido-5.3/cc \
  --objcopy /PRIVATE/mips-linux-gnu-objcopy \
  --readelf /usr/bin/readelf \
  --ledger /PRIVATE/current-stable-decomp/decomp/COMPILER_QUIRKS.md \
  --output /tmp/NEW-jp28-native-probes
```

This standalone isolated replay checks all 28 names, exact original MIPS
instructions (with relocation operand masks), exact source hash, original ELF
function extent, all 124 original symbolic relocation names/types/offsets,
and 28 negative-control mismatches. It is additional to the full original-ROM
G2 proof, not a substitute.
