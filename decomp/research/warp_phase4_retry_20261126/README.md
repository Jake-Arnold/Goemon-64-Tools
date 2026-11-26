# Warp Phase 4 — dispatcher retry and accepted-G2 donor diagnostics (FAILED_NATIVE)

Canonical base `8b195d8ce5a31723a71af428ee4f7bccf32b0bf8`, authenticated source archive 15142908886 (outer and inner SHA-256 checks, commit identity, reconstructed Git tree 3b7ec59747ce3557dd5b01d35ea94d1a8853e956). PR #285 predecessor `07074012ad5690d73aea992eb5c1c3454fc09d1a`, prior tree 5ba270d9bc12c7f6ec75fb22c00b75321437996f. Both previous hosted checks PASS. Original upstream 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee, independent USA and JP original retail/expanded ROM and original IDO hashes exact. Shell Git DNS failed; isolated authenticated archives and connector used. Extraction command timed out; the regional target references were present, independently checked against original expanded ROM and linked exactly. No complete baseline build or full candidate G2 is claimed. Existing canonical inventories USA3066/JP3004 unchanged; no overlap with accepted target names/ranges; prior PR #285 owns the same research; no new ownership. Prior principal pending-manifest audit not exhaustive.

## Bounded source retries

Original 256-byte extents; first mismatch scheduling +0xB0 (expected 8fa40028, generated 002c0821); +0xB4 exchange, +0xD4 operand order. Five new variants per region and two baseline replays: explicit destination pointer (32/64, size/reloc failure), explicit stored value (54/64), comma-expression call argument (61/64), unsigned comparison casts (61/64), preparatory callback/store same-line (61/64). All compiled and linked. No improvement, so stop at the v2 five-variant budget; no two extra variants authorized. Baseline, cast, comma and prep-group remain exact 24 named relocation records and original extent in both regions. No new matching function. No new general compiler finding. `native-results.json` records flags, source hashes, original reference links and first mismatches.

## Accepted G2 donors and intermediate code generation

- USA `func_802121EC_5CD6BC`: canonical Wave194 source 45/45 with 4 named relocations; multiline historical control 41/45, first mismatch +0x10. Existing physical-line scheduling quirk independently reproduced, but tested dispatcher callback/store line grouping did not transfer.
- Japan `func_80003808_4408`: accepted direct increment 26/26; historical explicit-mask temporary 23/26 at +0x34; both nine effective relocations with independent numeric reference (existing proven synthetic small-offset provenance). Existing lifetime/mask sensitivity reproduced. No new general compiler law. Use historical `decomp/research/jp_dispatcher_20261125/factorial/replay.py` and its two pinned donor sources.
- `donor_scan.py` scanned every accepted USA 3,066 function span, verifying each original byte hash. No literal `lw a0,sp; addu at; jal; sw ...,at` sequence within this heuristic; one masked-two-register branch hit within ten subsequent instructions (mask 0xF/0xF0/0xFF): USA `func_801D825C_60363C`, a 52-byte accepted overlay47 C source. The source and reversed comparison both 13/13; wider int argument and explicit 255 mask with int argument both 0/13 (different extent); not an ABI-equivalent type outside the original byte domain. This establishes source operand reversal alone is not decisive; the donor's narrow incoming parameter cannot directly establish target local-byte behaviour. No claimed new universal compiler rule. The census is a narrow opcode heuristic, not a complete dataflow search or an exhaustive Japanese donor search.
- Six diagnostic `-v -Wc,-d` replays (baseline, cast, comma in both regions) retain the normal compiled .text and relocation multisets exactly. Sanitized generator branch register operands are [2,14] in every diagnostic; original MIPS branch uses [14,2]. This locates the comparison order at or before code generation, not merely final assembly scheduling. The abstract post-callback reload precedes the store in the generator trace but final expanded address arithmetic precedes the physical reload. The precise later scheduling phase remains unproven. No raw tool logs or generated original ASM are shipped.

Next distinct bounded hypothesis: use a scalar member assignment `ExitWord w; w.word=task->exit.word;` (not the already rejected aggregate copy `w=task->exit`) and preserve narrow byte member access; compare whether generator branch order changes before final instruction scheduling. Separately investigate numeric-vs-symbolic ABS offset representation for the post-callback store using independent reference provenance; do not silently relax named-relocation comparison. Neither hypothesis was compiled in this round because no first-mismatch improvement authorized extra target variants. Phase 2 literal pools and Phase 3 repeated stores have different proven mechanisms; no direct applicability claimed. Existing semantic host suite was not rerun because the selected source is unchanged; no new gameplay evidence. Candidate owner/full G2/strict inventory/promotion integrity NOT_RUN. Canonical ROM-free integrity passes for both regions.

## Replay

With authenticated canonical repo, two pinned upstream trees, original expanded ROMs and Splat target references, set the native environment per GOEMON_BUILD_ENVIRONMENT.md (`PYTHONPATH` includes repository), then:

```
python probe.py --repo REPO --usa USA --jp JP --work NEW_NORMAL_WORK
python diagnostics.py --repo REPO --usa USA --jp JP --normal NEW_NORMAL_WORK --out NEW_DIAGNOSTICS_WORK
python donor-line/probe.py --repo REPO --usa USA --jp JP --work NEW_LINE_WORK
python donor-byte/probe.py --repo REPO --usa USA --jp JP --work NEW_BYTE_WORK
python REPO/decomp/research/jp_dispatcher_20261125/factorial/replay.py --repo REPO --upstream JP --out NEW_JP_DONOR_WORK REPO/decomp/research/jp_dispatcher_20261125/factorial/src/func_80003808_4408_direct.c REPO/decomp/research/jp_dispatcher_20261125/factorial/src/func_80003808_4408_explicit_mask.c
python donor_scan.py --repo REPO --rom USA/config/usa/baserom.decompressed.z64 --out NEW_CENSUS.json
python validate_checkpoint.py
```

The original target host tests remain in `decomp/research/warp_phase4_20261126/`. Keep ASM and both canonical inventories unchanged. No ROM, toolchain, compiled original or extracted ASM is included. Hosted full regression on the updated draft head is separate from native matching.
