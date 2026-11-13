# VM resource and stream call graph

**G64-021 research checkpoint — 2026-11-11.** This note records observed
call/argument behavior before changing shared VM types. Direct instruction facts
are marked **verified**; interpretations of opaque IDs and external engine
helpers are marked **inferred** or **unknown**. It is not a matching-C claim.

## Evidence source

- Branch base: `chatgptweb/decomp` at `907e86bc04e3abccb902c742813eb2e5406b2cd9`.
- Pinned upstream: `mnsg` commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`.
- Private reference: local ignored
  [`usa-decompressed.z64`](../practice/diagnostics/decomp-100-inputs/usa-decompressed.z64),
  USA SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`, 33,554,432 bytes.
- Original-code extraction: Splat 0.36.3 / spimdisasm 1.39.0, run from the
  pinned upstream checkout with
  `uv run splat split config/usa/splat.yaml --modes code --disassemble-all`.
  The generated, ignored local listing is
  [`3DBA0.s`](../practice/diagnostics/decomp-100-inputs/mnsg-pinned/asm/usa/3DBA0.s).
  These links resolve only in a workspace with the private inputs; neither file
  is stored in the repository.
- For each function below, all listing word comments were checked against the
  corresponding big-endian ROM slice at `VMA - 0x7FFFF400`. Start, extent and
  SHA-256 are therefore tied to this private reference, rather than reassembled
  text.

| Function | ROM offset | VMA | Bytes | Original-byte SHA-256 |
| --- | ---: | ---: | ---: | --- |
| `func_8003D468_3E068` | `0x3E068` | `0x8003D468` | 548 | `ece95b38f4dbaf5268d308e09aea54a02d32d1615664137de03ecd46a0c262d7` |
| `func_8003D68C_3E28C` | `0x3E28C` | `0x8003D68C` | 812 | `e49ad551d97f2f8cac887ee126e99dfdb29924901a4ff69f0792898207bf3da5` |
| `func_8003DDC4_3E9C4` | `0x3E9C4` | `0x8003DDC4` | 132 | `f7dab493df8553cae7eb55ce5bbaec5a2cd576e0454dc557dbbadad74a7a101a` |
| `func_8003DF98_3EB98` | `0x3EB98` | `0x8003DF98` | 528 | `76285ca92a7f611916d867d9938f93fcb3df32ebfa2962120083f2471a501631` |
| `func_8003F038_3FC38` | `0x3FC38` | `0x8003F038` | 196 | `7a258b9eae36120d3971f1997070c2a988fb9636cbd4c96f1f52ea888e7b9719` |

## Typed VM resource interface matrix (G64-030)

**Checkpoint:** current branch commit before this documentation update is
`5b9f74b52581b177ea3d7be7344f44c07047e948`. The live
`results/combined.json` records an exact 33,554,432-byte ROM match and 148/148
claimed functions / 11,020 bytes; `results/inventory.json` records 7,376
identified entries, 161 combined C entries and 7,215 remaining ASM. The
`script_vm.c` manifest unit spans `0x3DBA0..0x40320` and currently lists 56
functions: 43 C and 13 assembly. This supersedes older VM-unit totals elsewhere
in dated historical notes.

Evidence labels used below:

- **ROM-OBSERVED:** argument, access, control-flow, or original address/extent
  checked against the pinned USA ROM and Splat listing. This does not prove a C
  translation.
- **G2-MATCHED:** the live combined proof records original and candidate bytes
  equal at the function's original address, and the full image matches.
- **HOST-LAYOUT:** compile-time layout/endian assertions passed on the host;
  this does not establish callback or in-game behavior.
- **INFERRED:** a useful semantic name supported by call sites, but not an
  engine-level declaration.
- **UNKNOWN:** evidence does not establish a stable type or behavior.

### Function interfaces and current ownership

