# USA gameplay submodes and script VM — live observations (13 Nov 2026)

This is a **read-only observation log**, not a reconstruction of the original game's state enum. Screenshots and video were inspected while using the native Goemon Practice Toolkit. Runtime values can be sampled between native instructions; a screenshot never proves a complete state transition. No ROM, dialogue transcript, video, screenshot, or raw RAM dump is committed here.

## Relevant globals

| Guest address | Read as | Meaning / evidence |
|---|---|---|
| `0x80077858` | u32 | Script cursor storage (value is a RAM pointer, not a ROM offset) |
| `0x801C77E0` | u32 | Script VM state/dispatch word |
| `0x801C78E8` | u32 | Active script resource ID, often `0xFFFFFFFF` after interaction |
| `0x801C78FC` | signed byte | VM pause byte; semantics incomplete |
| `0x800C7A94` | u8 | Top-level game state (10 debug menu, 12 reload, 13 gameplay) |
| `0x800C7AA4` | u8 | Context-dependent submode; debug-menu category when top-level state=10 |
| `0x801FC60C` | u32 | Ordinary player-object pointer; **not reliable in all scenes** |
| `0x801FC604` | u32 | Ordinary player-task pointer; **not reliable in all scenes** |
| `0x8015C5DC` | u32 | Ordinary playable character ID; **not reliable in all scenes** |

## VM states (observed associations, not proven exclusive meanings)

| Value | Runtime association | Limits |
|---|---|---|
| 0 | Typically idle/no active text presentation | Transient 0 possible amid visible scripted dialogue; cursor 0/resource -1 after closing |
| 1 | Progressive dialogue/text rendering | Cursor advances in discrete jumps while state remains 1 |
| 2 | Interactive selection | Independently observed at rice-ball shop (resource 107), Adventure Diary save Yes/No (102), Pemopemo God Yes/No (102) |
| 3 | Ordinary dialogue page complete, A continues | Tested old-man and other dialogues |
| 4 | Ordinary final page complete, A closes | Tested old-man and Chain Pipe notice |
| 5 | Brief phase before state 7 on a castle area-name notice | Exact function unverified; early text already visible |
| 6 | Briefly observed in one video by user | No reliable paired cursor/resource/scene; **unknown** |
| 7 | Area-name notices **and scripted/cinematic dialogue** | Not unique to location labels; cursor can advance while state remains 7 |

## Repeatable cursor / resource observations

- Oedo Town old man (map **353**, resource **96 / 0x60**): dialogue A pages at cursor `0x803AB4F4` (state 3) and `0x803AB51C` (state 4); dialogue B at `0x803AB528` (state 3) and `0x803AB550` (state 4). A1→A2 and B1→B2 each `+0x28`; B minus A corresponding cursor positions `+0x34`. Dialogue closes to state 0, cursor 0, resource `0xFFFFFFFF`. This does **not** prove cursor points to literal text bytes.
- Chain Pipe notice (resource **96**): observed `0x803ACE48` → `0x803ACE58` → `0x803ACE60` → `0x803ACE68`, state 1 during progression and 4 at completion; sampled increments `+0x10,+0x08,+0x08`. Video replay repeated the sequence.
- Oedo Castle bridge dialogue (resource **96**): `0x803B2198` → `0x803B21A0` (state 1→3) → `0x803B21B0` → `0x803B21B8` → `0x803B21C8` (state 4). Cursor can remain steady as multiple characters render.
- Shop selection (resource **107 / 0x6B**): choice cursor `0x803859D8` persists in state 2 despite moving highlight; after selection, state 1 cursor `0x80385AD8`.
- Adventure Diary (map **332**, resource **102 / 0x66**): state 2 at `0x803B5DB8` while Yes/No prompt is displayed.
- Pemopemo God (same map and resource): state 2 at `0x803B6464` while Yes/No prompt is displayed.
- Area labels: Ugo Stone Circle state 7, resource **115**, cursor `0x803AC134`; Mutsu Shoreline state 7, resource **91**, cursor `0x803AB684`. The stable cursor during each notice does not establish an exclusive state-7 purpose.
- Gorgeous Musical Castle entrance (map **168**, resource **93 / 0x5D**): state 5 at `0x803A3AF0` followed by state 7 at `0x803A3B18` (`+0x28`). Location text was already visible during state 5.
- Zazen Gate scripted dialogue (map **359**, resource **97 / 0x61**): observed cursor `0x803AED90` (state 1) → `0x803AEDA8` (state 7) → `0x803AEDF0` (state 1) → `0x803AEE08` (state 7) → `0x803AEE18` (state 1) → `0x803AEE38` (state 7). A separate part of that recording sampled resource 97/state 7 at both `0x803AF2EC` and `0x803AF3D4` (`+0xE8`); intervening states may have been missed.

