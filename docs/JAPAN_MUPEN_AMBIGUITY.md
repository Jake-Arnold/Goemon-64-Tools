# Japanese Mupen64Plus: ambiguous RDRAM mapping fix

## What failed

The previous scanner matched three independent 64-byte Japanese executable-code windows, but **both the active 8 MiB N64 RDRAM and an in-process copy of the cartridge ROM can contain those same code bytes**. The scanner therefore correctly refused an arbitrary selection but gave no candidate addresses, even when a PID was supplied. A PID identifies the Linux process, not the memory mapping within it.

## Fix

- **ROM copy exclusion.** The exact verified Japan-0 cartridge header now travels with the verified code probes. For each apparent RDRAM base, the scanner checks 0xC00 bytes *before* that base for the matching 64-byte cartridge header in the same endian representation. If present, this candidate is identified as an offset into a cartridge-ROM buffer and rejected. Manual base hints are also checked against this condition.
- **Ambiguity is actionable.** If two independently matching candidates remain, the scanner raises a structured ambiguity containing the exact host bases and endianness. The Dashboard gains a **Japanese RAM base** dropdown. Initially it says `Auto (detect)`; on a double-match it lists every matching `0x... (big/wordswapped)` value. Choose one and select **Connect to game** again.
- **Safe manual selection.** The selected base is tied to its original PID and must pass all three verified main-code probes on every reconnection. A stale/different PID or invalidated memory base fails closed. Process memory is still opened `writable=False`, and the normal USA game-memory controls remain disabled.
- **Caveat.** Two fully populated, code-matching RDRAM buffers cannot be proven active by code signatures alone. Selecting one unlocks **read-only** inspection, not automatic gameplay editing. Only use dynamic observations to infer which buffer is active. Never auto-select an ambiguous buffer.

## Running the fix

In your existing test worktree, update to `chatgptweb/japan-mupen-ambiguity-fix`, then run:

    python3 -m practice.toolkit --game-version japan

Select **Japan**, verify the retail Japanese ROM, choose `mupen64plus`, enter the PID if necessary and connect.

If one original candidate is a retained cartridge image, the new scanner should automatically eliminate it and connect. If both remain, the new dropdown exposes addresses; select a candidate and connect again. You do not need to launch Mupen64Plus from the toolkit or relax PID permissions if the scanner already reads memory.

## Tests

- All nine existing local Japanese attach tests passed after the scanner change.
- Three new ROM-free duplicate/RDRAM tests passed: big-endian and wordswapped cartridge-ROM copy rejection, manual-decoy rejection, and exact two-RDRAM-candidate address reporting with manual revalidation. **12/12 local tests passed.**
- Additional real-input reconstruction: exact uploaded Japan-0 16 MiB ROM SHA-1 `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b`; 32 MiB synthetic host process with an active 8 MiB word-swapped RDRAM and a separate word-swapped full cartridge copy. The scanner correctly selected the true synthetic RDRAM `0x10000000` and rejected faux base `0x10C00C00`. Initial 16 guest code bytes matched the real ROM at `0x1050`.
- **Still untested:** actual running Mupen64Plus process after this patch, Tk GUI interaction with candidate selector, memory mutations during gameplay, actual savestate hotkeys. This is not a playable Japanese Goemon64Recomp.
