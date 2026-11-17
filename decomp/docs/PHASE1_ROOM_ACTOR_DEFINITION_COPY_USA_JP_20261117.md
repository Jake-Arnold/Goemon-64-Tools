# Phase 1: original room actor definition → live actor +0xD0 — exact USA/Japan MIPS proof

**17 November 2026.** Scope: resolve the remaining static-data-flow gap between Oedo Mr. Arrow room-definition field `+0x04` and the live actor field `+0xD0`. Both originals are authenticated 32 MiB decompressed retail images. This is **static original-code and room-data verification**, corroborated by earlier user-provided USA Project64 captures. No ROM, extracted assembly, live save or screenshot is committed.

## Results

**The missing transfer is now identified in original native MIPS in both regions.** The generic actor loader resolves a segmented 16-byte room actor definition from a 20-byte instantiated actor record, then copies its three 32-bit parameter words at `definition +0x04/+0x08/+0x0C` to `actor +0xD0/+0xD4/+0xD8`. It subsequently registers actor callbacks. This is a generic *parameter initializer*, **not** the saved-event setter; the latter is separately reached by the actor-specific pickup/torch callbacks.

| Proven instruction/property | USA NG5E | Japan rev-0 NG5J |
| --- | --- | --- |
| Original decompressed ROM SHA-1 | `6ea0ed71032ce08fc2745f412d84936382197494` | `6f8745fecc3a5e7d4918c7a73353eb0726116ded` |
| Loader resource | 12 | 12 |
| Original loader guest VMA | **`0x80218A54`** | **`0x8021DE00`** |
| Resource-relative function start | `+0xB7B4` | `+0xB734` |
| Decompressed ROM start | `0x5D3F24` | `0x5D8D54` |
| Segmented-definition resolver | `0x80014840` | `0x800143D0` |
| Current resolved-definition pointer global (transient `u32`) | `0x8015CDE0` | `0x801625D0` |
| `lw t3,4(t2)` (read definition parameter word 0) | **`0x80218B40`** | **`0x8021DEEC`** |
| `sw t3,0xD0(s0)` (write actor parameter word 0) | **`0x80218B44`** | **`0x8021DEF0`** |
| `sw t5,0xD4(s0)` | `0x80218B50` | `0x8021DEFC` |
| `sw t7,0xD8(s0)` | `0x80218B70` | `0x8021DF1C` |

Two different regional **main-segment** pointer resolver functions have been instruction-checked. In USA, `0x80014840` calls resource-base lookup `0x800141C4` and segment-byte lookup `0x80001E50`; in Japanese rev-0, `0x800143D0` uses `0x80013D54` and `0x80001DF0`. The loader first obtains `lw a0,0x0C(a1)` from the 20-byte room instance record, resolves it via the region-specific resolver, saves the resolved definition pointer in the transient regional global, and reads the actor type (`lhu t8,0(v0)`). Both regions then perform the three word transfers above.

The transient definition-pointer globals above differ by `+0x57F0`, **but this mapping is independently proved by original regional instructions**, not a universal assumption about pointers or overlays. These pointers have scene/initialization lifetime and are not saved fields. The loader function VMAs and decompressed ROM offsets must never be translated by the saved-field displacement.

## Concrete Mr. Arrow example — full independently checked chain

1. **USA stage 13 / Japan stage 4** each select original room **resource 835** (`0x343`). The original room's instantiated group contains an actor instance with definition pointer `0x080000D0` at room-relative `+0x210` (part of its 20-byte instance record). Here segment `0x08` resolves within this resource to definition index **13** (`0xD0 / 16`).
2. Original **16-byte definition 13** starts with actor type `0x0087` (Mr. Arrow). Its source parameter word at `+0x04` is **`0x01040000`** in both authenticated ROMs.
3. The generic loader resolves `0x080000D0` to that definition and performs `lw` from definition `+0x04` followed by `sw` into **live actor `+0xD0`**; the word copied is **`0x01040000`**. The next two 32-bit parameter words are copied to actor `+0xD4/+0xD8`.
4. User-observed USA Project64 RAM showed **`01 04 00 00`** at `0x8016B600` while `S0=0x8016B530`. Thus `actor +0xD0` matches the independently checked original ROM word. This is actual runtime corroboration for this one USA actor, not a live loader instruction trace.
5. The original **resource-26** pickup callback has `lhu a0,0xD0(s0)` in the setter-call delay slot: USA caller `0x08000140`, JP analogue `0x08000130`. The user's USA Project64 capture stopped at native setter `0x80024084` with `A0=0x0104`, `V0=0x8015C628`, `T4=0x10`. The bit is **saved bank C flag `0x104`**, USA `0x8015C628 & 0x10`; JP counterpart **`0x80161E18 & 0x10`**, independently anchored in regional native bank-C MIPS.

