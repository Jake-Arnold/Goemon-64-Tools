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