**Hypothesis:** the script cursor advances between instructions or text-associated records, not once per rendered character. Resource IDs appear to define a broader stream context. The pointer's exact meaning, the RAM→ROM mapping and the underlying 16-bit VM instructions all still need original MIPS validation. A forced cursor-write attempt was inconclusive and is **not evidence**.

## Gameplay submode at 0x800C7AA4 (not VM state)

This is one context-dependent byte, **not a universal enum**:

- In top-level state 10, its documented values 0–4 select native debug-menu categories MAIN, SIRO, DOUCHU, MACHI, SHOP.
- In top-level state 13, the user has documented value **0** in dungeons: Oedo Castle, Muscle Castle, Ghost Toys and Submarine.
- Value **1** is associated with overworld areas, including Bizen and Ugo Stone Circle.
- Value **2** is associated with towns/villages, repeatedly recorded in Oedo Town, Zazen Town and FolkyPoke Village.
- Value **3** is associated with houses and other interiors. The 21:29:22 recording independently shows **map 451 / 0x1C3, South Oedo House (Man c3)**, top-level state 13, gameplay submode **3**.
- Impact-related sequence: a screenshot at map **569 / 0x239** showed top-level 13 and submode **7** during the intro/transition; map **540 / 0x21C** showed top-level 13/submode **4** during Impact gameplay. These observations support, but do not fully establish, a special-mode progression.
- These are observed scene-category associations, **not MIPS-verified enumeration names or proof of exclusivity**. Other values remain unknown. Checkpoint restoration historically refuses value 3 and values 4+ as a conservative safety gate; the new interior association does **not** justify removing that gate without a separate safety analysis.

## Title screen and Impact player-pointer failure

The final five seconds of a 73-second 21:14:54 recording show the toolkit status:

`Memory read failed: Invalid player object pointer 0xA4600014`

The game was still running. The same type of issue is reported on the title screen: a nonzero ordinary-player field can be meaningless without an active normal player. Previously, `snapshot()` raised a `ValueError` and `Toolkit.tick()` discarded `self.mem` on every `ValueError` or `OSError`. This conflated unsafe player data with actual RDRAM failure.

The toolkit's **read-only monitor** now uses `snapshot_for_monitoring()`. It keeps the validated game connection and global watches when ordinary player data is absent, clears player-dependent coordinates/action/character fields, cancels pending restore/warp actions and resumes normal player sampling once a valid player appears. Strict `snapshot()` remains unchanged for gameplay operations. An invalid system pointer or loading flag remains a fatal validation failure.

### Questions remaining for decompilation

1. Determine original MIPS writers/readers of the script cursor, state and resource ID.
2. Verify state-2 choice index/branch dispatch and whether state 7 is a timed/automatic-wait or broader cutscene state.
3. Establish script resource-relative offsets and RAM→ROM location with relocation.
4. Identify the full game-mode/submode dispatch table, including the Impact controller.
5. Identify special-mode player-object storage independently; do **not** reinterpret or follow `0xA4600014` as a normal player pointer.

## Live Memory UI labelling (toolkit feature branch)

The inspector now displays **qualified user-observed hints** for VM states 0–7 and gameplay submodes 0, 1, 2, 3, 4 and 7. It keeps the raw hexadecimal values visible. State 6 remains explicitly unknown; other submodes remain unmapped. When the top-level state is not gameplay (13), it explicitly avoids interpreting the byte as a gameplay mode. The top-level native debug menu still decodes its own independent category enum. None of these hints constitute original MIPS proof.

## Impact State Discovery A/B/C (read-only) follow-up

The user reported that Capture A and Capture B fail with an invalid normal player object pointer during Impact encounters. A/B/C compared global RAM blocks; the initial implementation called strict `ram.snapshot()` when `Toolkit.current` was cleared by special-mode monitoring, making those comparisons fail even while the RDRAM link and global watches were valid.

The integration branch uses `snapshot_for_monitoring()` for read-only state captures, treats the current character as unknown when the normal ID is out of range, and skips optional player task/object regions when their pointers are invalid, unreadable or absent. Focused global regions remain mandatory and can be compared across Impact/title/normal scenes. This does not make player-dependent writes, checkpoint restoration, or dynamic pointer interpretations safe.

