# Goemon USA Script VM and runtime architecture

Research snapshot 2026-11-13. Base `84cf79834f8160953c19e537e66a2950a94dc505` from `origin/chatgptweb/decomp`. The retail and decompressed 32 MiB images matched the SHA-1 pins in [INPUTS.md](INPUTS.md). Guest addresses below use original USA MIPS. For main-segment instructions, subtract `0x7FFFF400` to find the ROM word. The loader, dispatcher, text-window lifecycle, submode classifier, and font ranges inspected here also matched byte-for-byte between the two images. A local decompression check independently reproduced resources 93, 96, and 97 from the retail intervals using the pinned upstream checkout's `lzkn64` dependency.

## A. VM architecture

| Layer | Original behavior |
| --- | --- |
| Load and relocate | `8003D468` records the resource ID, looks up or loads it via `800141C4` and `80013B14`, and stores the bit-30-cleared data base at `801C77FC` (store `8003D4F4`). `80001E50` supplies the segment. `8003DDC4` resolves a segmented address with the resource base and segment. `8003DE48` leaves negative 32-bit operands and segment `-1` alone. For other inputs it adds `801C78F0` modulo 32 bits. |
| Dispatch | `8003CFD0` calls `8003D68C` when its own byte gate at `801C7930` is zero. `D68C` checks PC and pause, updates controller input, and dispatches on the state word before fetching another opcode. Its command stream contains aligned big-endian 32-bit words. The interpreter may execute multiple commands during one call. See the [command and state tables](VM_MAIN_STEP_TRACE.md). |
| Text command | `0x8010` resolves its operand with `DE48`. The call delay slot at `8003D8BC` installs the text pointer at `801C77E8` before calling `8003DBEC`. `D68C` reloads the main PC after that call and, if nonzero, advances it past the operand. The script PC and the text cursor can move independently. |
| Text walk | `DBEC` calls `8003DE80` with the current cursor and window slot, stores the return at `8003DC6C`, and rechecks the VM state loaded at `8003DC68`. States 3–6 stop that text step. With other states it returns to 1 while the cursor is nonzero, or clears the state on null. `8003EB34` is the unpaced reader used for choice labels and generated values. Both walkers read signed big-endian halfwords and recognize `-1` before control dispatch. |
| Render | `DE80` calls `8000D060` for a nonnegative token. `D060` checks the selected window and searches up to 120 render entries. `8000D180` activates an entry with glyph data, selector, position and presentation fields. `D060` increments the window's column field at `+0x6C` and horizontal advance at `+0x6E` by the token width byte plus one. The VM can consume a token even when no entry is available. |
| Pace | `DE80` invokes `8003DF68` before a glyph. A counter at `801C77A0` of at least 2 causes a decrement and a no-emission return. The caller's suppression path then reloads the counter from the setting at `801C7798` at `8003DEE4`. With setting zero after emission, `DE80` can loop through consecutive glyphs in one call. `DBEC` also has a reread outer bound at `801C77D8` and controller-dependent retries. These are per-call rules. In particular, a setting of at least 2 can keep reloading the suppression counter, so a simple frames-per-character conversion would be incorrect. |
| Line, page and choice | Text `-60` calls `8000C3EC` to zero column and x advance, increment the line index and add line height to y. `-63` clears glyph entries and resets layout through `8000D2C0`. `-61` updates presentation fields and enters state 3 via `8003E1A8`. `-62` enters state 4. `8003E3EC` and `8003E4C0` handle continuation and close input. Command `0x8011` calls `8003E6C0` to render option labels and create 20-byte choice records. `8003E888` follows selected-record links at `+8/+0xC`. Confirmation in `E81C` installs the selected record's `+0x10` script continuation at `8003E848`. |
| Branches and callbacks | `0x800A` installs a relocated jump. `0x8006` uses the comparator. `0x8020/21/22` set, clear and test bits at `8015C608` through `80024038/88/DC`. `0x8022` branches when set. `0x800B` advances the PC before calling the raw callback pointer and reloads it afterward. `0x8004` delegates assignment to `DB0C`. Its subopcode `0x8009` stores an immediate to the resolved destination. |

