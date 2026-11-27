# 152 isolated native IDO matches — research only

USA 104 / 15,924 B, Japan 48 / 7,268 B. All linked bodies, named relocations and altered-source negative controls pass. Full canonical candidate G2, translation-unit, strict inventory and hosted CI are NOT_RUN. Keep original ASM ownership.

Baseline stable/decomp 0ad88225c1a11f85454b259103f0f4c6ff49fa16; pinned upstream 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee; original IDO 5.3 SHA256 76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0. The final replay read ledger SHA256 3ae3af76d1aa320f3249bff23956e88788cb3b691902d91afe33ce9eb6b5e707.

## Replay
Set GOEMON_REPO to the authenticated stable/decomp checkout and GOEMON_UPSTREAM to a private pinned upstream workspace with independently generated region-specific Splat ASM, original expanded ROMs and exact baseline ELF builds for both regions. Set PATH and LD_LIBRARY_PATH for the original MIPS binutils and use the project Python 3.12 environment. Run:

```sh
python3 make_replay_input.py replay-input.json
GOEMON_JOBS=4 python3 replay.py replay-input.json replay-output.jsonl
```

The replay requires private ROMs/toolchain/upstream and live repository Python helpers; none are included. No raw original code, ROMs, proprietary tools or compiled binaries are included.