| Function / address | Word-level ABI and contract | Current source ownership | Evidence and exactness |
| --- | --- | --- | --- |
| `D468` — VMA `0x8003D468`, ROM `0x3E068`, 548 bytes | Two 32-bit inputs: `$a0` script/address and `$a1` resource ID. Original returns a 32-bit 0/1 setup status; `script_vm.h` still declares `void`, and observed C callers ignore the result. The original spills `$a0` at `sp+0x20` (`0x8003D484`) and the entry resource ID at `sp+0x24` (`0x8003D4AC`). | `GLOBAL_ASM`; the 556-byte C probe remains nonmatching. | **ROM-OBSERVED:** extent SHA in the table and 36 address guards. Probe first differs at `+0x8`; no C promotion. |
| `D68C` — VMA `0x8003D68C`, ROM `0x3E28C`, 812 bytes | No explicit argument reads; returns 32-bit status values 0, 1, or 2. Reads the VM program cursor, pause byte and VM state; calls stream/state helpers and an indirect callback. | `GLOBAL_ASM`. | **ROM-OBSERVED:** all 203 words, 44 anchors and both dispatch tables are guarded. No C model was written. |
| `DDC4` — VMA `0x8003DDC4`, ROM `0x3E9C4`, 132 bytes | `u32(u32 address, s32 entry_resource_id)`. Resolves against the entry ID; on miss, reloads the current global for recovery lookup/retry; final segment query still receives the entry ID. Clears bit 30 from the base and applies the segment/address adjustment. | Matching C in `script_vm.c`. | **G2-MATCHED:** function SHA-256 `f7dab493df8553cae7eb55ce5bbaec5a2cd576e0454dc557dbbadad74a7a101a` matches; current full-image proof passes. G64-029 host test and cached-ID negative control pass, but callback mutation is synthetic. |
| `DF98` — VMA `0x8003DF98`, ROM `0x3EB98`, 528 bytes | Word `$a0` plus signed-halfword cursor `$a1`; returns a cursor pointer. The cursor token is read as `s16`, and values `-71..-32` select the 40-entry dispatch table. Some helper paths forward `$a0`; others load `D_801C7754`. | `GLOBAL_ASM`; header prototype is `s16 *(s32, s16 *)`. | **ROM-OBSERVED:** all 132 words, 54 decoder/caller anchors and 40 table entries are guarded. `$a0` semantic meaning remains **UNKNOWN**. |
| `F038` — VMA `0x8003F038`, ROM `0x3FC38`, 196 bytes | `$a0` is a signed 32-bit lookup index; `$a1` is stored in the caller home area but not read later. Returns a 32-bit zero or resolved value. The routine reads signed halfwords from `D_80077894`; index `0x100` returns zero. | `GLOBAL_ASM`; no C prototype is currently published. | **ROM-OBSERVED:** extent SHA in the table and 49 original-address words / 16 anchors are guarded. The 196-byte native probe is not exact (25/42 direct words and four relocation-layout differences); no C promotion. |
| `F23C` — VMA `0x8003F23C`, ROM `0x3FE3C`, 152 bytes; `F2D4` — VMA `0x8003F2D4`, ROM `0x3FED4`, 124 bytes | Both are no-argument context save/restore paths. They refresh the resource lookup/segment fields and compute the DDC4 start-relative relocation value. | Matching C in `script_vm.c`. | **G2-MATCHED:** proof hashes are respectively `d6d44b0af0c2d08a5e80e9a680ab31b9714e774a75a85bb77bcab265bf020692` and `91bc0fa446b716b14862edfd93ca3c9fa8da196591a49eb05d79c8806b4f67d4`; both remain exact in the live report. |

### Resource-context and shared-global fields

