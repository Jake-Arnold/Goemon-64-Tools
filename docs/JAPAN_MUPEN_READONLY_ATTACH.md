# Read-only Japanese Mupen64Plus PID attach

This branch introduces **read-only raw RDRAM access** for the Japanese retail revision-0 game in an already-running Mupen64Plus process. It does not translate USA game fields or make a Japanese native recomp executable.

## How to connect on Ubuntu Linux / X11

1. Start the exact Japanese revision-0 ROM in Mupen64Plus and let the game boot.
2. Start `python -m practice.toolkit` (or the normal toolkit launcher).
3. On the dashboard, select **Japan - Ganbare Goemon** as Game version.
4. Click **Verify ROM** and choose the same exact Japanese retail ROM file (`.n64`, `.z64`, or `.v64`). The SHA-1 must be `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b`.
5. Set the connection target to **mupen64plus**. Enter the real emulator **PID** or leave it blank when only one matching process is running.
6. Click **Connect to game**. On success, the dashboard reports the attached PID, RDRAM base, and detected endian order. The **Japan Mupen64Plus RDRAM (read-only)** panel enables byte reads such as `0x80000450` with length `16`.

On Linux, attaching to another already-running process may be denied by Yama `ptrace_scope` or sandbox restrictions. The toolkit's existing **Permit existing Linux PID** control can temporarily relax that system-wide permission after user consent, with the matching restore control. Do not change system-wide permissions silently. Launching Mupen64Plus through the toolkit is not required.

## Safety and validation

- The existing Mupen savestate support only chooses a process and sends emulator hotkeys; it never granted toolkit live RAM access.
- The new scanner uses **three complete, separate 64-byte executable-code probes** from the supplied, hash-verified Japanese ROM. ROM offset `0x1050` corresponds to guest RAM `0x80000450`; other probes are at ROM `0x1200` and `0x3000`.
- The scanner searches readable mappings of the verified Mupen PID, tries both word-swapped and big-endian layouts, and checks all three probes and the end of the 8 MiB host RAM buffer.
- The selected RDRAM mapping is rejected if it cannot be located uniquely. A manual `--base` hint **does not bypass verification**.
- The Japanese process handle is opened `writable=False`. The raw Japanese reader is held in `Toolkit.jp_rdram`, never assigned to `Toolkit.mem`. This intentionally prevents the original USA-memory field parser, freeze workers, warps, unlocks, story-progress write paths and checkpoints from touching Japanese RAM.
- A match of the three known executable windows is **not a full cryptographic measurement of the ROM running inside the emulator**. It provides strong RDRAM/code-layout evidence and a safe read-only attachment, but does not validate every field in a Japanese save file or running state.
- Savestate loading drops the RAM handle; reconnect to revalidate after a load. The existing emulator hotkey binding still needs testing against each Mupen frontend.

## Verification completed

Nine ROM-free synthetic scanner/unit tests passed locally (word-swapped, big endian, manual hint validation, mismatched code, duplicate candidates, permission failure, ROM probe selection). A synthetic 8 MiB word-swapped RDRAM reconstructed using **the actual uploaded Japanese ROM code bytes** was also found and decoded correctly. This is a reconstruction, **not an actual running Mupen64Plus integration test**.

The GUI connection wiring is a GitHub patch and has not been run against an actual emulator UI in this environment.

## Still required for richer Japanese toolkit support

- Live Mupen process test on Linux: map discovery, actual readback, reboot/savestate reconnect, pointer stability and all Yama permissions.
- Independently derive Japanese `SYS_POINTER_ADDR`, `PLAYER_OBJECT_PTR_ADDR`, `PLAYER_TASK_PTR_ADDR`, player offsets, global state and scene IDs; verify each against runtime traces. The USA addresses must not be reused merely because code matches structurally.
- Add per-region memory symbol definitions and gate every data-editing feature on verified Japanese fields.
- For a runnable Japanese Goemon64Recomp, full Japanese N64Recomp function coverage, relocation tables, compile/patch tooling, separate game entrypoint and native gameplay tests remain necessary. ROM decompression and candidate structural mapping alone cannot boot Japanese gameplay.
