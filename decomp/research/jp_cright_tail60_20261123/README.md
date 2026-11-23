# Japanese C-Right stage handoff: original-native 60-byte matching C

**Research-only handoff; NOT a canonical matching-C promotion.** Date: 23 November 2026. Canonical base consulted: `stable/decomp` at `c2103dd32a4c0833c6754e75edb65bf8f5e6010c` (the `chatgptweb/decomp` branch is historical). Existing canonical Japan remains **2,370 matching C / 127,008 original code bytes / 5,006 ASM entries**, and USA remains 2,090 C. The original-upstream assembly-only comparison below is deliberately **not** represented as a rebuild of the canonical 2,370 C source or its 80,745-relocation policy.

## Why these functions?

Real user-owned Project64 Phase-3 `normal` and `held` traces corroborate a deferred resource-loader handoff: 1 vs 76 stage initializer entries, 13 actor-constructor and marker writes in each, 75 held bypasses, no observed allocator call during the aliased interval. The post-load stage flag at `D_80162420 + 0xD1` (guest `0x801624F1`) is 0 (normal) versus 1 (held/released), but no gameplay/freezing cause can yet be assigned to this value. In the immediate original Japanese stage overlay, verified writes include `0x802125C4` (held gate) and `0x80212680` (normal branch conditional on input `0x0008`). There is no established consumer in this local stage excerpt. Never extrapolate unrelated `0xD1($reg)` accesses to this particular stage structure without register provenance.

The adjacent, previously ASM-owned `func_80212C50_5CE1E0` at **expanded Japan ROM `0x5CE1E0` / runtime VMA `0x80212C50`**, extent **60 bytes (15 MIPS instructions)**, resets `g_system_ptr = g_system` and invokes `func_80004170_4D70()` followed by `func_8000339C_3F9C()`. See `source/func_80212C50_5CE1E0.c`. This restores the system pointer at a stage handoff; its causal role in glitch effects remains unproven.

## Exact native evidence: PASS, but not accepted canonical integration

Authenticated private retail Japanese ROM SHA-1 `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b`; expanded 33,554,432-byte SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`. Original upstream `klorfmorf/mnsg` pinned commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`; native SGI IDO 5.3 executable SHA-256 `76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0`, official project flags:

```
-c -G 0 -non_shared -Xfullwarn -Xcpluscomm
-Iinclude -Ilibultra/include -Ilibultra/include/PR -Isrc -I.
-Wab,-r4300_mul -woff 649,838,712
-D_LANGUAGE_C -D_FINALROM -DF3DEX_GBI -D__sgi -DNDEBUG
-O2 -mips2
```

Two **independent freshly cloned pinned** upstream working directories received the verified original retail/expanded ROMs privately. For original ASM-only, the checked Splat config converted exactly 189 original C units into ASM (through `decomp.japan_asm_baseline`), and the known cross-object reference fix promoted exactly 22 genuine `.L` labels and renamed two pre-existing BSS aliases. For candidate C, the **only** extra stage edit changed original file_12 overlay owner boundaries:

```
- [0x5CD620, asm]
- [0x5CE1E0, c, jp_cright_tail60]
- [0x5CE220, asm]
```

Original ASM-only was linked with `C_FILES=`. Candidate was linked with `C_FILES=src/jp_cright_tail60.c`. Both passed the exact **33,554,432/33,554,432 original expanded ROM bytes**; the target is 60/60 code bytes exact, **7,376/7,376 positive ELF function name/address/extent identities** equal, and **80,810/80,810 full-ELF semantic relocation tuples** equal, fingerprint SHA-256 `82493bc7aa5eca079b1573a1f7999e99fb28384eed1efe8c4cf1777826dc2805`. Native compiler uses original IDO, not host GCC. The rebuilt original ROM was compared byte-for-byte, not only by checksum. `verify_original.py` independently checks frozen source hash, upstream/ROM/IDO pins, exact ownership split, complete ROM, ELF identity, full relocation multiset, and ASM→C identity provenance. `evidence_original-rom.json` is the sanitized recorded passing result.

Compiler attempt outcome for the exact 60B wrapper: **`NO_NEW_COMPILER_FINDING`**, with the known documented IDO source-line/ABI quirks consulted; the first source form already reproduced all original instructions and relocations, so no mismatch repair was needed.