| Field / symbol | Storage type and address | Observed use | Evidence level |
| --- | --- | --- | --- |
| `current_id.word` / `D_801C78E8_1C84E8` | 32-bit word at RAM `0x801C78E8`, context offset `+0`. `script_vm.h` currently exposes the global as `s32`; `VmResourceId.word` is `u32`. | D468 stores the incoming ID. DDC4 reads it afresh after recovery and before retry. Calling it the **current resource ID** is an interpretation of those uses. | **ROM-OBSERVED** access and **G2-MATCHED** DDC4 behavior; storage width is **HOST-LAYOUT**. Signed-vs-unsigned declaration is a source-level distinction to preserve unless separately tested. |
| `n64_be.low_half` / `D_801C78EA_1C84EA` | `u16` at RAM `0x801C78EA`, context offset `+2`. | The original loads this halfword for the recovery call; it is the low numeric half of the big-endian word at `+0`. | **ROM-OBSERVED** load/call and **HOST-LAYOUT** offset/endian assertions. The recovery callback's effects remain **UNKNOWN**. |
| `unknown_04` | `s32` at context offset `+4`, RAM `0x801C78EC`. | Written from the `s32` result of `01E50` in the resource setup/restart paths. “Segment” is a useful call-site label, not a recovered helper contract. | Offset/width **HOST-LAYOUT**; call-site assignment **ROM-OBSERVED** and **G2-MATCHED** for F23C/F2D4; helper meaning partly **INFERRED**. |
| `unknown_08` | `s32` at context offset `+8`, RAM `0x801C78F0`. | Stores the start-relative DDC4 result (`resolved_address - start`) in the matched setup/restart paths. | Offset/width **HOST-LAYOUT**; assignments **G2-MATCHED** for F23C/F2D4. Keep the field name offset-based. |
| `D_80077858_78458` — VM program cursor | `s32` at RAM `0x80077858`. | D468 stores the initial relocated address; D68C fetches 32-bit VM words and advances, branches, or reloads this program-stream pointer. | Program-stream use **ROM-OBSERVED**; “VM program cursor” is a behavior label. |
| `D_801C77E0_1C83E0` — VM state | `s32` at RAM `0x801C77E0`. | D68C reads it to select state paths. | Access **ROM-OBSERVED**; semantic “state” is **INFERRED** from dispatch behavior. |
| `D_801C78FC_1C84FC` — pause byte | `s8` at RAM `0x801C78FC`. | D68C reads the byte on its paused/active path. | Width/access **ROM-OBSERVED** and header-declared; “pause” label is **INFERRED** from control flow. |
| `D_801C7754_1C8354` — decoder context word | `s32` at RAM `0x801C7754`. | DF98 helper-call paths load this word, and the two-call paths reload it between callbacks. | Reload/order **ROM-OBSERVED**; meaning **UNKNOWN**. |
| `D_80077894_78494` — F038 halfword table | Signed 16-bit elements read from ROM-visible RAM address `0x80077894`. | F038 derives a signed halfword index from `$a0` and loads the selected `s16`; resource lookup/retry follows. | Element width, address and access **ROM-OBSERVED**; table schema/meaning **UNKNOWN**. |

The host resource-type test asserts `sizeof(VmResourceId)==4`, low-half offset
`+2`, `sizeof(VmResourceContext)==12`, and word fields at `+0/+4/+8`. These
checks establish C layout only. The current matching C fields and DDC4 machine
code remain protected by the live full-ROM proof; the unresolved D468, D68C,
DF98 and F038 helpers remain assembly. G64-030 selects no new candidate for
promotion.

## Observed edges

```mermaid
flowchart TD
  D310["D310 event start"] --> D468["D468 VM initialize"]
  D388["D388 context start"] --> D468
  D428["D428 reset wrapper"] --> D468
  F564["F564 restart from pending script"] --> D468
  D468 -->|"resource lookup"| WAVE["141C4 wave table lookup"]
  D468 -. "missing entry: callback" .-> RECOVER["13B14 recovery callback"]
  D468 -. "missing-entry path" .-> CFA0["3CFA0 pointer fallback lookup"]
  D468 --> DDC4["DDC4 VM address resolver"]
  D468 --> DE48["DE48 script-pointer relocation"]
  DDC4 --> WAVE
  DDC4 -. "missing entry: callback" .-> RECOVER
  DDC4 -. "missing-entry path" .-> CFA0
  DDC4 --> SEG["01E50 segment query"]
  CFD0["CFD0 scheduled callback"] --> D68C["D68C VM main step"]
  D68C --> DBEC["DBEC paced stream reader"]
  DBEC --> DF98["DF98 control decoder"]
  EB34["EB34 unpaced stream reader"] --> DF98
  ED60["ED60 resource display handler"] --> F038["F038 signed-halfword lookup"]
  F038 --> WAVE
  F038 -. "missing entry: callback" .-> RECOVER
```

