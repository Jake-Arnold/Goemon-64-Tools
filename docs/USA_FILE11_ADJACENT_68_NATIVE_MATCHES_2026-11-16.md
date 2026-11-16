# USA file_11 adjacent native-matching C discovery — 16 November 2026

## Scope and evidence boundary

Read the authentic **32 MiB decompressed USA ROM** SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494` and the generated original-USA Splat `asm/usa/587370.s` derived from pinned upstream `mnsg` Git revision `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`. Verified the original assembly source SHA-256 `e936f86295b8d8795369fd6db6a42da5b13184b9856058878066b9448e4a5f8b`. The Splat source inventories **906** positive-size `nonmatching func_...` names for original `file_11`, providing the original C function boundaries used in this pass.

All tested functions were **not** among the 77 native research candidates already recorded in draft PR #23 or the 50 functions formally promoted into the production 210-function baseline. The original IDO 5.3 compiler (`-G 0 -non_shared -Xfullwarn -Xcpluscomm -O2 -mips2`) generated matching MIPS instructions at each original USA VMA. Native objects were linked with the supplied pinned MIPS linker and compared to the exact original ROM spans.

**New result: 68/68 exact functions / 2,416 original instruction bytes**, comprising **55 more handler call wrappers** and **13 compact state/flag/float/no-op helpers**. The result is **isolated original-VMA IDO machine-code proof, not a whole-ROM rebuild**. There is no production manifest, complete 32 MiB candidate, full ELF relocation or `decomp.inventory` acceptance in this task. Official baseline **remains 210 functions / 13,336 bytes / 7,153 assembly entries**.

## The important adjacent discovery

Compiled **13 groups as single original-VMA C translation units**, preserving every original function instruction in its exact location. All **13/13 groups match**, covering **42 functions / 1,576 bytes**. Per-object trailing zero padding beyond the original final function is excluded from matching and would require an exact overlay linker adjustment during formal promotion. Only the first largest group compiles to its original length with no trailing padding.

| Original USA file_11 extent | Functions | Original bytes | Native combined C result |
|---|---:|---:|---|
| `0x59EE00–0x59EE54` | 3 | 84 | Exact |
| `0x5A6F30–0x5A7090` | 8 | 352 | Exact |
| `0x5A7B74–0x5A7BF8` | 3 | 132 | Exact |
| `0x5AA6B0–0x5AA734` | 3 | 132 | Exact |
| `0x5ACE10–0x5ACE94` | 3 | 132 | Exact |
| `0x5AAC94–0x5AAD08` | 4 | 116 | Exact |
| `0x59A104–0x59A180` | 3 | 124 | Exact |
| `0x5B13D0–0x5B144C` | 3 | 124 | Exact |
| `0x5ACFD4–0x5AD040` | 3 | 108 | Exact |
| `0x5B0488–0x5B04F4` | 3 | 108 | Exact |
| `0x5B3040–0x5B3050` | 2 | 16 | Exact |
| `0x5A4070–0x5A40A4` | 2 | 52 | Exact |
| `0x59ED40–0x59EDA0` | 2 | 96 | Exact |

The largest **eight adjacent 44-byte functions** occupy exactly `[0x5A6F30, 0x5A7090)` (352 bytes) and compile into a **352-byte C object with no text-size correction**. Each forwards the actor and an unsigned-byte event to a common native handler with a fixed third argument. This is a particularly clean future central-overlay promotion island.

The **three-function group** `[0x59EE00, 0x59EE54)` changes actor float fields and related nested actor state. A second contiguous pair `[0x5A4070, 0x5A40A4)` sets/clears bit 0 of the shared word at **`0x8015CD04`** (base address `0x8015CC30`, field offset `0xD4`); this establishes the native memory operation but not what the game flag means. The `[0x5B3040, 0x5B3050)` pair clears the actor's `+0x48` word followed by a genuine eight-byte empty hook.

## Broader findings

The additional handler wrappers include six- and three-function families with event selectors or byte-sized arguments. They are useful for call-graph reconstruction but **do not yet identify the underlying event's player-facing purpose**. Distinguish these thin forwarding wrappers from actor-state changes and the substantive 180-byte character selection routine, which remains in assembly.

Specific adjacent families worth investigating next:

- `[0x5A6F30, 0x5A7090)`: eight identical-size byte-event wrappers, one future C island
- `[0x59EE00, 0x59EE54)`: three actor float/nested-state helpers, usable together
- `[0x59ED40, 0x59EDA0)`: two 48-byte wrappers each chaining **two original native handlers**
- `[0x5AAC94, 0x5AAD08)`: an empty hook and three 36-byte forwarding callbacks
- `[0x5A4070, 0x5A40A4)`: complementary global bit set/clear operations

## Reproduction / new artefacts

- `decomp/research/file11_adjacent_sources.json` contains **68 reconstructed C function sources**, original ROM address/size/hash and linker bindings, plus the 13 contiguous review groups. Contains no original ROM/instructions/asset data.
- `decomp/research/file11_adjacent_native_probe.py` checks the original USA ROM and extracted original function index against pinned identities before compiling each function and each adjacent group with original IDO and native linker, emitting JSON proof without original machine-code dumps.
- `decomp/results/file11_adjacent_native_proof_20261116.json` records **68/68 exact original-VMA compiler results and 13/13 exact C islands**, original and candidate SHA-256 signatures and compiler-source hashes.
- `tests/test_decomp_file11_adjacent.py` provides ROM-free validation for pinned fixture metadata, group contiguity, C type/linker-symbol aliasing and fail-closed reference gates.

Example native proof command after setting up the pinned toolchain from `GOEMON_BUILD_ENVIRONMENT.md`:

```bash
python3 -m decomp.research.file11_adjacent_native_probe \
  --rom /path/to/usa/baserom.decompressed.z64 \
  --asm /path/to/upstream/asm/usa/587370.s \
  --cc /path/to/upstream/tools/ido-5.3/cc \
  --ld /path/to/mips-linux-gnu-ld \
  --objcopy /path/to/mips-linux-gnu-objcopy \
  --report /tmp/unique-file11-adjacent-proof.json
```

## Totals, formal promotion rule and next steps

Previous unpromoted draft PR #23: **77 functions / 2,120 bytes**. Newly identified in this pass: **68 more / 2,416 bytes**. Combined **145 independently original-address native-matching C research candidates / 4,536 bytes** beyond the canonical **210 matching C / 13,336 bytes**.

**Prospective only**, if all 145 were subsequently integrated and passed a complete original USA ROM+ELF+inventory gate: **355 matching-C functions / 17,872 bytes**, with assembly inventory adjusted only after verification. No such 355-function production build has occurred. The authentic Japanese regional whole-ROM promotion also remains a distinct blocker.

The immediate next engineering step is a versioned multi-island `file_11` adapter staging the highest-confidence contiguous groups. It must preserve original assembly between islands, original C symbol locations, all 8,825 `file_11` relocation tuples, the full original 32 MiB USA ROM, and the rest of the existing 210-function central G2 before any published inventory change.