The `-1` sentinel finishes a text record, returning null in the paced reader. A state-changing token can yield before the sentinel. Pages can span several separate `0x8010` commands and can contain separate clear and close records. The [control-token table](VM_STREAM_MATCHING.md) lists renderer callbacks and skip behavior for the other signed values.

### Retail source and loaded offsets

`80001C00` uses one-based IDs 1–1311. For row `id - 1`, source words are at file offset `0x57FD8 + 4*row`, and virtual bounds at `0x556CC + 8*row`. At `80001CB8` a negative source-start word selects `80005394` instead of the DMA path. The loader masks both bounds with `0x7FFFFFFF` to obtain source offsets. The compression flag is on the start word. The next row's flag, present on the end word, does not describe the current row.

| ID | Row | Retail compressed interval | Decompressed image interval | Output CRC-32 |
| ---: | ---: | --- | --- | --- |
| 93 | 92 | `[0x6C1500, 0x6C265E)` | `[0x73F530, 0x743EB0)` | `8E400F63` |
| 96 | 95 | `[0x6C6118, 0x6CA7D2)` | `[0x74ECE0, 0x759DF0)` | `22A5F521` |
| 97 | 96 | `[0x6CA7D2, 0x6CFC1C)` | `[0x759DF0, 0x767640)` | `D0C38E8D` |

All three have virtual start `0x08000000`. For a coherent sample, check that the resource ID, base and relocation describe the same resource, with `segment == 8` and `delta == (base - 0x08000000) & 0xFFFFFFFF` for these examples. Subtract `base & 0xBFFFFFFF` from the cursor and require that the entire word or halfword is inside the output extent and aligned. Add that offset to the **decompressed** image start. The retail source can identify the compressed block. Individual decompressed bytes have no general additive retail-offset mapping. A text pointer may also address generated RAM text, so a failed resource-range check has diagnostic value.

## B. States 5–7

```text
Text -70 → DF98 → E548 → C260 → C6A8 (create window if absent)
                        → state 5 → E5EC ┐
Text -71 → DF98 → E5B8 → C3A0 (close a ready window)
                        → state 6 → E620 ├→ C314(slot) → zero: VM state 1
                                         ┘              nonzero: keep waiting
Command 800B → D68C jalr → F460 → state 7
                           D68C state 7 → E654 → positive: stay 7
                                              → nonpositive: state 0
```

- **State 5 waits for window opening.** `C260` indexes the same three-slot window table at `80167C48` that `D060` uses. It allocates only when the chosen slot is empty. `C6A8` allocates and initializes `0x1818` bytes, sets window `+0x30=1`, stores style and layout parameters, registers the window and clears the glyph entries. Render/update `8000B8B0 → 8000B8F0` dispatches window phases 1–6 via table `8007ABE4` at `8000BA3C`. The opening paths go through `D400/D4E0/D66C`. Depending on the style at `+0x2C`, they expand window dimensions or animate scale before entering ready phase 4 at `8000D6B4`.
- **State 6 waits for window closing.** `C3A0` acts only on an existing window in phase 4. It writes phase 5 at `8000C3D4` and sets a flag. The update path dispatches to `8000D6D0`, which moves supported styles to phase 6, or frees the slot for an immediate-close style. `8000D79C` shrinks dimensions or reduces scale until `8000C878` frees the window. Window phase numbers are separate from the VM state word.
- **Completion is polled immediately and on subsequent VM steps.** Both entry wrappers set state in a call delay slot and immediately call their pollers. `C314` returns 1 for window phases 1–3, 2 for phases 5–6, and zero for a null slot, ready phase 4 or another phase. Both pollers use zero/nonzero and return to VM state 1 on zero. A close request with no ready window may therefore be unobservable in a polling trace. The dispatcher has a fall-through check for zero, while the verified successful poll stores 1.
- **State 7 is a script-programmed wait.** `F460` copies the script-controlled word `801C7740` into `801C77F8` and stores state 7 at `8003F47C`. `E654` decrements once per eligible state-7 VM step. If the signed result is nonpositive, it clears state and clamps the countdown to zero. The dispatcher returns 1 after the handler even on the step that clears the wait. It fetches more commands on a later step. The clock unit established here is a VM step that passes the outer gate, PC and pause checks. A mapping to VI ticks or wall time needs a runtime cadence trace.
- **The resource supplies the presentation meaning.** Resource 93's castle title candidate opens the window at command `+0x43A8` (operand points to `-70`), emits the title at `+0x43B0/+0x43B8`, sets the count to 120 at `+0x43C0` and calls `F460` at `+0x43D0`. Resource 97's cinematic commands at `+0x9620/+0x9680/+0x96B0` call the same callback after setting 60. Both place the next-command PC before entering the wait. `E654` never writes the PC. Across sparse samples with state 7 at both endpoints, countdown completion, text work, PC movement, and re-entry into another wait can all occur between readings.

