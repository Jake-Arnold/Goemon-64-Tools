# Finding native C targets from conversation traces

2026-11-13. Evidence uses the original USA MIPS and SHA-1-pinned decompressed image described in [INPUTS.md](INPUTS.md). The recorded guest PCs come from the [gameplay runtime observations](../docs/VM_GAMEPLAY_RUNTIME_FINDINGS_2026-11-13.md).

## Chain Pipe notice

Resource 96 has 432 aligned text-command patterns consistent with the four recorded PC spacings. Requiring a state-4 token at the last PC leaves 90. Within those sampled records, only the sequence starting at `+0xABC8` contains the Chain Pipe reference. Its surrounding text identifies the Star Block notice. The inferred loaded base is `0x803A2280`.

| Recorded guest PC | Resource-relative resume PC | Preceding text command | Referenced text offset |
| --- | --- | --- | --- |
| `0x803ACE48` | `+0xABC8` | `+0xABC0` | `+0x7CC8` |
| `0x803ACE58` | `+0xABD8` | `+0xABD0` | `+0x7D0C` |
| `0x803ACE60` | `+0xABE0` | `+0xABD8` | `+0x7D44` |
| `0x803ACE68` | `+0xABE8` | `+0xABE0` | `+0x0180` |

The script sets the window style word at `+0xABA8` and requests opening at `+0xABB8`. A spacer line at `+0xABC8` accounts for the skipped eight-byte command in the recordings. The shared final record at `+0x180` contains `-62` (state 4), `-71` (close), and `-1` (end). The close token follows the input wait. `0x8008` follows at `+0xABE8`.

## Oedo Castle bridge

The five observed PC spacings match 248 aligned text-command patterns in resource 96. Requiring `-61` at the state-3 position and `-62` at the state-4 position leaves 19. Two passages explicitly discuss the bridge to Oedo Castle. Both follow the same earlier dialogue in the resource and are separated by a branch that tests story bit 0. The second path also tests bit `0x17`. A third match explicitly names Nihon Bashi Bridge and remains relevant if the scene label in the recording was approximate.

| Passage | Resume PCs relative to resource 96 | Inferred base |
| --- | --- | --- |
| Bridge destroyed | `+0x8980/+0x8988/+0x8998/+0x89A0/+0x89B0` | `0x803A9818` |
| Bridge repair | `+0x89C8/+0x89D0/+0x89E0/+0x89E8/+0x89F8` | `0x803A97D0` |
| Nihon Bashi Bridge | `+0x9598/+0x95A0/+0x95B0/+0x95B8/+0x95C8` | `0x803A8C00` |

All three have a clear-glyph command immediately after the first page wait and use the same final record at `+0x180`. A transcript fragment, coherent loaded base, or text pointer and bytes from either page would resolve the runtime identification.

## Matching-C candidates

`DF98` ties the text tokens directly to the following candidates. They start out assembly-owned in the pinned upstream `asm/usa/C4F0.s` dialogue graphics unit and were absent from the matching-C manifest at the start of this investigation. The function extents below were compared word-for-word against the pinned original ROM.

| Priority | Guest VMA / ROM offset / size | Observed contract and focused test |
| ---: | --- | --- |
| 1 | `8000C53C / D13C / 36 B` | The paired `-33/-32` controls select window presentation values 8/0. The helper stores its argument to window `+0x24` only when the slot exists. Check a missing window and two successive selector writes. |
| 2 | `8000C3EC / CFEC / 68 B` | The `-60` line break zeroes column and x advance, increments the line index and adds line height to y using halfword stores. Check missing window, nonzero layout and halfword wrap. |
| 3 | `8000C3A0 / CFA0 / 76 B` | The shared `-71` close path advances a ready window from phase 4 to 5 and sets bit 0 of the word at `+0x14`. Check absent, busy and ready windows, including preservation of the other flags and the original store at `+0x10`. |
| 4 | `8000D2C0 / DEC0 / 124 B` | The bridge `-63` control calls `D33C` for each of 120 glyph slots. Each iteration clears four layout halfwords after the call. Check the null-window exit, first/last indices and callback/store order. |
| 5 | `8000C314 / CF14 / 140 B` | The open/close poller maps phases 1–3 to 1, 5–6 to 2 and all other phases or a missing slot to zero. Check every phase and an out-of-range signed halfword. |

