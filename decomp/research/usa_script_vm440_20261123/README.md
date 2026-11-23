# USA script VM — independent native E234 replay, 23 November 2026

Research only. No canonical promotion, no gameplay test. The live source snapshot changed from `78e6303e2fe5f4e5f5a17bab50cb62fc792d241b` to `1ddb1b0941b0f39d4db6b0a3534fc1f230b51e0e` during this work (PR #204 merged). The E234 candidate and two blocked candidates remain ASM in the latter canonical manifest. The original 440-byte source comes from PR #203, Git blob `1d40ef0e89943033fa06ac16ea8c37dbd5e040e6`. The line-split control here is independently derived; it is not asserted to be byte-identical to PR #203's control. The source files are frozen by SHA256SUMS.

Fresh 2165 canonical verification passed. Independently replayed the actual post2165 native151 stage from the new stable snapshot, obtaining the exact published USA2316 ELF SHA256 `16fe08c2eebc6285f8c9fe882c54ca25ec5040c8eb32426b6da75c0929d52873`. Then compiled only E234 in the mixed VM, verified its entire unlinked text and relocation identity, restored two strictly guarded undefined-coordinate ELF metadata bytes (size and symbol type), used existing VM table layout adapter and existing inline-label restoration, and relinked to identical original USA ROM. The candidate ELF SHA256 is `f03cb69cf367c2627d6e5e3e0838e2753b7bd13f67da3796f7d619d323043cad`. Strict scratch inventory via unchanged `summarize_inventory` on readelf symbol lists and exact reviewed claim names: 2317 new C, 5046 ASM, 0 new positive aliases. This is not a canonical verifier run with a new claim. Full new-claim `decomp.verify`, canonical promotion-integrity validation and full new-claim local CI remain NOT_RUN. The unchanged published 2316 stored promotion integrity passed.

## Reproduction

Use authenticated clean archives/checkouts of the two exact stable snapshots above, your own original USA ROM, pinned original mnsg upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, original IDO 5.3 and cross binutils per GOEMON_BUILD_ENVIRONMENT.md. Read live BRANCHES.md, AGENTS.md, CONTINUE.md, autonomous skill and COMPILER_QUIRKS.md before native work. Do not reuse stale source snapshots as publication authority. All ROMs, upstream ASM, native objects, ELF, compiler binaries and logs with private bytes stay outside this kit.

Set `OLD` and `CURRENT` to the two authenticated repository roots, `UPSTREAM` to clean pinned original upstream, `ROM` to original private USA ROM, `WORK` to an absent scratch path, `REPORT` to an absent JSON path, `BIN` to the cross-binutils executable directory, `LIB` to the matching runtime library directory, `UV` to the working uv launcher, and `KIT` to this directory. Use the documented dependency setup. In this session the archived Python 3.12.16 launcher stood in for uv (offline, verified imports and frozen packages); GNU host readelf/nm were used only for ELF symbol inspection, not native code generation. Set PATH and LD_LIBRARY_PATH appropriately before builds.

```sh
cd "$OLD"
python3 -m decomp.verify --upstream "$UPSTREAM" --retail-rom "$ROM" --workdir "$WORK" --report "$REPORT" --uv "$UV" --jobs 8
python3 "$KIT/replay.py" --repo "$OLD" --baseline "$WORK/baseline" --binutils "$BIN" --lib "$LIB" --out "$WORK/probes"
cd "$CURRENT"
python3 - "$WORK" "$UV" <<'PY'
from pathlib import Path
import json,sys
from decomp.native251_promotion import apply_usa
w=Path(sys.argv[1]); d=apply_usa(w/'candidate',w/'baseline',w,sys.argv[2],8)
(w/'replayed2316.json').write_text(json.dumps(d,indent=2))
PY
python3 "$KIT/mixed_emitter.py" --repo "$CURRENT" --work "$WORK" --predecessor-report "$REPORT" --native151-proof "$WORK/replayed2316.json" --out "$WORK/emitter-current" --binutils "$BIN" --lib "$LIB" --uv "$UV" --jobs 8
```

The mixed script mutates only the scratch candidate and preserves predecessor ELF/object copies in its output directory. Do not run against a production checkout. To reproduce the earlier 2166 scratch result instead, use the fresh 2165 workdir and omit `--native151-proof` (the earlier result was run using the original 2165-only revision of the script; the generalized script's 2317 mode was executed successfully).

Host sanitizer fixture (actual candidate source; pointer-to-word conversion is intentional for the N64 32-bit ABI):

```sh
cd "$KIT"
for cc in gcc clang; do
  "$cc" -std=c11 -O1 -g -Wno-int-conversion -fsanitize=address,undefined -fno-sanitize-recover=all -fno-omit-frame-pointer -no-pie host_emitter_test.c -o "/tmp/goemon-e234-host-$cc"
  "/tmp/goemon-e234-host-$cc"
done
```

Both compilers passed 4096 cases each. No new C functions are counted canonically. F37C literal stays instruction-exact with 4-byte pool but differs in named relocations (+4 first); named external load moves first instruction/relocation mismatch to +8, with LO16 at +0x0C rather than +0x08. Five bounded external variants failed; no general new compiler quirk claimed. The dispatcher DF98 has not been independently recompiled in this session and retains the previous PR #203 relocation blocker.

## Follow-up, 23 November 2026 — actual canonical E234 stage

The preceding sections describe the historical scratch experiment. The fresh new-claim verifier now completes at 2,317/2,317 and exact 110,288 claimed instruction bytes using `decomp.usa_script_vm440_promotion`. The 2316 manifest/proof/inventory are frozen. Complete original expanded and retail ROMs match; strict inventory and promotion integrity pass. E234 alone is staged, F37C and DF98 remain ASM in the canonical manifest. See the new dated G2 proof and top-level PROGRESS entry for the actual acceptance status. `evidence/metadata_guard_controls.json` records six deliberately invalid private-object fixtures rejected by the stage guard, using the previously compiled raw mixed E234 object and independently rebuilt predecessor. No negative fixture bytes are distributed.
