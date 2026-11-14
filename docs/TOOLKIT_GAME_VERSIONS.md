# Toolkit game-version selector (2026-11-14)

The Connection panel now includes a game-version selection with:
- **USA - Mystical Ninja** (default): existing USA live toolkit, with unchanged addresses and controls.
- **Japan - Ganbare Goemon**: exact retail ROM verification and explicit unsupported-runtime state.

The **Verify ROM** action checks the local 16 MiB image's N64 byte order, game code, revision and canonical SHA-1. The verified retail identities are USA `NG5E` SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66` and Japan `NG5J` SHA-1 `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b`. The input is not copied, patched, stored or transmitted.

Version changes safely stop the current USA write/freeze activity, detach from the process and clear live state. The Japanese selection disables live-process attachment, the Linux recomp launcher, memory tabs and checkpoint actions because Japanese guest RAM addresses, structures, emulator identification and recompilation are not validated. A selected file is **not** evidence of the running process's ROM version. This does not enable Japanese gameplay in Goemon64Recomp.

CLI: `python3 goemon_app.py --game-version usa` or `--game-version japan` (offline ROM verification only).

Tests: `python3 -m unittest tests.test_game_versions tests.test_dashboard -v` (GUI tests require Tk display/Xvfb). Five ROM-free version identity tests passed in a local isolated harness and both supplied retail ROMs passed exact-hash identity checks. The GitHub connector environment did not execute the integrated UI tests. The local ROMs and code assets were not committed.

Next: build Japanese recomp region tables/symbols/overlays and validate Japanese runtime memory mappings. Only then activate Japanese live toolkit features behind explicit region verification.