**Result:** Original room instance → regional segmented-definition resolver → generic 32-bit parameter copy → actor `+0xD0` → pickup callback `lhu` → native bank-C setter. The static transfer is independently established in **both regions**; final setter **runtime execution** is directly confirmed in USA only.

## Applicability to other instanced pickup and torch actors

The same original generic loader instructions apply to the following **14 individually validated, instantiated original actor definitions** in both ROMs (10 pickups and four Ghost Toys prerequisite actor records). All 14 have identical 16-byte definition records across regions, and each record is actually referenced by the original room-instance groups.

| USA stage → JP stage | Room file / definition index | Actor type | Source word at +0x04 → actor word +0xD0 |
| --- | --- | --- | --- |
| 9 → 0 | 831 / 9 | `0x086` Elly Fant | `0x00FF0000` |
| 13 → 4 | 835 / 13 | `0x087` Mr. Arrow | `0x01040000` |
| 52 → 43 | 871 / 22 | `0x086` Elly Fant | `0x01000000` |
| 57 → 48 | 876 / 7 | `0x087` Mr. Arrow | `0x01050000` |
| 95 → 86 | 900 / 9 | `0x086` Elly Fant | `0x01010000` |
| 99 → 90 | 904 / 16 | `0x087` Mr. Arrow | `0x01060000` |
| 145 → 235 | 943 / 23 | `0x086` Elly Fant | `0x01020000` |
| 152 → 242 | 950 / 9 | `0x087` Mr. Arrow | `0x01070000` |
| 174 → 264 | 962 / 14 | `0x086` Elly Fant | `0x01030000` |
| 182 → 272 | 970 / 16 | `0x087` Mr. Arrow | `0x01080000` |
| 47 → 38 | 866 / 7 | `0x195` Ghost actor | `0x019A0000` |
| 47 → 38 | 866 / 8 | `0x195` Ghost actor | `0x019B0000` |
| 85 → 76 | 893 / 2 | `0x195` Ghost actor | `0x019A0000` |
| 85 → 76 | 893 / 3 | `0x195` Ghost actor | `0x019B0000` |

The USA debugger separately recorded the `0x19A` and `0x19B` native setter calls with `lhu +0xD0` from resource 40, and then a resource-43 call setting gate flag `0x19C`. **Do not claim runtime execution of all four Ghost actor instances or all ten pickups:** the trace confirms the shared static data layout and observed USA flag IDs, not every room placement. Actor `0x08C` exit definitions are excluded; their identically numbered fields are destinations, not event flags. **Stage IDs, VM event IDs and packed saved-bit IDs are separate namespaces.**

## Test record and limitations

- **Actually run:** SHA-1 validation of both original 32 MiB images; **19 original generic-loader MIPS word anchors per region**, plus **two original segmented-resolution JAL anchors per region**, exact match (42 region-specific anchors in total). Both originals' room stage tables, resource pointers, 20-byte actor-instance group references, actor IDs, 16-byte definitions, and the three-word layout were inspected; **14/14 paired definitions PASS**. The complete validated 14-row metadata is in the reproducibility package.
- **ROM-free regression tests:** `python -m unittest -v test_actor_definition_loader_trace.py`: **13/13 PASS**, covering MIPS encoding, endianness and word transfer, valid instantiation, malformed pointers/out-of-bounds refusal, and original-ROM hash/anchor guardrails. Original-ROM CLI: `python actor_definition_loader_trace.py --usa USA_32MiB.z64 --japan JP_32MiB.z64 --report NEW_REPORT.json` produced PASS. Source and tests are supplied in the associated research ZIP, containing no ROM or game asset.
- **Not run:** new native IDO C compilation, combined USA or JP matching-C ROM verification, ELF/relocation/inventory, full `decomp.local_ci`, or live JP debugger capture. No function is promoted by this research. Current separately accepted checkpoint is **779 USA matching-C functions / 34,288 code bytes, 34 Japan / 1,912**, subject to live manifest changes.

**Next technical question:** Identify the upstream engine scheduling/allocation caller of the generic `file_12` loader and whether it is shared across every actor type. The data-copy step itself is now original-MIPS-proven; additional Project64 debugging is not required for this specific Mr. Arrow field mapping.
