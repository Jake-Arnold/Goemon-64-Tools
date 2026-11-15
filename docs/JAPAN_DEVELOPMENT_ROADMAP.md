# Japanese port work plan — living engineering handoff (2026-11-15)

## Current validated baseline

- The user attached the toolkit directly to Japan revision-0 **Mupen64Plus PID 959604** on Linux using independently checked executable signatures and a word-swapped 8 MiB RDRAM map.
- The 58 Japanese GameShark-derived read-only watches respond as expected in the user's running game. Semantics are not yet completely verified for every entry.
- Scene **300 → 355** and **352 → 354** were observed. Current, previous and pending scene globals behave coherently at stable endpoints. Gameplay submode **1 → 2** was observed once. Pending-scene timing *during loading* remains unknown.
- Japanese character index `0x80161DCC`: **0 Goemon ↔ 1 Ebisumaru**, directly observed in both normal swap directions.
- The user subsequently tested using Cheat Engine: writing `2` or `3` directly to the character index **does not correctly change the playable character**. Writing the Japanese Sasuke/Yae party-availability flags **does unlock native selection**. The resulting genuine Sasuke/Yae index values have not yet been supplied.
- **15 November update:** the user also reports that the two new *toolkit* Sasuke/Yae unlock buttons worked correctly in live Japan-0 Mupen, and the prior party regression suite passed on Ubuntu. The specific read-only character-index values after switching via C-Down were not reported; do not mark Sasuke=2/Yae=3 confirmed yet.
- The Japanese full native Goemon64Recomp executable is **not yet built**. Partial USA↔Japan function correlations and ROM decompression are not equivalent to a runnable port.

## P0: Safe Sasuke/Yae native-character test

**Source PR:** draft branch `chatgptweb/japan-controlled-party-writes`; see `docs/JAPAN_PARTY_WRITE_EXPERIMENT.md`.

**Implementation:** Only opt-in, confirmed one-byte party flags; never direct character index writes; verified read-only connection retained, separate short-lived writable handle; explicit user confirmation and manual emulator savestate as recovery.

**Required external observation:**

| Test | Real character identity | Read-only index expected | Gate |
|---|---|---|---|
| Native C-Down to Sasuke after party unlock | Sasuke model, weapon and normal movement | `00000002` (hypothesis) | Not yet recorded |
| Native C-Down to Yae after party unlock | Yae model, weapon and normal movement | `00000003` (hypothesis) | Not yet recorded |
| Reverse switch back to Goemon | Goemon model, normal controls | `00000000` | Already confirmed for Goemon/Ebisumaru; repeat after new unlock |
| Restore pre-experiment Mupen savestate | Party flags and character revert to snapshot | Return to pre-test values | Not yet recorded |

Only promote value `2` / `3` from **unverified** to **confirmed** after a genuine native in-game switch, not after raw memory edit.

## P0.5: Region-aware read-only research tabs — code delivered, emulator tests pending

Source: same draft PR #17; [full parity checklist](USA_JAPAN_TOOLKIT_PARITY_CHECKLIST.md) and [live testing protocol](JAPAN_READONLY_VALUE_SEARCH.md).

- **Implemented in code:** existing Value Search can now select verified Japanese 8 MiB RDRAM, without assigning it to the USA `self.mem` pointer or enabling any raw writers; includes unsigned/signed/float filters, unknown baseline and custom-watch promotion.
- **Implemented in code:** separate Japan Live typed custom watch list, persisted in a Japan-0-specific JSON file, with read-only value/raw views and baseline comparison. No USA watch list is automatically imported or treated as writable.
- **Implemented in code:** existing Event Sessions → Advanced RAM Comparison supports asynchronous Japan-focused or 8 MiB A/B/C captures, bounded change shortlists, same-session identity and candidate exports. USA persistent Event flag sessions stay disabled for Japan until save-bank layout is validated.
- **Validation outstanding:** execute expanded `./scripts/test_japan_party.sh`; test all three features against real Japanese Mupen and verify connection/savestate cache invalidation. These new tests are not covered by the user's earlier successful party-write testing.
- **Next:** map exact Japanese player/task pointers and XYZ, then investigate the Japanese event-bank layout and 45 Fortune Dolls. Promote only observed semantics to write-capable fields; keep Japanese recomp as a separate effort.