## C. Dialogue extraction and runtime regressions

The width table is at `8005BB10` (image `0x5C710`). `D060` chooses glyph data at `800629A0 + 48 * (token / 2)` and combines the window's `+0x24` field with `token & 1` for the selector. The 48-byte block has 12 rows of four bytes. For glyph parity `p` in each byte, read the two-bit samples at shifts `4 + 2*p` then `2*p` to view the eight columns. Reading both planes in token order identifies space at 0, digits at 16–25, uppercase at 33–58 and lowercase at 65–90. The decoder covers identified punctuation and preserves other IDs, including palette/style controls such as `-33/-32`, as numeric tokens. A uniform ASCII conversion would miss punctuation exceptions and style tokens.

Run the single-record decoder locally with the pinned image. Use `--summary` to reproduce offsets and the record digest without displaying text. The CLI also accepts a resource-relative `--text-offset` for a known record. It requires an aligned, in-bounds operand and a sentinel within the resource and 4096 halfwords.

```sh
python3 -m decomp.vm_dialogue PATH_TO_DECOMPRESSED_USA_Z64 97 --command-offset 0x9608 --summary
```

| Regression | Recovered evidence | Runtime confidence |
| --- | --- | --- |
| Zazen Gate, resource 97 | Command `+0x9608` (image `0x7633F8`) references `0x08000004`, giving text at `[0x759DF4,0x759E24)`, 23 tokens before sentinel. The first glyph token `57` is Y. The same cluster contains more Yae/Goemon dialogue, including a record at `+0x58` ending with the `-60` line break and its continuation at `+0x8C`. | State-7 resume PCs `+0x9628/+0x9688/+0x96B8` match the recorded PCs with inferred base `0x803A5780`. The three state-1 PC observations map to `+0x9610/+0x9670/+0x9698`, immediately after text commands. The raw loaded base still needs live confirmation. |
| Oedo old man, resource 96 | `+0x8C58` tests story bit 2 and branches to `+0x8CA0`. The branch paths set and clear bit 2 at `+0x8C8C/+0x8CC0`. The state-3 and state-4 resume PCs are `+0x8C74/+0x8C9C` and `+0x8CA8/+0x8CD0`, respectively. First-page ending streams are at `+0x1CC0/+0x1D38`. Both final pages use `+0x180`, which contains the state-4 token, the close-window token, and the sentinel. | All four reported PCs fit base `0x803A2880`. The same spacing also occurs in a separate resource-96 script with flag `0x17`; flag 2 and readable old-man dialogue discriminate the candidate. |
| Castle title, resource 93 | Window-open next PC `+0x43B0` and wait next PC `+0x43D8` differ by `0x28`. Other resource-93 routines have the same spacing, but the two title records at `+0x1894/+0x18AC` identify the castle sequence. | The two sampled PCs imply base `0x8039F740`. Text can become visible between separate polls before the wait, so a sample's presentation and state should be correlated at instruction or frame boundaries. |
| Chain Pipe and Oedo Castle bridge | Cursor movements are compatible with a sequence of commands and operands followed by state 4. The relative spacing alone admits multiple command chains in resource 96. | Obtain the loaded base and paired text/PC bytes to resolve the candidate. |