**Not run:** rebuild with the **live accepted Japan 2,370-C mixed source and its special dual-reference relocation policy**, canonical `decomp.verify`, strict inventory, `decomp.promotion_integrity --validate` and *full* current stable/decomp `decomp.local_ci`. Therefore the official accepted count **remains 2,370**, not 2,371. The 80,810 relocation count here belongs to the independent all-ASM original-upstream comparison and must not be compared directly to canonical 80,745. No emulator gameplay experiment using this reconstructed C was run.

## Adjacent bounded IDO probes — preserve ASM

`func_80212460_5CD9F0` (original 76B), two C variants: both compile to 76B but first instruction register `$v1` in original versus `$v0` in candidate; reversing source-load order did not recover original register assignment. `func_802124AC_5CDA3C` (original 104B), four C variants: first is 96B; symbolic offset restores 104B but wrong register at first instruction. Explicit `u8 **system = &g_system_ptr` restores **first 8/26 original instruction words**, but at original function-relative `+0x20` compiled halfword load targets `$v1`, original targets `$t7`. A fourth explicit table local preserves the same mismatch. These six variants are included under `source/failed_*.c` with source SHA-256s and failures in `evidence_negative_controls.json`. These are **`EXISTING_QUIRK_NOT_APPLICABLE`** for the attempted known source-order/temporary type controls, not a new verified general compiler quirk. No native match or promotion for either function. Full attempted original-unit staging of these failed sources was NOT run.

## Reproduction (private original inputs are never packaged)

Place this research directory in a **clean current stable/decomp checkout** at `decomp/research/jp_cright_tail60_20261123/`; ensure the pinned upstream Japan checkout(s), user-owned Japan-0 ROM, authenticated native IDO 5.3, and private dependencies are present. Never stage into a shared checkout. All commands assume `python3` has access to the current decomp package and the pinned `mnsg` sources have been initialized with their usual dependency setup.

```
python3 decomp/research/jp_cright_tail60_20261123/verify_original.py stage-asm --checkout "$JP_ASM"
(cd "$JP_ASM" && splat split config/japan_0/splat_asm_only.local.yaml)
python3 -m decomp.japan_asm_baseline patch-asm "$JP_ASM"
(cd "$JP_ASM" && make -j8 VERSION=japan_0 C_FILES= build/japan_0/mnsg.z64)

python3 decomp/research/jp_cright_tail60_20261123/verify_original.py stage-c --checkout "$JP_C"
(cd "$JP_C" && splat split config/japan_0/splat_tail60.local.yaml)
python3 -m decomp.japan_asm_baseline patch-asm "$JP_C"
(cd "$JP_C" && make -j8 VERSION=japan_0 C_FILES=src/jp_cright_tail60.c build/japan_0/mnsg.z64)

python3 decomp/research/jp_cright_tail60_20261123/verify_original.py verify \
  --original "$JP_ASM" --candidate "$JP_C" --report /PRIVATE/NEW-proof.json
python3 -m unittest discover -s decomp/research/jp_cright_tail60_20261123/tests -p 'test_*.py' -v
bash decomp/research/jp_cright_tail60_20261123/tests/run_host.sh /PRIVATE/NEW-host-results
```

`stage-asm` and `stage-c` **refuse to overwrite** an existing generated config. These commands are one-time operations on **two independent scratch checkouts**. Do not rerun `stage-c` on one already staged checkout, and do not write confidential ROM or generated ASM to Git. `verify` also refuses to overwrite a report path. Any new source/layout/ROM/ELF/relocation mismatch fails closed.

### Next bounded native targets

1. Retry `func_802124AC_5CDA3C` (104B) with controlled original IDO register-pressure experiments centered on original relative `+0x20` halfword destination register; do not expand to random source sweeps. 
2. Investigate `func_80212460_5CD9F0` (76B) first-instruction `$v1` allocation independently.
3. Use the live stage pointer provenance to locate actual downstream consumers of flag `0x801624F1`, and acquire the first freeze-triggering or otherwise anomalous post-release trace before asserting a freeze mechanism.
4. Only then do full current-accepted-2370 JP combined ROM, ELF, relocation-policy, strict inventory, promotion integrity and full CI; promote one function through atomic `decomp/*` PR if every gate passes. Any future rejected source stays ASM.
