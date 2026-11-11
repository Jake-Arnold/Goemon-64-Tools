---
name: goemon-full-rom-proof
description: "Use when validating production Goemon matching C, complete 32 MiB ROM identity, ELF inventory and final function promotions."
---

# goemon-full-rom-proof

Read `decomp/INPUTS.md` and verifier help. Use fresh workdir/report paths. Run `python3 -m decomp.verify --upstream "$GOEMON_UPSTREAM" --retail-rom "$GOEMON_ROM" --workdir "$WORK" --report "$REPORT" --uv "$(command -v uv)" --jobs 2`. Only after success run `python3 -m decomp.inventory --baseline "$WORK/baseline" --candidate "$WORK/candidate" --report "$INVENTORY_REPORT"`. Require 33,554,432 exact bytes, all claimed functions, source hashes and unchanged symbol inventory. Missing private inputs: BLOCKED_INPUT.