The demo digest is `6428e00a0211ee021f889900f1a189492b015dbfb9642ff9bbb2b18f7c83a559`, covering the record including its sentinel. Text transcripts, atlas previews and original assets stay local. The decoder extracts a bounded record and does not traverse complete scripts, execute callbacks or reconstruct conditional conversations.

## D. Read-only capture specification

Start with a separate diagnostic sampler against the already-validated RDRAM adapter, using `read_guest` for endian-normalized bytes. Use a 10 ms polling target for a 30-second trial, a 4096-event ring and a dropped/unstable-sample counter. Emit the first sample, then emit on change of map, submode, state, resource, either cursor, base, segment, delta, pause or countdown. Record monotonic start and finish time in nanoseconds, sequence number, changed-field mask and old/new cursor values. Include the adapter type and sampling mode in the header.

| Guest address | Width | Capture field |
| --- | --- | --- |
| `800C7A94 / 800C7AA4 / 800C7AB2` | 8 / 8 / 16 | Top-level state, submode, map |
| `8015C5C8 / 8015C5D4` | 32 / 8 | System pointer sentinel and loading flag |
| `80077858 / 801C77E8` | 32 / 32 | Main PC and text cursor |
| `801C77E0 / 801C78E8 / 801C77FC` | 32 each | State, resource ID, loaded data base |
| `801C78EC / 801C78F0 / 801C78FC` | 32 / 32 / 8 | Segment, delta and pause |
| `801C7740 / 801C77F8` | 32 each | Script wait input and active countdown |
| `801C7754 / 80167C48 + 4*slot` | 32 each | Optional window slot 0–2 and validated window pointer |
| Window `+0x30/+0x6C/+0x6E` | 16 each | Optional phase, column and x advance |
| `801C7800`, selected record `+0x10` | 32 each | Optional state-2 choice pointer and branch target |

1. Read fixed fields in small contiguous groups, including a single VM-context read `[801C77E0,801C7900)`. Require the system pointer `8008CCC0` and a loading byte of 0 or 1. Read at most 16 bytes forward at each cursor on a candidate event. Require guest RDRAM bounds, alignment, a compatible mapped host range and room for the entire read. Cap samples at the resource end when the mapping is known. Record absent, invalid or unreadable pointers as such. An out-of-resource pointer can still be valid RDRAM and should be identified as such.
2. Reread fixed fields and compare the keys and countdown after reading pointer samples. Keep unstable events flagged or retry once. Equal bracketing values reduce the chance of mixing resources but cannot prove a same-frame snapshot or detect an ABA transition. The polling trace can miss short-lived states or several writes to the same pointer.
3. For writer attribution use a debugger or emulator with read-only guest store observation. Capture guest writer PC, old/new store values, and a frame or guest-step ID for writes to `80077858`, `801C77E8`, `801C77E0` and `801C77F8`. On a paused guest or an in-thread callback, gather the fields at a documented instruction boundary, accounting for branch delay slots. `D52C` installs the initial PC, `D894` advances it before a native callback, `D8BC` installs a text stream, `DC6C` publishes the walker return, `E848` installs the choice continuation and `F47C/E670` set/clear state 7. Use a post-step or end-of-frame capture alongside the store trace for a consistent view of a completed transition.
4. Stop on deadline, invalid global sentinel or loss of the RAM mapping. Store records under ignored `practice/diagnostics/`. Capture neither full memory nor actor regions. Use synthetic big-endian and word-swapped buffers to check bounds, torn-read handling, duplicate suppression and ring eviction before a live session. During a replay, compare valid cursor samples with the corresponding decompressed resource bytes.

