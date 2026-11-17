# Original-USA 346 + 47 C = 393 native promotion candidate

**Checkpoint 2026-11-17: proven exact source-compiled complete USA ROM and standalone original-symbol inventory, but the final current-source `decomp.verify` + full `decomp.local_ci` gates are outstanding. Do not describe these as canonical 393 production C.**

The live USA production base independently advanced from 342 C to **346 C / 17,720 instruction bytes** through four separately verified `file_11` functions (152 bytes) under the published `goemon-file11-183-central-v1` stage. This change supersedes the earlier 389-C target. All four were recompiled from the exact current production fixture, and all four source and staged-object SHA-256s were verified, then linked to the original complete USA ROM.

The **47 new previously unpromoted original-address C functions / 2,220 bytes** live in `decomp/research/jp_recomp_to_c/src/`, covering file_12 (5), file_13 (15), file_14 (8), file_15 (2), file_17 (1), file_18 (9), file_19 (7). Their reviewed original addresses, exact original ROM code SHA-256s, source SHA-256s and original sizes are pinned in `decomp/research/jp_recomp_to_c/overlay47_promoted_manifest.json` (v2). No overlap with the four new canonical file_11 functions or any other 346-C claims.

## Native 393-C results — all passed

| Property | Native result |
| --- | --- |
| Original expanded USA ROM | **33,554,432/33,554,432 bytes exact**, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494` |
| Base canonical | **346 matching C / 17,720 source-code bytes** |
| Newly integrated | **47 matching C / 2,220 source-code bytes** |
| Combined native | **393 matching C / 19,940 source-code bytes** |
| Original positive-sized ELF functions | **7,376/7,376**, original names, addresses and sizes preserved |
| ASM functions remaining | **6,970** |
| Newly introduced aliases | **zero** |
| Inherited original-to-canonical size annotations | Two preexisting, unchanged |
| `file_11` semantic relocation tuples | **8,825 / 8,825 exact** |
| `file_12` | **7,051 / 7,051 exact** |
| `file_13` | **9,589 / 9,589 exact** |
| `file_14` | **3,041 / 3,041 exact** |
| `file_15` | **1,625 / 1,625 exact** |
| `file_17` | **1,739 / 1,739 exact** |
| `file_18` | **3,365 / 3,365 exact** |
| `file_19` | **1,078 / 1,078 exact** |
| Combined linked native ELF SHA-256 | `57bd38215d722154a1d62621093616f81dc222d6520d4646d5c15c83eba86f8e` |
| Source-stage negative-control tests | **7/7** with original ROM |

The newly rebuilt **346-C** native ELF SHA-256 is `02e355ab8765881608f27982e33e3b6895e6d042bba6c396837dde5ddd16bfdc`. The native build removes only verified zero-only compiler/ASM object alignment beyond the named original MIPS instructions. The exact full 32 MiB ROM, all positive ELF function identities and every semantic relocation table were independently compared. Local original sources and proprietary objects are not committed.

`decomp/overlay_crossregion47.py` provides the versioned v2 original-ROM adapter. `decomp/verify.py` integrates the adapter only *after* a complete 346-C original-ROM proof, checks original ownership and fails closed on overlap, compiles the source-owned functions, re-links the original game, checks all symbol/relocation data and adds exactly 47 C claims. A portable source/ROM guardrail test `decomp/test_overlay_crossregion47.py` accepts an optional private ROM through `GOEMON_USA_DECOMPRESSED_ROM`.

## Not yet accepted as canonical production

The native original-ROM proof was executed on a full pinned local source reconstruction using the actual 183-function file_11 fixture and verified IDO objects. It is **not** the same as a successful fresh invocation of the entire updated `python3 -m decomp.verify` production pipeline. The complete latest-source `python3 -m decomp.local_ci` has not yet been recorded passing with this manifest change; existing snapshot tests/ledgers need matching 393 reports first. The checked-in `decomp/results/combined.json` and `decomp/results/inventory.json` are intentionally still the published canonical **346-C** proof until full current-source verification succeeds.

Formal promotion requires successful new `decomp.verify` native G2, standalone `decomp.inventory` and full `decomp.local_ci` on the same source tree, then producing fresh canonical 393-C proof JSONs and ledger hashes. This branch remains draft until that acceptance. Japan rev-0 is separately **34-C** and unaffected.

Evidence: `decomp/results/native_393_standalone_inventory_20261117.json`.