## Impact boss resource-value observations (14 Nov 2026)

The user reports verifying the following values during an Impact boss encounter with the toolkit's read-only custom watches:

| Displayed resource | Guest address | Read width | Live examples | Evidence confidence |
| --- | --- | --- | --- | --- |
| Impact Ryo | `0x802F7066` | unsigned 16-bit | 196 (`0x00C4`), later 400 (`0x0190`) | User-verified matching displayed Ryo within a fight |
| Impact oil / health | `0x802F706A` | unsigned 16-bit | 40 (`0x0028`), later 600 (`0x0258`) | User-verified matching displayed oil within a fight |

The offsets are four bytes apart. **Storage-width hypothesis:** since these guest addresses both have offset `+2` inside four-byte-aligned words, the user may have found the low halves of two adjacent unsigned 32-bit resource counters at `0x802F7064` (Ryo) and `0x802F7068` (oil). In big-endian memory, `u32 600` appears as `00 00 02 58`, and `u16` read at byte offset 2 returns 600. This is an unverified structural inference; adjacent fields could have other widths or layouts.

**Next validation:** make additional **read-only** `u32` watches at `0x802F7064` and `0x802F7068` during Impact, confirm changing amounts alongside their corresponding `u16` watches, then repeat in a freshly started fight and another boss. Do not promote fixed addresses to general-purpose global resource mappings until allocation/scene scope is understood. These discoveries do **not** yet identify enemy HP. Existing normal-player pointer limitations remain separate.

### Full-width Impact resource validation (14 Nov 2026)

Four further screenshots of the Thaisamba 2 Impact boss battle show that the earlier `u16` watches were reads of the **low 16 bits of three consecutive 32-bit big-endian fields**. Full-word `u32` custom watches at the preceding aligned addresses match the game HUD:

| Field | Verified `u32` watch address | Evidence samples | Prior low-half `u16` watch |
| --- | --- | --- | --- |
| Enemy boss HP | `0x802F7060` | 2000 → 1995, matching displayed enemy 2000 → 1995 | `0x802F7062` |
| Impact Ryo | `0x802F7064` | 200 → 186, matching displayed Ryo 200 → 186 | `0x802F7066` |
| Impact oil / health | `0x802F7068` | 400 → 320 → 250, matching displayed oil 320 → 250 and earlier 400 | `0x802F706A` |

**Confirmed for this fight:** the `u32` values correlate with and match their corresponding HUD counters. The user separately reports that editing these runtime resource values also changes the corresponding in-game variables, further supporting their functional identity. The boss HP decrease by 5 is visible in the final screenshots. This upgrades the former two-field `u32` hypothesis to a three-field observed layout with 4-byte spacing, 12 bytes total.

**Not yet established:** the actual original MIPS access width (reads at `+2` may still be intentional), whether this is a globally fixed structure or a dynamically allocated instance, which original instructions read/write it, stability across restarting the game and across boss encounters, or whether every Impact boss uses exactly the same layout. Until independently verified, keep addresses as **Impact battle / screenshot-verified observations**, not unconditional universal game globals. The older `u16` hits remain valid low-half representations but should not be described as evidence that the native fields are only 16 bits wide.

### Special-attack charge and cross-boss stability (14 Nov 2026)

The user has now independently tested the three original full-word counters across **all Impact boss fights tested** and after **restarting the game**: `0x802F7060` enemy HP, `0x802F7064` Impact Ryo, and `0x802F7068` oil/health continued to match the corresponding in-game values at the same addresses. The user had also confirmed that editing these runtime values changes the expected corresponding resource. This supports calling the three addresses **stable, user-validated Impact resource fields**, rather than merely single-encounter candidates. The original MIPS owners/readers/writers remain unidentified.

A fourth field was found during the boss fight:

| Candidate field | N64 guest address | Observed reading | Behaviour |
| --- | --- | --- | --- |
| Impact special-attack charge | `0x802F706F` | `u8`: 0, 50 (`0x32`), 86 (`0x56`) | Increases as the charge bar fills; drops/resets to zero after the special attack is used |

The screenshots show this value changing alongside the charging mechanic. Its exact charge maximum, whether intermediate values correspond linearly to the visible meter, and the underlying original MIPS field width have not been established. Because `0x802F706F` is byte 3 within the aligned word beginning at `0x802F706C`, it could be a standalone byte or the low byte of a `u32` counter (or part of some other layout). A **read-only** `u32` watch at `0x802F706C` would distinguish common possibilities: it should equal the `u8` watch if the upper 24 bits are consistently zero, but that agreement alone cannot prove the original MIPS uses 32-bit accesses.