Solid edges are direct call instructions in the ROM-derived listing, or calls
in matching C source at this pinned revision. Dashed edges are conditional
calls observed at the stated missing-entry branch. The graph does not imply
that the external recovery routine mutates the VM resource ID.

## ABI, global access and side effects

| Function | Verified ABI and direct effects | Limits / current declarations |
| --- | --- | --- |
| `D468` VM initializer | `$a0` is the initial address word and `$a1` the resource-ID word. It returns 0 when `D_80077860_78460` is null, otherwise 1 after setup. It writes the resource ID at `D_801C78E8_1C84E8`; derives the resource segment and relocation delta; resets VM fields; stores the relocated VM program cursor in `D_80077858_78458`; and clears owner bytes `0x5C` and `0x5D`. It calls `141C4`, conditionally `13B14`, `3CFA0`, `141C4` again, `01E50`, `DDC4`, `DE48`, and `24088(0x82)`. | Current `script_vm.h` declares `void D468(s32,s32)`, although the ROM returns 0/1. All observed callers ignore that result. `D_801C78E8` as a “current resource ID” is an interpretation supported by its use and the matching C resolver, not an engine-level name. |
| `D68C` VM step | No explicit input arguments are read. It returns small status values (0, 1, or 2 along observed exits). It reads the current cursor `D_80077858_78458`, pause byte `D_801C78FC_1C84FC`, and VM state `D_801C77E0_1C83E0`; it dispatches stream, choice, input, wait, comparison, state and relocation helpers. It can invoke the function pointer in `$a2` with `jalr`. | `script_vm.h` declares `s32 D68C(void)`. The only C caller `CFD0` ignores the result. The `$a2` target and its effects depend on VM state; see [VM_MAIN_STEP_TRACE.md](VM_MAIN_STEP_TRACE.md) for the original control-flow map and unknowns. |
| `DDC4` address resolver | Two word arguments: address in `$a0`, entry resource ID in `$a1`; returns the resolved address in `$v0`. It queries `141C4(entry ID)`. If missing, it passes the low halfword at `D_801C78E8+2` to `13B14`, then reads the current full word at `D_801C78E8` for `3CFA0` and reads it again for the retry lookup. The final `01E50` call receives the original entry ID from its saved argument. It clears bit 30 of the returned base and combines that with the address and segment. | Matching C in `script_vm.c` agrees with the visible operations. The meaning and indirect effects of `13B14` are not recovered here. `DDC4` itself does not store to `D_801C78E8`. |
| `F038` halfword-table lookup | `$a0` supplies the signed index/value; its 32-bit result is used by `ED60` as a zero/nonzero test and then as a display-list word. `0x100` returns zero immediately. Otherwise it forms a signed half-index with negative values rounded toward zero, reads a signed halfword from `D_80077894_78494`, and calls `141C4`. On `-1`, it calls `13B14` with the low 16 bits of the saved table value and retries using that saved value. A second miss returns zero; successful values below index 4 receive the computed address adjustment. | Both observed call sites pass `$a1=0`; the body writes that value to the caller home area but does not read it afterward. Do not infer a meaningful second parameter or rename the table without further evidence. The function remains `GLOBAL_ASM`. |
| `DF98` stream control decoder | Callers pass a word in `$a0` and signed-halfword cursor in `$a1`; `$v0` returns the cursor for both callers (`DE80` and `EB34`). DF98 sign-extends `*a1` and dispatches it. It does not inspect `$a0` as data, but several helper calls forward that value unchanged; other paths replace it with `D_801C7754`. | The current header declares `s16 *DF98(s32,s16 *)`. See the G64-028 section in [VM_STREAM_MATCHING.md](VM_STREAM_MATCHING.md) for the dispatch table, caller sentinel obligations, callback ordering and unknowns. |

