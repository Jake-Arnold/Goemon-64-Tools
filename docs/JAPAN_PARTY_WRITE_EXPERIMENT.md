# Japan-0 controlled party writes — Sasuke and Yae experiment

**Status:** Implemented on `chatgptweb/japan-controlled-party-writes`, not merged. Real writable Mupen64Plus integration **not yet verified with this toolkit patch**. The user's **separate Cheat Engine test** verified that setting the Japan-0 Sasuke and Yae party flags makes those characters selectable, whereas forcing the character-index field directly does not correctly rebuild the character.

## What is actually known from the game

| Japanese guest RAM | Type | Meaning | Evidence |
|---|---|---|---|
| `0x80161DCC` | u32 BE | Current character index: Goemon = 0; Ebisumaru = 1 | User observed both normal switch directions via Japan Live |
| `0x80161E97` | u8 | Sasuke party-availability flag | Japanese GameShark code; user tested write in Cheat Engine, selectable afterwards |
| `0x80161E9B` | u8 | Yae party-availability flag | Japanese GameShark code; user tested write in Cheat Engine, selectable afterwards |
| `0x800CD2A2` | u16 BE | Current scene candidate | Observed in two Japanese scene transitions |

**Do not directly write 2 or 3 into `0x80161DCC`.** The user found this does not correctly switch to the character, as the original game must rebuild relevant character object, animation, assets and task state. **Values 2 and 3 are *not yet confirmed* by a normal user-initiated Sasuke/Yae switch.**

## Exact run procedure

1. Use a dedicated copy/test savestate. Start the Japanese retail revision-0 ROM in Mupen64Plus and enter an ordinary playable scene as Goemon or Ebisumaru. Avoid a boss fight, title screen, debug menu, loading transition or active character transformation.
2. **Manually save a complete emulator state** using Mupen64Plus's normal save-state action. Verify it exists and works before any experimental write. In-game saving after a flag unlock could persist the effect.
3. In a separate terminal from your normal USA toolkit, launch the experimental JP branch:

   ```bash
   cd ~/Desktop/goemon-japan-mupen-test
   git fetch origin chatgptweb/japan-controlled-party-writes
   git switch --detach FETCH_HEAD
   python3 -m practice.toolkit --game-version japan --enable-japan-party-writes
   ```

4. Select the **Japan - Ganbare Goemon** game version, **Verify ROM** against the exact retail Japan-0 ROM, select target **mupen64plus**, and connect to its running Linux PID (specify the PID if several emulators are running).
5. On **Japan Live / Party Test**, press **Unlock Sasuke**, read and accept the explicit one-byte write prompt only after saving the emulator state. The toolkit rechecks the current Mupen PID, rehashes the verified ROM, verifies three independent Japanese executable signatures at the **existing** RDRAM host base/endian, checks that read-only and short-lived writable views agree, and accepts only a normal scene and current character 0 or 1.
6. It writes **one byte** `0x01` at **`0x80161E97`** only when the **entire party word** was `00000000`. It reads that word back as `00000001` and checks the independent read-only reader sees the same flag. If the flag was already 1, no write is attempted. Every other value is rejected.
7. Switch character by pressing the game's **native C-Down**, not by editing `0x80161DCC`. If Sasuke appears correctly, note the current character index raw bytes and on-screen character identity. The expected (unverified) index is `00000002`.
8. Switch back to Goemon or Ebisumaru, and repeat with **Unlock Yae** (`0x80161E9B`). Repeat the native C-Down switch; the expected (unverified) index is `00000003`.
9. To undo the experiment, **load the pre-test emulator savestate**, then reconnect the toolkit; its original process-memory handle is invalidated on savestate load. The program does **not** automatically reset party bits, and **does not** claim the save-state completed merely because a hotkey was sent.
10. Use **Capture baseline → Compare → Copy changes** on the Japan Live tab to preserve the evidence. Record the selected character name alongside the raw index, party flags, current scene, and whether the correct model/animations/movement were loaded. Do not mislabel a raw 2 or 3 as a successfully spawned character without confirming in-game behaviour.

If Linux permissions allow reads but deny `process_vm_writev`, the button reports the write error; do not escalate privileges invisibly. The existing **Permit existing Linux PID** control is a user-visible, system-wide ptrace permission change and should not be toggled automatically.

## What the patch deliberately does **not** allow

- **No general-purpose Japanese hex editor**, arbitrary address writes, player coordinate writes, HP cheats, freezes or native debug warps.
- **No direct writes to the character index** `0x80161DCC`, player object/task pointers, scene IDs, pending scene, loader flags or other speculative globals.
- **No writable background polling.** The existing live reader remains `HostProcess(..., writable=False)`; each confirmed unlock opens a **new `HostProcess(pid, writable=True)`**, validates the existing RAM base, performs at most one guest-byte write, reads back and closes the handle.
- **No automatic rollback** of the flags during gameplay. Removing a party flag while its character is selected could leave the game in inconsistent state. The recovery mechanism is a verified pre-test emulator savestate.
- **No promise of atomicity**: Word-swapped single-byte guest writes are implemented as a host 4-byte read/modify/write, so the emulator can theoretically modify neighbouring bytes concurrently. The guarded before/after verification reduces but cannot remove this risk.

## Test matrix and gate to promote

1. Unit tests: only indices 2/3 accepted; both host endian orders; byte-accurate single flag write; no-write when already 1; rejection of unexpected word contents, unknown current character, invalid scene, and non-writable process.
2. CLI tests: default disabled, explicit opt-in enabled, `--read-only` takes precedence.
3. Controller tests: opt-in/--read-only gating, decline confirmation, PID mismatch rejection, independent writable view, and writable handle closure.
4. Tk smoke tests: both buttons disabled until verified Japan PID + reader + CLI opt-in; disabled in USA and on disconnect.
5. Real Linux Mupen64Plus test: write and readback of both flags, then normal C-Down switch with correct character visuals and index `2`/`3`, then restore savestate and reconnect.

**Only after the last item passes** should the two Japanese character-index identities be marked fully runtime-confirmed.

### Reproducible test commands

From the repo root on Ubuntu:

```bash
sudo apt-get install -y python3-tk xvfb xauth
python3 -m pip install -r requirements.txt
./scripts/test_japan_party.sh
```

The script runs the unit/controller tests against synthetic process memory and the Tk smoke tests under Xvfb (or an existing X11 display). It **does not** write to a real emulator or replace the user-controlled native-game test. If the host uses an externally managed Python, use the project's virtual environment as `PYTHON=.venv/bin/python ./scripts/test_japan_party.sh`.

**Current verification status in this chat:** test source is committed but the private branch's Python tests have not been executed here; do not claim 20 passing tests solely because 20 are defined.

## GitHub cadence and progress records

This feature uses a **separate draft branch** based on the latest Japanese scene/character evidence. Changes are pushed as small commits:

- Checkpoint 1: write primitive and ROM-free behavioural tests.
- Checkpoint 2: guarded UI with optional CLI gate, independently validated writable handle and confirmation.
- Checkpoint 3: test coverage, evidence log, step-by-step live test and forward plan.
- Checkpoint 4: controller-level tests, executable test script and precise test-status documentation.

`PROGRESS.md` records the implementation and its limitations. Keep each significant feature on an isolated branch with a draft PR, add a source-linked evidence record when the user provides a real RAM trace, and do not merge to the decomp mainline until runtime tests pass.

### Related work for future sessions

The separate USA memory/cheat/actor research remains on **PR #12** (`research/usa_external_memory_leads.json`), to review in the next USA decompilation session. Japanese player/task pointer work and native Japanese recomp execution require separate plans and proofs.
