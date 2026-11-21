# Japanese original-ROM G2: 145 short/repeated C functions

**21 November 2026 — `PASSED_G2_LOCAL`, remote publication pending.**

The original Japanese region `japan_0` advances from **2,123 matching C / 112,336 original bytes / 5,253 ASM** to **2,268 C / 121,288 bytes / 5,108 ASM**. All **145 new C** (101 from the first repeated-source research batch and 44 from the structural-alternative batch) were rebuilt in their original source/ASM owner positions with SGI IDO 5.3 `-O2 -mips2`. Original instruction bytes: **8,952**. No overlap with the two previously promoted Japanese VM functions.

## Native acceptance already executed

- Pinned original upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee` with the private original Japanese ROM and bundled original compiler/binutils.
- Exact **33,554,432/33,554,432** expanded Japanese ROM SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`.
- Exact **16,777,216/16,777,216** recompressed retail Japanese ROM SHA-1 `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b`.
- **7,376/7,376** original ELF positive-sized function identities, **80,747/80,747** semantic relocations including main, relocation SHA-256 `e5420c90550fb564bb6c839357e92d5ab28f90b4e945734dc2dcfd892eb41f20`.
- Strict original ASM/C partition: exactly 145 old `.NON_MATCHING` markers removed, no C regressions or extra ELF aliases. Stage is fail-closed on original ROM, C SHA-256, original function extent, owners, and relocation multiset.
- Fresh native source byte reproof: previous packages independently passed 101/101 and 44/44 isolated exact checks. These do **not** substitute for the linked full-ROM proof above.
- Four new ROM-free regression tests **PASS**; **full** `python3 -m decomp.local_ci` **PASS**; 2,000 original-C GCC ASan/UBSan setter/interpolation cases **PASS**.
- Emulator gameplay **NOT RUN**. No USA code or original ROM inputs changed.

The 15 unusual source owners had genuine original trailing `nop` instructions **outside** their function labels. The stage retains those actual instructions as original assembly. No MIPS byte patching, fabricated NOPs, deletion of relocations, or relaxed original-ROM checks occurred.

## Reproduction

Obtain a fresh *pinned* `mnsg` checkout and copy your private normalized Japanese retail ROM into `config/japan_0/baserom.z64`. Restore the bundled dependencies and runtime additions as in `GOEMON_BUILD_ENVIRONMENT.md`. Then:

```sh
GOEMON_JOBS=8 bash decomp/build_japan_short145_promotion.sh \
    /path/to/fresh-pinned-mnsg /path/to/dependencies /path/to/runtime-additions
```

The script builds and authenticates all **2,118** baseline C, the previously published Start3 and VM2 (giving 2,123), then stages the new 145, checks full expanded/retail ROM, ELF, all relocations, inventory and full local CI. It requires fresh original inputs and never commits ROMs, original assembly, ELF, proprietary compiler or assets.

For a prepared, independently authenticated JP2123 checkout:

```sh
python3 -m decomp.japan_short145_promotion stage --checkout /path/to/JP2123
python3 -m decomp.japan_short145_promotion build --checkout /path/to/JP2123 \
  --deps /path/to/dependencies --runtime /path/to/runtime-additions
python3 -m decomp.japan_short145_promotion verify --checkout /path/to/JP2123 \
  --base /path/to/pristine-original-JP2123-baseline
```

The `--base` path must contain the pre-staging `build/japan_0/mnsg.elf` **and** exact `mnsg.z64`; the same checkout after staging is not a valid baseline. The full script handles this with private temporary reference copies.

All candidate C sources, original hash ledgers, isolated verification scripts and safe host fixtures are frozen under `batch101/` and `batch44/`. No private source bytes are included. The new linker/stage is `decomp/japan_short145_promotion.py`; evidence is `decomp/results/japan_0_2268_short145_g2_20261121.json` and regional inventory `japan_0_2268_inventory_20261121.json`.

**Publication boundary:** local authentic ROM G2 and full local CI have passed. A GitHub `chatgptweb/decomp` commit has **not** yet been pushed or remotely verified. Do not claim `PUBLISHED_REMOTE_VERIFIED` until a coherent implementation+metadata commit is fetched from the remote. Never push to `main`.