## E. Gameplay submode and Impact

The gameplay scene initialization path calls `8000B364 → 8000B3E4` at `80002EC4` before setting top-level state 13 at `80002EE4`. `B3E4` clears the submode byte at system base `+0x3ADE4`, reads the map as `u16` from `+0x3ADF2`, and stores `i-1` for the first threshold strictly greater than the map. With the observed system base these fields resolve to `800C7AA4` and `800C7AB2`. The threshold table at `8005BA10` (image `0x5C610`) is `0,300,350,400,540,544,549,561,588,607,613,618,619,620`. Map IDs at or above the final threshold retain the initial zero on this path.

| Submode | Map interval on this path | Runtime examples |
| ---: | --- | --- |
| 0 | 0–299 | Dungeons including castle map 168 |
| 1 | 300–349 | Overworld |
| 2 | 350–399 | Towns, including Oedo 353 and Zazen 359 |
| 3 | 400–539 | Interiors, including South Oedo House 451 |
| 4 | 540–543 | Impact gameplay sample at 540 |
| 7 | 561–587 | Impact intro/transition sample at 569 |

This proves the numerical classification of the sampled maps on the common initialization path. It does not give original enum names or prove a one-controller-per-submode dispatch. Main-segment readers at `8003236C/800326A4/80032898` gate ordinary linked-object processing on mode <4. `8003729C` gates another operation on modes 1 or 2. The native debug menu reads and writes the same byte for its category selection, so record top-level state with each sample. Special scene callbacks and actor lifetimes need a separate bounded overlay trace.

`snapshot_for_monitoring()` retains validated global RAM access and clears ordinary player fields on missing/invalid player data. The toolkit keeps its handle, clears player display values, and cancels pending player-dependent operations. A/B/C capture reuses the tolerant snapshot or requests one, reads global ranges, and conditionally reads bounded dynamic regions. The synthetic monitoring and Tk capture tests exercised the `0xA4600014` case and verified that strict snapshot still rejects it. No new live Impact capture was performed. There is no evidence for dereferencing that value as an Impact actor. Existing checkpoint gates remain strict.

## F. Five follow-ups

| Priority | Targets and expected result | Verification and stopping condition |
| ---: | --- | --- |
| 1 | `Rdram.read_guest`, the capture design above, and map 359. Pair both cursors with base, delta and writer address across a wait. | Compare sampled bytes to resource 97. Stop after the first wait expires and the next text command maps, or after a bounded session yields a specific capture failure. |
| 2 | Resource 96, map 353, flag `0x002`, `E3EC/E4C0`. Verify both old-man paths and the inferred base. | Record A1/A2/B1/B2 with text pointer and flag in one run. Stop after all four captures agree with the candidate or a coherent capture disproves it. |
| 3 | `decomp.vm_dialogue`, `D060`, `C53C` and the atlas. Extend glyph and style coverage only for unknowns observed in actual records. | Inspect the actual glyph planes and palette selectors and test a sample containing punctuation, style switches and a line break. Stop at the end of the observed token set and preserve unknown IDs numerically. |
| 4 | `D68C/DB0C/D9B8/E6C0/E81C` and resource 96 choice/flag entries. Recover a bounded script graph with conditional and choice edges. | Verify flag-2 branches and both selected targets from one choice prompt against bytes and runtime evidence. Stop at unknown callbacks, external operands or configured node bounds. |
| 5 | `B8F0` phase table, `CFD0/D68C/E654`, plus Impact modes 4/7. Check the window and wait cadence and repeat the A/B/C Impact capture. | Observe an opening, a closing, one countdown expiry and successful global-only Impact comparisons in a controlled replay. Stop when these are measured or the debugger/process adapter limit is identified. |
