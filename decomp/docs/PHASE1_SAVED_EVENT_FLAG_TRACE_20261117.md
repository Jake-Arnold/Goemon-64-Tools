# Phase 1: USA/Japan saved-event flag writers and readers (2026-11-17)

**Scope:** Read-only static scans of the authenticated USA and Japanese rev-0 decompressed retail ROMs, plus direct review of the original instructions and one user-supplied Japanese gameplay observation. This report is research evidence, **not** a matching-C promotion, an exhaustive call graph, a verified live-memory write interface, or a claim that every candidate script opcode is reachable.

## Inputs and fixed guest-address ownership

| Region | 32 MiB decompressed SHA-1 | Saved bank C (100 bytes) | Original native saved-flag set / clear / test |
| --- | --- | --- | --- |
| USA NG5E | `6ea0ed71032ce08fc2745f412d84936382197494` | `0x8015C608..0x8015C66B` | `0x80024038 / 0x80024088 / 0x800240DC` |
| Japan rev-0 NG5J | `6f8745fecc3a5e7d4918c7a73353eb0726116ded` | `0x80161DF8..0x80161E5B` | `0x80023CF8 / 0x80023D48 / 0x80023D9C` |

Original USA native VM dispatcher `func_8003D68C_3E28C` calls saved-bank-C helpers for opcode `0x8020` (set), `0x8021` (clear) and `0x8022` (test and conditionally jump when nonzero). The primary saved-event bit ID `n` resolves to byte `bank_C + (n >> 3)` and mask `1 << (n & 7)`. These helpers and the corresponding 12-function Japanese flag-management unit were independently checked against original MIPS in the preceding [save/editor research](USA_JAPAN_SAVE_EDITOR_EVENT_FLAG_CROSSWALK_20261117.md). The Japanese **bank C** storage is therefore independently known, not merely guessed by offset. **Bank A/B are different banks with JP displacement +0x57E0**, not +0x57F0.

## Region-paired bounded scan totals

Both original decompressed ROMs expose 1,084 nonempty file-table ranges. The scripts scan aligned 32-bit `0x8020/0x8021/0x8022` commands and bounded native JALR flag-helper patterns. The second scan misses reused, spilled and computed call targets; it is not complete dataflow analysis.

| Candidate category | USA | Japan-0 |
| --- | ---: | ---: |
| Script set `0x8020` | 296 | 297 |
| Script clear `0x8021` | 290 | 291 |
| Script conditional test `0x8022` | 306 | 307 |
| **Total script patterns** | **892** | **895** |
| Distinct script flag IDs | 136 | 137 |
| Native indirect helper call candidates, A/B/C | 484 | 486 |
| Native candidate sites with literal delay-slot flag ID | 343 | 342 |
| Native candidate sites with dynamic/unresolved argument | 141 | 144 |

USA native bank C has **325** candidate call sites, **258** carrying literal valid saved-event IDs (49 set, 55 clear, 154 test) across **109 distinct IDs**. Japan native C has 49 set, 55 clear, 153 literal test sites. USA script and native-literal saved-bank-C IDs together cover **201** distinct values, with **44 shared** between the two scanners. Japan adds ID `0x142` (322), yielding a **202-ID union**.

Of the editor's **156 named** packed saved-event bits, **35** have at least one candidate script or native-literal reference (10 via scripts, 28 via native calls, three overlap). The remaining named or unknown editor bits have **not** been proven unused. The regional pattern count agrees for **410** shared `(resource file ID, flag ID, opcode operation)` tuples; **891** USA script occurrences have JP tuple-level counterparts. A simple pattern hit may still occur in unreachable script data. See the [202-ID machine-readable index](../data/phase1_saved_event_flag_reference_index_20261117.csv). Its `editor_label` field is an unverified third-party annotation; other columns are static reference-candidate counts, **not runtime hit counts**.

## Newly evidenced Super Pass → Oedo Castle gate chain

