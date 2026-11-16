# Verified Japanese recompilation build input

This change produces a **correct 32 MiB expanded Japanese ROM image** from the user's own retail revision-0 `.n64`, `.z64`, or `.v64` file. It does not bundle ROM data or make the USA-only Goemon64Recomp executable run the Japanese game.

## Verified inputs

| Region | Retail 16 MiB SHA-1 | Expanded 32 MiB SHA-1 |
| --- | --- | --- |
| USA (`NG5E`) | `df8083a54296b8c151917c5333e1c85f014a2a66` | `6ea0ed71032ce08fc2745f412d84936382197494` |
| Japan revision 0 (`NG5J`) | `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b` | `6f8745fecc3a5e7d4918c7a73353eb0726116ded` |

The tool normalises byte order, verifies the original hash and revision, locates the 1,312-pointer Nisitenma-Ichigo table, expands its 1,311 intervals, aligns decompressed files to 16 bytes, recalculates the CIC-6102 header CRC, and verifies the final SHA-1 **before** writing output. An incorrect ROM or expansion cannot produce the expected output file.

Run from a Goemon-64-Tools checkout:

```bash
python -m decomp.recomp_rom_input \
  "/path/to/Ganbare Goemon - Neo Momoyama Bakufu no Odori (Japan).n64" \
  "/path/to/mnsg/config/japan_0/baserom.decompressed.z64" \
  --region japan_0

python -m decomp.recomp_rom_input \
  "/path/to/Mystical Ninja Starring Goemon (USA).z64" \
  "/path/to/mnsg/config/usa/baserom.decompressed.z64" \
  --region usa
```

This Japanese output matches the `sha1` pinned in `klorfmorf/mnsg/config/japan_0/splat.yaml`. Against the two supplied retail ROMs, the output hashes above were reproduced exactly.

## Japanese port blockers

1. The original `mnsg` repository has a Japanese `config/japan_0/splat.yaml`, but its `symbol_addrs` and `reloc_addrs` source directories are empty and `rommy.yaml` is absent. It is not an independently verified, ready-to-build Japanese project.
2. Upstream `Goemon64Recomp/mnsg.toml` references USA function symbols; its ROM loader has a hardcoded USA file table at `0x57FD8`, USA `NG5E` check and USA decompressed CRCs. Japan's table begins at `0x58258`. A Japanese runtime must introduce separate functions/overlays and patch symbols; changing a hash alone will not work.
3. `Goemon64Recomp` complete savestates need runtime-level execution state snapshots, not RDRAM copying. Project64/Mupen full native states are addressed separately in the toolkit PR chain.
4. No user-owned `Goemon64Recomp` fork has been created: the connected GitHub integration can read upstream but has no fork/create-repository permission. A local offline source checkout cannot be cloned in this environment. Do not claim a Japanese runtime was built or tested.

## Verification

`python -m unittest tests.test_recomp_rom_input -v` — five synthetic tests passed in an isolated local test checkout. Both supplied real ROM inputs expanded and matched their expected hashes. No CPU replay, title screen, player movement or save/load in a Japanese static recomp has been tested. No ROM, expanded ROM, assets or save files are added to GitHub.
