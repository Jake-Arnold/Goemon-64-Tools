# Japanese player XYZ research — read-only Windows/PJ64 workflow

**Branch:** `chatgptweb/japan-controlled-party-writes`  
**Implementation:** `practice/japan_player_position_research.py` and the existing **Event sessions → Advanced RAM comparison** panel.  
**Evidence level:** research tool and synthetic regression tests **authored, not yet executed on the user's live Project64 session**. No Japanese player pointer, float XYZ offset or task memory address is established by this feature.

## Current confirmed live milestones

On 2026-11-15 the user explicitly confirmed **Project64 savestate restoration works** and that the two individually opted-in **Sasuke and Yae party-unlock writes work** on their Windows system. This verifies those actions for their tested session but does not by itself verify native C-Down selection to Sasuke/Yae or character index `2/3`; that remains a separate observation.

Value Search and focused A/B/C had also been live-tested on Project64, with details in [the screenshot record](JAPAN_PROJECT64_LIVE_SCREENSHOT_EVIDENCE_2026-11-15.md).

**Important alias:** the reversible A/B/C row `0x80161DCF: 00 → 01 → 00` is the **last byte** of the known `u32` character index at `0x80161DCC` (`00 00 00 00` → `00 00 00 01`). The A/B/C results now label such bytes **character-index byte (known alias)**; they are not independent quest/event flags. The other reversible `0x80161DBD: 0B → 09 → 0B` remains unknown.

## New XYZ discovery experiment

1. From PowerShell, update the branch and run the suite:

   ```powershell
   git pull --ff-only origin chatgptweb/japan-controlled-party-writes
   .\scripts\test_japan_party.ps1
   py -3 -m practice.toolkit --game-version japan
   ```

2. Start Project64, load the exact Japan-0 retail ROM, then in the toolkit verify the ROM, select `project64`, and connect. This research mode is **read-only**; the `--enable-japan-party-writes` flag is not required.
3. Enter a normal gameplay room with a stationary player. In **Event sessions → Advanced RAM comparison**, set **Test: Player movement** and **Memory range: wide**. Save a Project64 savestate as a rollback marker if desired. Make sure the game is running, not paused in its internal menu.
4. Stand still. Select **Capture A: Before**. Wait for the Japanese capture completion message.
5. Walk a visible distance within the **same room** without switching character, then **stop moving**. Select **Capture B: After**. Wait for completion.
6. Without moving further, remain at this **new position** and select **Capture C: Still at B** (the button relabels itself when **Test: Player movement** is selected). Here C is a **settled state at B**, not a physical return to A. Do **not** walk back to A for this experiment.
7. Select **Find XYZ triples (read-only)**. A background worker scans the verified 4 MiB or 8 MiB wide Japanese snapshots. The results are **aligned consecutive big-endian float triples** whose X/Z values changed from A to B but stayed approximately fixed from B to C. Y may change moderately (e.g. from a jump). Rejected cases include changed map/character, different emulator PID/RAM session, mismatched capture ranges, nonfinite floats and implausible coordinates.
8. Results are **ranked hypotheses**, not confirmed player XYZ. The table's C column temporarily changes to **C stable at B?**, avoiding confusion with normal A/B/C's **C matched A?** semantics. **Export comparison JSON** exports address, XYZ values, deltas, rank and session metadata, **not the raw 4/8 MiB RAM snapshots**.
9. Selecting a candidate and **Watch selected address** creates a **read-only `f32` X candidate** in Japan Live. For a candidate start `0x80ABCDEF`, the trial Y and Z fields are at **start+4** and **start+8** respectively (assuming the candidate really is a contiguous XYZ structure); add them manually as typed `f32` custom watches. They are not promoted to writable addresses.
10. Repeat with another movement direction and in another room. Check that the same candidate behaves like the on-screen player and is not an NPC, camera, animation object or staging buffer. Character switches and savestate restoration should be separate controls after the movement correlation is established.

## Algorithm details and limitations

- A/B/C are canonical **big-endian guest RAM snapshots** captured by the already-verified Windows Project64 or Linux Mupen region-specific reader. Matching session identity includes region, PID, host RAM base, byte order and live reader instance. Scope must be **wide** for all three.
- Each aligned 12-byte group is decoded as `(X,Y,Z) = (>f, >f, >f)`. Reject values outside ±100000, `NaN` or infinity. Horizontal A→B displacement must be between 0.75 and 5000 coordinate units; vertical difference must be at most 300; each C coordinate must be within 0.5 units of B.
- Rank higher when the Y coordinate remained stable, both X and Z changed, and the horizontal movement is moderate. Cap returned candidates at 200, recording the complete candidate count. This is intentionally a **heuristic**, not an automatic structural/pointer derivation.
- **Wide snapshots are not atomic:** the emulator can update game state during each multi-chunk read, producing inconsistent candidates. In that case repeat while stationary and compare results.
- There is **no** proven relationship yet between a returned triple and Japan player object base, task pointer, velocity, action, collision, safe warp or logical checkpoint. USA layout guesses must never enable Japanese writes.
- All discovery work happens in a background thread. Disconnect/reconnect and the general **Clear** button invalidate pending results. The existing ordinary A/B/C `Compare` continues to work with its separate semantics, restoring the original table heading after XYZ research.

## Next proof threshold

A proposed Japanese player XYZ field requires reproducible **read-only** observations across at least two scenes, two movement directions and a normal character switch. A stable player/task pointer requires additional exact guest pointer cross-references, object lifetime analysis and loading-state tests. No GUI teleport, freeze, pointer-derived collision or checkpoint restore control should be enabled before those separate stages.