The same unit also contains `8000D060 / DC60 / 288 B` and `8000D180 / DD80 / 160 B`. Both conversations exercise them through glyph tokens. They follow the smaller helpers because the glyph allocator, atlas lookup, positional fields and stack arguments increase the exact-codegen surface. Stop each candidate after the applicable finite IDO budget. Promote only after original-address unit equality and full-ROM verification.

## Repeatable search pattern

1. For one known resource ID, enumerate word-aligned `0x8010` commands. Resolve each operand within the resource and require a text sentinel within a bounded token count. Record the candidate resume PC at command offset plus 8, alongside the text offset and token IDs. This is a signature scan and may include unreachable data.
2. Try one loaded base across the whole trace. Match all observed PC differences, then require state-specific tokens and any known text, flag or callback clues. Sparse traces can skip intervening commands. For ambiguous results, a coherent live base maps the PCs directly.
3. Follow token dispatch through `DF98` or follow the native callback operand of `0x800B`. Deduplicate by native VMA and compare to the manifest. Use the source unit's original symbol extents to check candidate size and ownership.

With a 256-halfword bound, resources 93, 96 and 97 yielded 353, 1,060 and 1,200 candidate `0x8010` references, respectively. Resource 96 alone yielded 400 references to records containing the line-break control and 173 to records containing the glyph-clear control. These are static references that converge on shared helpers. The same scan can identify distinct native callbacks and give reusable dialogue fixtures to test each helper.

## Promotion results

The pinned native IDO 5.3 build promoted `8000C53C`, `8000C3EC`,
`8000C3A0`, and `8000C314` in the original dialogue graphics unit.
`C53C` and `C3EC` matched with direct field access. `C314` needed the
ordered equality tests and reuse of the argument register for the phase.
`C3A0` needed a 64-bit flag field. Under the original MIPS II flags the
compound update preserves both original word stores and their ordering.

`8000D2C0` remains assembly-owned. The baseline and the three loop/alias
variants all emitted stack allocation at offset zero, where the original
starts calculating the window slot. The callback and four layout stores
were reconstructed. The entry scheduling discrepancy persisted with
postincrement, a distinct layout alias, and volatile layout stores.

The research-branch build matched the complete 6,928-byte unit at
`[0xC4F0,0xE000)` and its full 32 MiB image, with 157 claims / 12,120 bytes.
The four helpers were then integrated with the target branch's verified
file_43 key initializer. The fresh target build matched all 158 claims /
12,216 bytes and the complete 32 MiB image at SHA-1
`6ea0ed71032ce08fc2745f412d84936382197494`. Inventory retains the same 7,376
function identities: 171 combined C and 7,205 ASM entries. The current proof
is `decomp/results/combined.json`; the ignored fresh verifier report is
`practice/diagnostics/decomp-100-inputs/g64-dialogue/20261114-current-target-verify-01.json`.
The sanitized evidence summary is
`decomp/plans/execution/2026-11-14-dialogue-helper-integration.json`.
The generated ELF reports 72 bytes for the retained `D3B8` symbol where
the baseline reports 64, covering two original trailing padding words.
The linked bytes and function entry are identical. The focused host
ASan/UBSan harness covered all signed halfword phases, absent slots,
flag preservation, line wrapping and repeated selector updates.

## Native callback leads

An aligned `0x800B` scan of resources 93, 96 and 97 found 203 main-segment
references to five distinct callbacks already covered by the manifest.
Extending the scan to 756 nonempty resources with virtual base
`0x08000000` and restricting operands to identified native function
entries found 1,043 references to 11 distinct targets. Four still have
assembly ownership, all in the unit beginning at decompressed image offset
`0x5C8770`. Treat these as static call-site candidates until reachability and
overlay identity are confirmed.

| Guest VMA / decompressed offset / size | References | First observed native effect |
| --- | ---: | --- |
| `80222034 / 5DD504 / 20 B` | 11 | Copies a global word to `801C7750`. |
| `80222168 / 5DD638 / 36 B` | 31 | Calls `801DCD48` with the sign-extended byte at `801C7743`. |
| `80221FD4 / 5DD4A4 / 96 B` | 81 | Reads a signed script halfword, adds it to a global word and checks limits. |
| `80214D58 / 5D0228 / 456 B` | 12 | Calls native predicates before branching. Resource 96 contains a candidate reference. |

The 20- and 36-byte callbacks are the first overlay candidates to try.
The current matching manifest and verifier require the main-segment
ROM/VMA relation. These callbacks use a different relation and need
overlay-aware symbol, section and full-ROM verification before promotion.