**User-supplied JP runtime event**, 2026-11-17T19:34:40Z, recomp backend, investigation `b71e3414387d4e45aaf874f60d2ad961`: one event trial during a guard conversation with the Super Pass-related condition set showed **`0x80161DF8 & 0x02` changing to set**, while the player observed the castle gate open. **No idle/control trials, live-ROM SHA-1 verification or instruction-access trace** were supplied. This is strong corroboration when combined with the actual JP script/native code, but the trial alone is not a causality or safe-writing proof.

Two **independent bits** share one byte:

| Event ID | Japan saved byte / mask | USA saved byte / mask | Evidence distinction |
| --- | --- | --- | --- |
| `0x000` | `0x80161DF8 & 0x01` | `0x8015C608 & 0x01` | Prior editor: Super Pass-related stage; used as a script prerequisite; actual item possession separately represented |
| `0x001` | `0x80161DF8 & 0x02` | `0x8015C608 & 0x02` | Prior editor: "Oedo Castle: Gate opened"; original script writer and native readers verified in both ROMs; new Japanese gameplay corroboration |

The investigation reports the mask being set, not a full `0x01 → 0x02` byte replacement. If the `0x01` bit remains set, both bits together produce byte value `0x03`. **Do not infer a clearing of bit 0** from this trial.

### Original JP resource-96 script, branch and write verified

JP resource 96, decompressed file base `0x74F660`:

1. **`+0x50D8`** (absolute `0x754738`): `0x8022, 0x000, 0x08005138` — test receipt-stage `0x000`; jump to `+0x5138` when set.
2. **`+0x5138`** (absolute `0x754798`): `0x8022, 0x001, 0x080051C4` — test whether gate bit `0x001` is already set; skip the following first-time interaction when set.
3. **`+0x5184`** (absolute `0x7547E4`): `0x8020, 0x001` — **set gate flag** through native saved-bank-C helper.
4. **`+0x52E0`** also tests `0x001`, and **`+0x532C`** also sets `0x001`, showing a second script path for the gate event.

USA resource 96, base `0x74ECE0`, independently contains the same flag sequence at **`+0x8260`** (test `0x000` → `+0x82C0`), **`+0x82C0`** (test `0x001` → `+0x8344`) and **`+0x8304`** (set `0x001`); additional test/set at `+0x8470/+0x84BC`. This is an **original-ROM regional code and data crosswalk**, not blindly translating script offsets.

### Independent original gate-object readers in resource 51

JP resource 51, base `0x711C70`, contains two literal calls to native tester `0x80023D9C` with argument `1`: JALR at **`+0x388`** and **`+0x770`**. At `+0x390`, the first result selects a different object update path; the second at `+0x778` branches to call another engine routine when the flag is set. USA resource 51, base `0x70D740`, has corresponding original JALR tests at the **same relative +0x388 and +0x770** into native tester `0x800240DC`. This supplies an independent **gate-object reader** outside the guard script.

**Evidence outcome:** JP observation + both regions' original script setter path + both regions' original native readers support the *guard conversation → gate-bit set → gate-object checks flag* model. Precise sprite collision/animation causality and runtime instruction access remain open without a VM cursor/native trace.

## Other high-value original-code relationships

### Ghost Toys castle entrance (same conditional code in USA and Japan)

A separate original **140-byte MIPS function** in USA file 43 `+0x6490` (ROM `0x6F9970`) and JP file 43 `+0x63B4` (ROM `0x6FDF44`) has **30 identical instruction words and five regional immediates/call-address differences**. It tests saved bank C **`0x19A`** and then **`0x19B`** with the native tester, sets **`0x19C`** only if both tests return nonzero, then updates actor state. The second tester call **reuses a function pointer** and was not recognized by the narrow native scan.

| Flag | USA byte / mask | Japan byte / mask |
| --- | --- | --- |
| `0x19A` (entrance condition A) | `0x8015C63B & 0x04` | `0x80161E2B & 0x04` |
| `0x19B` (entrance condition B) | `0x8015C63B & 0x08` | `0x80161E2B & 0x08` |
| `0x19C` (unlock flag) | `0x8015C63B & 0x10` | `0x80161E2B & 0x10` |

