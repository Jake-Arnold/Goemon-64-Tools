# USA/Japan original-ROM event-flag banks and save-editor crosswalk

**Date:** 2026-11-17. **Status:** RESEARCH_ONLY; **no C promotion**, **no new native G2**, **no gameplay write**. Original region ROMs were independently authenticated and inspected. This research does not alter `main`.

## Evidence and scope

- USA retail NG5E SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`; expanded 32 MiB SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
- JP rev-0 retail byte-swapped into big-endian, SHA-1 `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b`; expanded 32 MiB SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`.
- Pinned upstream `klorfmorf/mnsg` `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`. Original USA `decomp/event_flags.c` already has 12 accepted matching-C functions (876 bytes). This work **does not count them again**.
- The public third-party [Game Tools Collection](https://game-tools-collection.com/mystical-ninja-starring-goemon/save-editor) editor has source at [`template.ts`](https://github.com/RyudoSynbios/game-tools-collection/blob/bbed775f373db592d5af0cb4993908a0db18a912/src/lib/templates/mystical-ninja-starring-goemon/saveEditor/template.ts) (MIT licensed, commit `bbed775f373db592d5af0cb4993908a0db18a912`). These labels are **external annotations**, not our own native-MIPS proof of gameplay causes, nor proof that every checkbox is valid. The editor supports NG5E/NG5J/NG5P save identifiers and has USA/JP tests and fixtures. Tests were **inspected, not executed** in this session.

## Three banks: original MIPS across both regional ROMs

| Bank | USA first byte | USA 100-byte exclusive end | JP first byte | JP 100-byte exclusive end | JP–USA |
|---|---|---|---|---|---|
| A | `0x80168E90` | `0x80168EF4` | `0x8016E670` | `0x8016E6D4` | `+0x57E0` |
| B | `0x80168EF8` | `0x80168F5C` | `0x8016E6D8` | `0x8016E73C` | `+0x57E0` |
| C (packed saved events) | `0x8015C608` | `0x8015C66C` | `0x80161DF8` | `0x80161E5C` | `+0x57F0` |

**Do not use `+0x57F0` for A/B.** Each bank has 100 bytes/800 possible bit IDs. The 12 original helper functions implement set (byte OR mask), clear (byte AND inverse mask), test (masked return) and reset (zero exactly 100 bytes). Indexing uses 8-bit-truncated `flag/8` and `flag%8`; negative input handling follows C signed division. Bounds, scripting semantics and safe writing are not established merely by these functions.

| Operation | USA A / JP A expanded-ROM offsets | USA B / JP B | USA C / JP C |
|---|---|---|---|
| Set | `249F0 / 246B0` | `24B14 / 247D4` | `24C38 / 248F8` |
| Clear | `24A40 / 24700` | `24B64 / 24824` | `24C88 / 24948` |
| Test | `24A94 / 24754` | `24BB8 / 24878` | `24CDC / 2499C` |
| Reset | `24AE4 / 247A4` | `24C08 / 248C8` | `24D2C / 249EC` |

Local byte-by-byte direct comparison over **all 12 original function spans**: 876 bytes = 219 MIPS words in each region. All 12 JP counterparts are at USA expanded ROM offset **minus `0x340` for this specific contiguous unit**. The only 15 mismatching instruction words are the expected address-immediate operands for the two regional bank-base/end pointers (set/clear/test: one; reset: two). Their other 204 words agree exactly. **Neither this code-offset coincidence nor the RAM delta is a universal cross-region code map.** JP matching-C is **not** yet compiled/proven and thus not promoted.

## Save-file offset ↔ live USA RAM relationship

The editor's three slots have relative record stride `0x500`. Each slot's checksum lives at relative `0x100`; the protected 0x304-byte payload spans **`0x104..0x407` inclusive**. These are **post-unpacking, slot-relative offsets**, NOT physical byte offsets in raw `.mpk`, DexDrive `.n64`, or RetroArch `.srm` files.

USA `decomp/save_resources.c` (already accepted matching-C) copies exactly 0x304 bytes from saved `D_8015C608` into shadow `D_8015C910`; `decomp/save_resources.h` defines `SaveData.flags[0x64]` at the front. The resulting **USA live saved-data crosswalk** is:

```text
USA guest RAM byte = 0x8015C608 + (editor slot-relative offset - 0x104)
JP candidate RAM   = USA guest RAM byte + 0x57F0
```

For editor offsets `0x104..0x167`, this resolves to the **independently original-MIPS-proven** JP bank-C storage range. For offsets `0x168..0x407`, it is an **offset-candidate**, not individually corroborated Japanese writer or field interpretation. The 3 `Option` flags at editor offsets `0x007`, `0x00B`, `0x00F` are **outside this payload**, not safely translated by this formula.

### Examples (third-party labels vs independently evidenced locations)

| Meaning/source | Editor slot offset / bit | USA RAM / mask | JP RAM / mask | Status |
|---|---|---|---|---|
| Super Pass-related packed event, editor annotation ID `0x000` | `0x104 / 0` | `0x8015C608 / 0x01` | `0x80161DF8 / 0x01` | Bank locations native; label external |
| Benkei encounter ID `0x025` | `0x108 / 5` | `0x8015C60C / 0x20` | `0x80161DFC / 0x20` | Independently recorded in toolkit; editor leaves label unknown |
| Miracle Snow progression ID `0x035` | `0x10A / 5` | `0x8015C60E / 0x20` | `0x80161DFE / 0x20` | Editor label + native bank location; distinct from inventory Snowflake |
| Mr. Arrow (Oedo Castle) ID `0x104` | `0x124 / 4` | `0x8015C628 / 0x10` | `0x80161E18 / 0x10` | USA has placement evidence; JP individual meaning unverified |
| Ghost Toys entrance torch IDs `0x19A/19B`; unlock `0x19C` | `0x137 / 2,3,4` | `0x8015C63B / 0x04,0x08,0x10` | `0x80161E2B / same masks` | Existing USA native/gameplay research; editor labels all three unknown; JP semantics unverified |
| Oedo Castle visited flag | `0x3B3 / 0` | `0x8015C8B7 / 0x01` | `0x801620A7 / 0x01` | Corresponds to previous USA external `0x8015C8B7` cheat lead; JP offset-candidate only |

The save editor records visited-location fields at `0x3DF` (`0x8015C8E3`, low byte of a big-endian word beginning `0x8015C8E0`), `0x3E3` (`0x8015C8E7`; word start `0x8015C8E4`) and `0x3E7` (`0x8015C8EB`; word start `0x8015C8E8`). These **reconcile the apparent three-byte mismatch** with external whole-word warp-unlock GameShark addresses without establishing the cheat's write safety or usage semantics.

### Explicit discrepancies / do not silently replace existing toolkit mappings

1. The editor's Miracle Snow inventory checkbox uses slot `0x363`, mapped byte `0x8015C867`, whereas toolkit `practice/unlocks.py` uses USA `0x8015C866`. The known JP `0x80162057` is `USA 0x8015C867 + 0x57F0`, but `USA 0x8015C866 + 0x57F1`. This may be a field-width/endian representation difference, source error or actual regional variation. **Disputed until native loads/stores and a controlled event capture resolve it.**
2. The editor's character weapon-level checkboxes use `bit=1,2,3` as **threshold selectors**, via a custom getter/setter; they are **not masks**. Twelve such entries in the CSV have blank mask and `CHARACTER_LEVEL_THRESHOLD_NOT_A_MASK`.
3. The toolkit records Chain Pipe byte `0x8015C6BF` with acquired value `0x02`, but the editor checks bit zero at slot `0x1BB`. These semantics conflict for byte value `0x02`; do not assume the third-party checkbox is correct.
4. Editorial `???` fields and labels in the editor do not prove specific in-game triggers. The editor's `Miscellaneous` tab is hidden and the game may have more bank bits than the editor names.

## Data registry and accounting

[`editor_save_flag_crosswalk_20261117.csv`](../data/editor_save_flag_crosswalk_20261117.csv) contains **524 unique saved-data editor checkbox definitions** with parsed slot offset, bit or level selector, USA guest address, cautiously classified JP guest candidate, and third-party label. Among them: **456** are within packed bank C (156 non-`???` labels, 300 unknown) and **68** refer to later saved-data fields. Total: **223** labelled and **301** `???`. Three menu-Option entries are explicitly excluded. Bank A and B contribute another 1,600 possible unnamed IDs not asserted to be saved.

For every known packed bit, trace actual event-script opcode/call chain into one of the three set/clear/test helpers, determine scene/overlay ownership, and distinguish direct byte/word stores from helper calls. Separate script data offsets from code/ROM offsets and original RAM globals. Begin with the already-promoted USA `event_flags.c`, `save_resources.c`, `script_vm.c`, `practice/story_progress.py` and referenced original resource scripts. The editor alone cannot supply these writers.

## Adjacent matching-C candidates (unproven, no promotion)

- Preceding USA `func_80023DC4_249C4`, 36 bytes, is an original MIPS wrapper loading `D_801C7740` and calling `func_800239B8_245B8`. **RESEARCH_ONLY**, possible simple native IDO candidate, unrelated to saved-event bit semantics.
- USA `func_80023D80_24980`, 68 bytes, is an adjacent call + small nested loop, not yet source-matched; **RESEARCH_ONLY**.
- Next USA `func_80024160_24D60`, 0x510 bytes, is a substantial unrelated allocation/object routine; lower immediate promotion priority.
- **JP counterpart 12-function batch**, 876 bytes, is especially promising source-layout research because the original instruction control-flow is identical apart from regional global addresses. Still **RESEARCH_ONLY**: no original-ID0 compiled JP C, actual-unit integration, full Japan ROM, ELF relocation inventory or full local CI pass in this task.
- Existing USA 129 research candidates, 5 JP research candidates, and USA 732 / Japan 34 promoted functions remain unchanged. New JP MIPS discovery is not counted as matching C.

### Tests actually run

- Authenticated all three uploaded retail/normalized images and their SHA-1s.
- Reproduced **both** 32 MiB expanded ROMs with pinned `rommy.py`; both SHA-1s exactly matched expected.
- Read and disassembled original-USA main segment around `0x249F0` and `0x249C4`; compared 12 original USA/JP function spans with a direct Python 32-bit-word comparison; **219 words, 15 permitted address-operand differences**.
- Parsed the editor's upstream TypeScript; checked 527 total entries, 524 per-slot saved-data entries, 3 Option entries, 456 packed-bank entries and zero duplicate offset/bit pairs. Inspected its special character-level getter and its checksum/payload metadata.
- **NOT RUN:** any new native compiler promotion, fresh central USA G2, Japanese 34+12 C combined G2, full `decomp.local_ci`, in-game read/write tests, editor's Playwright suite. No assertion of new matching-C acceptance.
