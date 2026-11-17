# Isolated Goemon64Recomp USA/Japanese ROM loader preparation

This **prepares the ROM decompression code only**. It does not produce a Japanese executable or alter the USA recompiled code. It must never be interpreted as completed Japanese game support.

## Tested metadata from supplied retail cartridges

| Parameter | USA NG5E | Japan NG5J revision 0 |
| --- | --- | --- |
| 16 MiB original SHA-1 | `df8083a54296b8c151917c5333e1c85f014a2a66` | `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b` |
| Header original CRC1/CRC2 | `FCBCCB21` / `72903C6B` | `832C168B` / `56A2CDAE` |
| Nisitenma file-table start | `0x57FD8` | `0x58258` |
| Expanded CRC1/CRC2 | `9CC11F4B` / `ABAA8538` | `673A3EDC` / `2491ADFC` |
| 32 MiB expanded SHA-1 | `6ea0ed71032ce08fc2745f412d84936382197494` | `6f8745fecc3a5e7d4918c7a73353eb0726116ded` |

The upstream `Goemon64Recomp/src/game/rom_decompression.cpp` hardcodes the USA values. The patcher replaces only the variant metadata, ROM-code and original-header-CRC checks, file-table selection and expanded-header CRCs. It also verifies the Nisitenma signature at the selected table location. It retains the original USA algorithm and code. The runtime's `GameEntry` ROM hash validation must remain enabled.

### Apply only to an isolated checkout

    python3 -m decomp.prepare_recomp_region_loader /path/to/Goemon64Recomp --dry-run
    python3 -m decomp.prepare_recomp_region_loader /path/to/Goemon64Recomp

The tool rejects a dirty target file, an unrecognised upstream source layout or repeated patching. Output writes are atomic. It does not alter submodules, build code or user saves.

**The GUI will still reject the Japanese ROM.** `src/main/main.cpp` registers only one USA `GameEntry` with USA `.rom_hash = 0xDB1BC7EE0E6BEBA1ULL`, USA `recomp_entrypoint`, and USA overlay/patch symbols. A Japanese `GameEntry` must be created only after generating and linking Japanese recompiled functions with the correct overlays, entrypoint, patches and assets. Registering Japanese input against USA executable functions would be incorrect.

## Verification and limitations

- Three source-renderer/unit safety tests passed locally (`python3 -m unittest tests.test_prepare_recomp_region_loader -v`). Combined local ROM-input, function/overlay and loader source tests: 17 passed.
- The Japanese and USA decompressed hashes were independently verified, and their ROM-table locations and CRCs were read directly from the verified images.
- Applying this patch to a complete upstream checkout and compiling/booting its C++ runtime were **not** completed in the connected GitHub environment.
- Full recomp savestates require runtime-level thread/scheduler/RSP/timing and graphical/audio state restoration; this patch does not address them.
- The repo integration cannot create a user-owned GitHub fork; this is an isolated, reproducible source preparation for a local writable upstream checkout.