### D468 stack frame and saved-register lifetimes (G64-026)

The original prologue subtracts `0x20` from `$sp`, then saves `$ra` at
`sp+0x1C`, `$s1` at `sp+0x18`, and `$s0` at `sp+0x14`. The delay slot at
`0x8003D484` stores incoming `$a0` at `sp+0x20`; the entry resource ID is
stored at `sp+0x24` at `0x8003D4AC` for the later `DDC4` call. `$s1` is formed
as the resource-context address at `0x8003D490/494` and `$s0` as the VM-work
address at `0x8003D4B0/4B4` on the normal path or `0x8003D538/53C` on the
clear path. These saved base pointers remain live across nested calls and the
shared reset tail. The epilogue restores `$ra`, `$s0`, and `$s1` from those
slots, returns, and releases the 32-byte frame in the return delay slot.
`test_vm_loader_original.py` now guards the prologue, argument spill, base
construction, saved-register restores, and return sequence (36 original-address
guards total). The 556-byte isolated C probe instead allocates 24 bytes and
saves only `$ra`; its first difference is the frame-size instruction at `+0x8`.
The probe remains research-only and the production function remains assembly.

### Resource lookup and recovery boundary

- At the pinned source, `func_800141C4_14DC4(unsigned int)` is C in
  `src/wave_uty.c`: it scans the 48-entry `D_80167FC0_168BC0` table, returning
  zero for ID zero, the matching entry's data word, or `-1`. This is a read-only
  lookup in that C body.
- `func_80013B14_14714` is declared `int(int)` in `src/wave_uty.c` but retained
  assembly. Its result is ignored by all three VM call paths above. The exact
  callback side effects are **unknown** from this call graph.
- `func_8003CFA0_3DBA0` is matching C and selects an entry from
  `D_80077550_78150` or the fallback `D_8007CCA4_7D8A4`; these VM calls discard
  its return value. No mutation is present in that C body.
- `func_80001E50_2A50` is declared `int(unsigned int)` in `src/wave_uty.c` and
  called with the original resource argument by `D468`/`DDC4`. Its full
  implementation is not inferred from the call sites.
- The recovery tests deliberately mutate the modeled current VM ID between
  callbacks. That is a conservative negative control, **not** evidence that the
  retail callback writes `D_801C78E8`. Preserve the original reloads until the
  callee effects are established.

## Earlier bounded work through G64-028

G64-022 records the observed ID word and offset-only +4/+8 words in
`vm_resource_types.h`; the entry resource argument remains separate from the
mutable global word. Its loader candidate did not match native IDO and remains
unpromoted. G64-023 reproduced the 196-byte F038 baseline; G64-024 tested
three additional source hypotheses without improvement. G64-025 confirmed the
entry-ID/current-ID distinction under synthetic mutation. G64-026 pinned the
original 32-byte loader frame and saved-register lifetimes, but the 24-byte
candidate still differs. G64-027 added a ROM-bound D68C control-flow map and
host-model test matrix; no C candidate was written. G64-028 traced the signed
DF98 decoder and its paced/unpaced caller ordering; no C candidate was written.
No function in this graph is newly promoted by this note.

G64-029 subsequently added a production-body host regression for DDC4 retry
reload and original entry-ID retention; a temporary cached-global mutant is
rejected. G64-030 reconciled the live proof/inventory and added the typed
interface matrix above. No new resource candidate passed G2, and no function
claim or ASM ownership changed. Continue with G64-031, the DBEC text-loop CFG.
