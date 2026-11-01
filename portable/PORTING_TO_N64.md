**Important v0.9.8 correction:** The pending-map + exit-flag approach described in old archive notes sends Goemon64Recomp back to the title screen; it is **NOT a functioning direct warp**. Do not use or port that procedure.

# N64-first architecture for the Goemon practice toolkit

Target: original **Mystical Ninja Starring Goemon (USA)** code, including potential ROM hacks. The PC recompilation is **only a host adapter**. No `recomp_*`, `N64Recomp`, SDL, RmlUi, Win32, Python, LiveSplit, filesystem, or emulator-only symbols are used by the portable C checkpoint core.

## Shared guest-state contracts

- `goemon_checkpoint.h` declares a fixed-size in-RAM checkpoint and a small `read`/`write` callback interface.
- `goemon_checkpoint.c` reads and writes original N64 virtual addresses. The callbacks must transfer **guest byte order**, not word-swapped PC bytes.
- `practice/checkpoints.py` uses the **same original-game addresses** but serializes checkpoints in a versioned, SHA-256-protected, host-independent JSON format. **These formats are not yet binary interoperable**; C checkpoint structs are an in-memory proof of concept. A cross-platform wire-format converter will be needed later.
- `autosplitter/` continues to be a host-side LiveSplit adapter. Actual ROM mode should expose game event IDs or flags through a separate reporting channel, not depend on a PC timer process.

## Original game memory fields used

| N64 virtual address | Bytes | Purpose |
| --- | ---: | --- |
| `0x8015C5D8` | `0x30` | Live resource/status block (HP, Ryo, lives) |
| `0x8015C608` | `0x304` | Primary game-save data, including event flags, inventory/progression |
| `0x8015C910` | `0x304` | Save shadow buffer, synchronized on restore |
| `0x8015CC18` | `0x0C` | Global progress/unlock flags |
| `0x800C7AB2` | `2` | Current map ID, used to refuse cross-map restores |
| `0x8015C5DC` | `4` | Current playable character ID |
| `0x801FC60C` | `4` | Pointer to current player object; pointer itself NOT restored |
| `Object + 0x08` | `12` | Position as 3 floats |
| `Object + 0x14` | `6` | Orientation as 3 short angles |

Source: [original-game static RE notes](https://github.com/ogdanimal/Goemon64Recomp-Android/tree/main/docs/re-notes) and [Goemon64Recomp headers](https://github.com/klorfmorf/Goemon64Recomp/blob/dev/patches/variables.h).

The save-data block's live mirror at `+0x64` is not automatically current during gameplay. On restoration, **the live block, save mirror, and shadow** are synchronised. This avoids inconsistent HP/money/lives on the next save.

## What is intentionally NOT captured yet

- Active stage-specific/overlay data, actor AI state, enemy health, collision state, animation state, velocity/inertia and NPC/script virtual machine state.
- Native recompiler state (host threads, render/audio and input caches).
- Full level/scene transitions: restoring is **only allowed in the currently loaded map with the same character**. The saved `gamedata` may include *continue* spawn coordinates; it is not the same as restoring an active room.
- Entire 4/8 MB RAM images. A blind bulk restore would overwrite live pointers, stale overlays, render buffers and system task state and would not be safe on original hardware.

Even with all `0x304` save-data bytes captured, **a logically complete state restore is not guaranteed**. Game state is distributed across transient entities and code overlays. The next step is to reverse-engineer the game's area-load and character-switch routines to recreate actors from the restored game flags on a safe scene reload.

## Hooking the original ROM

1. Reserve a small RAM region for a static `GoemonCheckpoint` without overlapping game RAM, expansion-pack buffers, overlays or the heap. This needs a real linker/ROM memory-map audit; it cannot be assigned arbitrarily.
2. Hook a gameplay frame function in the **original ROM** (not `recomp_run_ui_callbacks` or another PC-only function). Ensure capture/restore occurs after game-state writes settle, and only at a safe frame boundary.
3. Implement `read` and `write` callbacks with volatile byte loads/stores to KSEG0 RAM or game-native copies, with appropriate cache/interrupt safety. The callbacks are not supplied here because the correct hook, storage and cache behavior are **not yet verified**.
4. Add N64 controller input and original display-list/font drawing for an in-game menu.
5. For a robust restore, bring the game to a controlled room/scene reload using original ROM mechanisms. Restore persistent flags *before* the loader reconstructs the scene; restore position/orientation once the new player object exists. Verify room-specific switches after load.
6. Keep practice-modified runs separate from leaderboard-eligible runs. Console autosplitting may require a separate emulator, flashcart, capture, or telemetry mechanism.

## Local build check for the portable C prototype

```bash
cc -std=c11 -Wall -Wextra -Werror goemon_checkpoint.c test_checkpoint.c -o checkpoint-tests
./checkpoint-tests
```

This tests the data model against simulated big-endian N64 memory, **not** a running Nintendo 64 or an actual patched ROM.


## Scene warp experiment (v0.5)

The external PC inspector has an optional **unverified** transition request:
`0x800C7CA0` pending map (u16), followed by setting `0x800C7A9F` exit flag
(u8) during ordinary gameplay. It is **not yet a validated original ROM warp
procedure** and must not be copied into a distributable N64 patch without
confirming teardown, entrance/spawn setup, overlay loading and state lifetime.
The actual scene-loader function remains the required ROM-native integration.
