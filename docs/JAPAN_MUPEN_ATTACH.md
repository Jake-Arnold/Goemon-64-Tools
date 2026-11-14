# Japanese Mupen64Plus — experimental read-only RDRAM attachment

**Status:** New isolated Python attach probe; not yet connected to the GUI's USA gameplay watches. No end-to-end real Mupen64Plus PID test has been performed.

## What it does

- Verifies a **user-supplied** Japanese revision-0 `NG5J` retail `.z64`/`.n64`/`.v64` or exact expanded `.z64` image by SHA-1.
- Confirms the chosen PID belongs to the Mupen64Plus process (`practice.emulator_savestates`).
- Opens Linux `HostProcess` **read-only**, scans readable/writable host address ranges, checks four separate 64-byte original Japanese MIPS main-code signatures at N64 physical offsets `0x10000`, `0x20000`, `0x30000`, `0x40000`.
- Tests big-endian and 32-bit word-swapped host-memory layouts, rejects byte-identical cartridge-ROM decoys, incomplete/ambiguous signatures and inaccessible memory.
- Exposes `Rdram.read_guest()` for an explicitly requested **N64 address** and prints the detected process PID, host base and endian. The host process is closed after the read.

## Ubuntu run

From the root of a Goemon-64-Tools checkout containing the probe:

```bash
python3 -m practice.japan_mupen_rdram \
  --rom '/path/to/Ganbare Goemon - Neo Momoyama Bakufu no Odori (Japan).n64' \
  --pid 12345
```

Leave off `--pid` if exactly one Mupen64Plus emulator is running. The default read address is executable code at `0x80030000` (32 bytes); to read another N64 guest address use `--address 0x80030000 --length 64`. Optionally use a known **host** RDRAM base via `--base 0x...` (still verified against the Japanese code) or increase `--max-scan-mb` if the host memory footprint exceeds 1 GiB.

**Linux permissions:** `/proc/PID/maps` and `process_vm_readv` may be denied for an independently launched game because Ubuntu's Yama `ptrace_scope=1`. This command does not weaken the policy or elevate privileges. Use the toolkit's existing *Permit existing Linux PID* control if you understand its system-wide tradeoff; otherwise launch as a child or adjust permissions separately.

**Host RAM layout has not been confirmed with a live Mupen64Plus process.** The code assumes the main text is present in contiguous host RDRAM and unmodified at the checked offsets. Different emulator versions/plugins or boot phases may invalidate that assumption. Failures should be treated as diagnostics, not evidence that the ROM is unsupported.

## Specifically not supported

- Japanese dashboard player position, scene reloads, item grants, progression flags, freezing, Live Memory tab or memory writes. All known offsets in those tools remain USA-specific.
- Selecting Japanese version in the original toolkit UI **still** provides ROM verification and the pre-existing emulator save-state hotkeys only. The new probe is currently CLI-accessible.
- A Japanese Goemon64Recomp binary, JP recompiler output, linked overlays, runnable JP GameEntry, or complete Goemon64Recomp savestates.

## Verification

Six Python synthetic tests passed locally, covering both endians, exact ROM identity, rejection of a ROM-buffer decoy, duplicate candidates, incomplete fingerprints, and scan budget. The real 32 MiB Japanese decompressed ROM supplied in this conversation was checked against its expected SHA-1 and used to populate two synthetic RAM layouts; the scanner recovered the correct base and endian for both.

The live follow-up gate is a real `mupen64plus` PID playing the Japanese ROM, followed by validation during gameplay and after native savestate restore. Only after that should read-only Japanese field discovery and GUI integration begin.