The previous USA research describes the two prerequisites as torches and the final state as the entrance unlock. **The native tests/set are proven; the exact physical activators and JP gameplay still need isolated confirmation.**

### Script-only crosswalks and region differences

- **Oedo old-man cycle `0x002`:** USA resource 96 `+0x8C58` test, `+0x8C8C` set, `+0x8CC0` clear; JP resource 96 `+0x5AB0/+0x5AE4/+0x5B18`. USA byte `0x8015C608 & 0x04`; JP `0x80161DF8 & 0x04`. USA runtime observations already exist; explicit scene causality is not inferred from pattern matching alone.
- **Oedo coffee-shop cycle `0x008`:** USA file 96 `+0xA434/+0xA480/+0xA4B4` test/set/clear; JP `+0x72E4/+0x7320/+0x7354`. USA `0x8015C609 & 0x01`, JP `0x80161DF9 & 0x01`.
- **Benkei encounter `0x025`:** USA file97 `+0xA68C` set and `+0xC078` test, file112 `+0x332C` set, file121 `+0x1D74` set. JP: file97 `+0x69B0/+0x835C`, file112 `+0x1E8C`, file121 `+0x1200`.
- **Miracle Snow progress `0x035`:** USA file97 `+0xCDA4` test, `+0xD5D0` set; file102 `+0x90C4` test; file112 `+0x3CB0` test; native file62 `+0x4BC` test. Japanese static operation counts also agree. Distinct from disputed Miracle Snow inventory field.
- **Actual regional difference:** USA file110 `+0x2A80` (expanded ROM `0x797FB0`) sets **flag `0x05B` (91)**; JP file110 `+0x1DE0` (expanded ROM `0x786010`) instead sets **`0x05C` (92)** within corresponding surrounding script code. Preserve different flag identities.
- **Japanese-only script candidates:** JP file81 `+0x84` set `0x081`, `+0x8C` clear `0x142`, and `+0x94` test `0x081` with target `0x09000068`. Segment 9 is legitimate for some resources; whether this path runs in-game is not yet proven. USA file81 has different script data.
- **Unresolved:** editor-labelled Mr. Arrow flag `0x104` (USA `0x8015C628 & 0x10`; JP `0x80161E18 & 0x10`) has no literal script/native-C candidate in this bounded scan, indicating the need to trace computed IDs and direct stores. High-volume `0x082` (130) shows **84 script set and 207 script clear patterns** in each region; do not equate frequency with a verified story interpretation.

## Reproducibility, verification tier and next analysis

The existing [USA opcode-pattern analyzer](../../practice/rom_flag_trace.py) is a public starting point. This task used a separate local read-only regional scanner that authenticated both SHA-1s, parsed the same ROM file table, collected aligned opcodes and bounded `LUI 0x8002 → ADDIU/ORI → JALR` calls, then joined the bank-C ID summaries to the existing editor metadata. The **202-ID index** records both regions' 12 operation-count columns. No ROM payload, raw disassembly, runtime save or personal save-state is committed.

**Tests actually run:** two original 32 MiB SHA-1 checks; original-script word/branch/operand assertions at three guard anchors in both regions; two native-reader target/argument plus branch assertions in both regions; **3/3 original-ROM anchor tests pass**. **5/5 synthetic/ROM-free scanner tests pass** (JP segment-09 flag operand, file boundary, regional helper targets, bank A versus bank C, wrong-ROM rejection). The native Ghost Toys 140-byte span was separately compared word-for-word with the original two ROMs. **No runtime debugger was attached for these static tests.**

**Not run:** full resource entrypoint CFG, complete overlay dataflow, user-side controlled guard repeats, native IDO recompile of new C, new full-ROM G2/inventory or full decomp local CI. No C functions were promoted; the new static research does not change current accepted matching-C counts.

**Next targets:** prove the guard resource-96 VM entrypoint from the relevant NPC/map; trace setter of `0x000` in file94; derive native/computed writers for Ghost Toys `0x19A/0x19B` and Mr. Arrow `0x104`; inspect the JP-only file81 path; use control trials only for the remaining semantic uncertainties.