Observed offsets from the stable resource block base `0x802F7060`: enemy HP +0x0, Ryo +0x4, oil +0x8, special-attack charge byte +0xF. These are address relationships, not yet a verified C struct. Existing normal-character pointer validation remains independent; the toolkit's special-mode monitoring must not treat these addresses as ordinary player objects.

**Next research focus:** find original MIPS reads/writes of this 16-byte region, confirm field widths/charge reset, and distinguish fixed globals from a consistently allocated battle struct. Do not imply that a charge maximum of 100 or any particular threshold has been confirmed.

### Full-width special-charge field validation (14 Nov 2026)

The user added a 32-bit unsigned watch at **`0x802F706C`** and compared it directly with the original 8-bit watch at **`0x802F706F`**. Both showed **79** at the same time (`u32 0x0000004F` and `u8 0x4F`), and the user reports the two readings remain identical throughout repeated charging and discharge. Consequently, the value at `0x802F706F` is consistent with the low byte of a **fourth aligned 32-bit value**. This is a strong runtime-supported 32-bit representation, not yet MIPS proof of the native instruction width.

The user additionally verified the special charge has an observed gameplay range **0 through 100**. Firing one Ryo shot increases the *special-attack charge counter* by exactly **1**; other game actions also increase or decrease it. Executing the charged special attack resets the value to **0**. The exact other actions and thresholds remain to be enumerated; this refers to charge, not an increase in the Ryo currency balance.

The now-observed contiguous 16-byte resource region is:

| Offset | N64 guest address | Read type | User-validated field |
| --- | --- | --- | --- |
| `+0x00` | `0x802F7060` | `u32` | Current enemy boss HP |
| `+0x04` | `0x802F7064` | `u32` | Impact Ryo balance |
| `+0x08` | `0x802F7068` | `u32` | Impact oil / health |
| `+0x0C` | `0x802F706C` | `u32` | Special-attack charge (0–100 observed) |

The first three addresses have been confirmed by the user across all Impact bosses tested and after game restart. A similar multi-boss/restart test of the **fourth** aligned field has not been separately established. For all four, actual native access widths, precise struct ownership, reset semantics across modes and original code-level writers/readers remain to be traced. This section supersedes the earlier statement that the 100 maximum and fourth-width hypothesis were unverified.

## Interactive dialogue-menu selection candidate at 0x801C792C (14 Nov 2026)

Two native Recomp/toolkit screen recordings were inspected at approximately 0.5-second sampling resolution:

- **Inn, 10:07:33 clip (~14 s):** a `u32` custom watch at `0x801C792C` follows the red highlight through three options: `0 = Spend the night`, `1 = Adventure Diary`, `2 = Nothing`. Repeated forward/reverse menu movement reproduces the values; occasional single-frame discrepancies are consistent with non-atomic toolkit/UI/recording timing. The word reads `0xFFFFFFFF` (`4294967295`, signed −1) before choice presentation and after the menu closes.
- **General Store, 10:08:01 clip (~21 s):** the same field switches among `0, 1, 2` during the shopkeeper's visible *introductory text*, even while no selection labels are displayed. It also reads `0xFFFFFFFF` in non-choice portions and at least one sampled frame showing a two-option purchase prompt. In a later Yes/No prompt, `0` was seen; no complete verified mapping of both displayed choices was captured.

**High-confidence scoped result:** `0x801C792C` is a zero-based index matching the inn's highlighted choice, with `0xFFFFFFFF` plausibly indicating unset/inactive. **Not yet verified:** universal applicability to every NPC choice menu, original MIPS access width/writers, how the value interacts with VM state 2 and choice record `0x801C7800`, and whether movement inputs can update a latent selection while unrelated dialogue is rendered. In particular, the shop recording rules out treating `0xFFFFFFFF` as an absolute proof that *no* choice is visible.

**Next capture:** monitor `0x801C792C` as `u32` alongside VM state `0x801C77E0` (`u32`) and choice context `0x801C7800` (`u32`, semantic interpretation not yet established). Record inn / general-store / another unrelated NPC choice at selection-open, every arrow movement, confirm/cancel and close. Compare both options of a Yes/No menu, test arrow movement during text-only frames, and confirm reset/initialization across new interactions. Read only; do not infer an event-flag or edit this field until dispatcher writers and branch semantics are verified.