## P1: Japanese player and task pointers

1. Inspect **Japan-native code references** to globals corresponding to USA `PLAYER_OBJECT_PTR_ADDR=0x801FC60C` and `PLAYER_TASK_PTR_ADDR=0x801FC604`. Do not assume `+0x57F0` works on overlays. Use Japan decomp symbol references / disassembly and reverse cross-references.
2. Build a **read-only pointer candidate scanner** for KSEG0/KSEG1 pointers inside RDRAM. Reject null, out-of-range, misaligned, non-finite floats and implausible velocities. Keep any discovery completely separate from the working USA memory parser.
3. Compare read-only position candidates while walking, jumping, standing still and swapping each of the four characters. Validate across at least two unrelated locations and one savestate reload.
4. Independently identify action ID and task character type. Cross-check with the existing USA object layout only where Japanese runtime observations agree.
5. When pointer access is validated, add **read-only XYZ and action** to Japan Live. Defer position writes and warps until the pointers are stable under load/character reconstruction.

## P2: Scene load timeline and story progression

1. Observe candidate current, previous and pending scene variables at short intervals before, during and after several normal doorways. Establish exactly which variables update and in what order; stable endpoint captures are not enough.
2. Validate loading/phase/transition/pause candidates individually, using actual event sessions and time-aligned logs.
3. Catalog 45 Fortune Dolls against the Japanese guides using before/after bitfield experiments. Distinguish silver and gold and verify individual entries. Never infer flag location solely from collection order.
4. Cross-reference 47 TCRF USA actor IDs and their spawn records against Japanese overlay actor tables. IDs may survive region changes, but confirm them in Japanese scenes before labeling UI.

## P3: Playable Japanese native recomp runner

The remaining work is a distinct toolchain and code-generation effort, not a setting on the USA executable.

1. Freeze a legal, local Japan-0 retail ROM input with exact fingerprint; verify decompression reproducibility and section boundaries.
2. Produce native **Japan-specific complete function symbols**, correct overlay layouts, ELF/function metadata, and deterministic instruction relocation tables. Candidate 16-opcode/JAL matches are **not complete native recomp coverage**.
3. Configure N64Recomp code generation for the Japanese ROM and overlays, including audio/threading patches where required; compare emitted symbols and relocation targets with Japan original. Keep the USA runner entirely unchanged.
4. Build a separate `GanbareGoemonRecomp` target and run smoke tests: boot, title, Oedo, NPC dialogue, character switch, first dungeon, Impact and save handling. Document failures with exact overlay/function addresses and commits.
5. Gradually broaden gameplay parity and reproducible Linux builds. Do not claim Japanese ROM runnable until the executable actually boots and plays.

## P4: Next **USA decompilation** session

**Do not lose the independent source record**: draft PR #12 `chatgptweb/usa-external-memory-leads`, `research/usa_external_memory_leads.json` (25 new USA addresses, 47 externally listed actor IDs, four actor-record patterns). Keep those as evidence-only until independently validated. Revisit unused warp flags, boss-rush/sound-test unlock bytes, actor loader routines and Impact patch addresses as separate targeted decomp leads. Continue the existing matching-C promotion and full-ROM/overlay relocation proof workflow; require documented binary identity before claiming a promoted function.

## Version-control and reporting discipline

- **Commit and push after each complete, testable milestone**, not only at the end of a long research session. Each commit should describe the observed behaviour/changed code and its test scope.
- Make an **isolated branch and draft PR** for each workstream, based on the correct parent PR; avoid changing the user's local worktree or merging unvalidated edits.
- Update `PROGRESS.md` **with every material discovery**, including exact addresses, ROM/revision, source provenance, test evidence, uncertainties, observed regressions and the immediate next action.
- Preserve raw, user-supplied RAM traces as machine-readable `research/*.json`; never replace observations with inferred interpretations.
- Use unit tests for byte ordering, field-width/layout, pointer validation, process permissions, and GUI enable/disable gates. Distinguish **local synthetic tests**, **actual user emulator tests**, **GitHub CI results**, and **unexecuted tests** explicitly.
- No background coding or GitHub pushes happen automatically merely because this plan exists. Work is pushed during active development sessions; any separately configured automation is for monitoring, not writing unreviewed game RAM.
