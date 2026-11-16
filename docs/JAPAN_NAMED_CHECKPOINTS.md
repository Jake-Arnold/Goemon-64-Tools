# Named native Japanese checkpoints — 15 November 2026

## Purpose

The original USA logical checkpoint records/restoration use region-specific actor pointers and saved-event offsets; they are **not** safe to reuse for Japan. Native emulator savestates already preserve the game-wide state (scene, character, position, inventory, actors, scripts and progression), and the existing Project64/Mupen64Plus F5/F7 commands are user-reported working.

The dashboard's **Full emulator savestates** card now adds two compact Japan-only controls: a name field and **Save named slot**, and a selector with **Load named slot**. They reference the existing ten native emulator slots (0–9). The actual savestates belong to Project64 or Mupen64Plus; the toolkit **never copies or serializes savestate or RAM bytes**.

The human-readable metadata is stored locally at `practice_data_dir()/native-state-bookmarks.json` using the versioned `goemon-named-native-saves-v1` format. Each entry records region, backend, slot, name and save-request timestamp. If stable JavaScript-free Japanese gameplay reads are available, it additionally records scene, character and XYZ **for presentation only**. These values are **not used for restoration** and may be unavailable in menus/loading or other characters/scenes.

## Operations

- **Save named slot:** capture optional scene/character/position annotation; dispatch existing native emulator SAVE to the selected slot; replace any prior name for that same Japan+backend+slot. Record metadata only after the command is sent successfully. The toolkit cannot confirm the emulator completed or persisted the state; the UI explicitly says *save requested*.
- **Load named slot:** choose a matching Japan emulator record, select its native slot and dispatch the existing LOAD command. The native handler automatically stops freezes, disconnects stale RAM readers and invalidates pending transitions before loading. After actual emulator load, reconnect to read the game state.
- When switching to USA, the named controls are hidden. USA's existing native save/load and USA logical checkpoint code remain untouched. Names from one emulator cannot appear in another emulator's selector.
- **Read-only mode blocks** saving and loading. If the selected process differs from the connected Japanese backend, the existing native handler refuses to send input.
- **Slot overwrite policy:** saving again to the same native slot replaces the previous label for that slot, since the emulator itself overwrites that slot.

## Limits and next stage

The toolkit can request a native savestate but **cannot detect completion** from the emulator APIs currently in use. A name is metadata, not confirmation that the slot exists on disk. The local name file may outlive the emulator's actual save files or be copied between machines; the user must verify emulator state availability.

Next checkpoint work: optional native emulator save-file existence verification per backend and a compact in-game scene/position summary after load. Do not add direct Japan logical RAM restoration using unmapped pointers or USA event-bank offsets.

Implemented source: `practice/native_checkpoints.py`, `practice/toolkit.py`. Tests: `tests/test_native_checkpoints.py`, upcoming Tk acceptance. No ROM assets, dumps or emulator files committed.
