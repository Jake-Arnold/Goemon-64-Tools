# Ebi Slide: geometry controls and instruction-tracer roadmap

## Current checkpoint — 2026-11-26, after distance interventions

**RESEARCH_ONLY.** This refreshed record supersedes the earlier planning snapshot in PR #290; the latter and #281 remain historical evidence. All 14 geometry-enabled captures (Q/R, A1–A9, D1/D2 at 18/77, D1 at 19/77), 2,520 sampled frames, are represented below, with original hashes and negative controls. The first Q/R exports without geometry watches are separate baseline evidence; they contained only the old 24-watch schema. No private raw traces, video, savestates or ROMs are committed.

The earlier angle and distance plans have now been executed. Do not restart them by default. Fixed candidate near face X=-346, sampled correction radius 70*scale, and free candidate X79 explain all tested same-wall directional and distance outcomes. D1/D2 at 18/77 isolate X offset with identical precontact movement and identical Z79. A9 is rescued by D1. A7/A8 and both D1 runs demonstrate that far-side snapping is not required. Proposed per-update clipping window, for the tested geometry and state only: r < d < v_n, where r=70*scale, d is perpendicular center distance to the proposed face and v_n is the perpendicular candidate displacement. Strict boundary equality is untested; geometry and original branch not yet proved. This is not a universal wall or angle rule.

**Next exact task:** read-only instruction-level trace D1/D2 (18,77) on JP at relative step 79, first calibrating debugger/core frame and update identity. Compare candidate vector, wall plane and bounds, query return, chosen branch and applied displacement; then independently validate USA. Do not add arbitrary memory freezes or treat experimental private coordinate changes as a toolkit write authorization. Original Q timeline and watches are below. D1 X float bits C3A25275, D2 C3A21F41; original C3A238DB. All three new distance files confirm the one-time X edit survived the first 60 idle frames; animation phase differs until jump resets it. No native IDO attempts or new C/byte delta.

**Consolidation provenance:** live stable/decomp 863311ba349822c129cc257c10d6d9f7dba5ea73; successful source archive workflow 45897446676, artifact 15154367222; COMMIT.txt, SHA256SUMS and reconstructed Git tree 568867259bc104f2182e552a1fa063d871178b44 verified in a clean isolated snapshot. Direct Git DNS failed; GitHub connector publication. Reopened all 14 private geometry-enabled TSVs and two older baseline exports: all 180 rows each, hashes match the recorded records. Important qualification: A3 has a single 17-poll sample at relative step 132 (door-transition region, X=95), not at initial contact. All other samples in the 14 captures have one poll. Thus A3 initial contact comparison remains valid, but the complete capture is not strictly one poll per sampled row. The old 24-watch exports have SHA-256 Q 9cb9d89f9fa0cb7db5e71161a60daa30689ec5cc9e65453ca81f23c7e1e978e1 and R 37a72940cc13fd8116395365a6e90c12a8f9e98fb80e1b548ecba099f3f190cd. No new native ROM/ELF proof needed for these documentation-only changes; prior original instruction findings remain attributed to earlier verified research. Full hosted ROM-free gate and branch routing required before merge.

## Earlier original-instruction and Q/R roadmap (historical snapshot)


2026-11-26 — RESEARCH_ONLY; no matching-C promotions, no guest writes, native IDO NOT_RUN. Companion to [PR #281](https://github.com/Jake-Arnold/Goemon-64-Tools/pull/281) and merged #278. PR #281 carries earlier Q/R input, transformation and original collision pipeline evidence; its branch has diverged from current stable. This independent research-only topic does not copy or merge its history.

## Provenance and repeatability

Live stable/decomp 92ea1a5930eb75c6bc85a2799868bb6db2a0b8c5, source archive 15153308363, COMMIT.txt and SHA256SUMS pass; extracted Git tree 6513d4e1e46edd33d62e1de04454183bd338815b equals live tree. Direct Git DNS unavailable; inspect authenticated original ROMs in isolated scratch. Expanded JP SHA-1 6f8745fecc3a5e7d4918c7a73353eb0726116ded, USA 6ea0ed71032ce08fc2745f412d84936382197494 rechecked. JP player overlay ROM 0x58CB60 VMA 0x801D0B90, USA 0x587370 VMA 0x801CB460; main ROM 0x1050 VMA 0x80000450. No ROM, original ASM, saves or raw traces committed.

Private capture SHA-256: R 2c04df0f24440658b6b36be94c4fb032e53f38f68869182901566f1006470142; Q 6a2d4cae38960cdf6467fd3767ca4a18cd178588631dd451179971ff7c9607c4. Both 180 rows, 24 watch fields, one poll each, exact equality of shared fields except serial/absolute frame through relative step 69; only input difference Q button 8 versus R 0 on step 70. Verified directly with CSV reader. Previous 27-watch draft was rejected by 24-watch toolkit limit; v0.11.96 PR #277 fixes it (64 watches). Q and R used 24 watches with three redundant input fields removed.

Same JP-0 savestate; 180 core steps, Q:
```text
1-60 - 0 0
61 A 0 0
62-67 - 0 0
68 - 0 30
69 - 0 0
70 CU 0 30
71-120 - 0 80
121-180 - 0 0
```
R substitutes `70 - 0 30`. Preserve exact input and prior state; do not equate core frame and game update before instruction calibration.

JP watch additions (verify player identity before using the dynamic task pointers):
```text
object_scale f32 8016F798->1C
animation_frame f32 8016F798->28
transform_phase u16 8016F7DC->30
query_flags u16 8016F7DC->0A
geometry_result u16 80211856
geometry_aux u16 80211854
geometry_support u16 8021185A
```
Retain movement_e4/e8, action, callback, miniature, history, XYZ and controller inputs. Watch names provisional, not original symbol identities.

## Quantified controls

| Step | Q X | Q scale | Q flags/result/aux | R observation |
|---|---:|---:|---|---|
| 1 | -324.444183 | .025 | 31/154/0 | identical |
| 61–65 | -324.444183 | .025 | 0/0/0 | identical jump |
| 66 | -324.444183 | .025 | 31/154/0 | identical landing |
| 68 | -325.143127 | .025 | 31/154/0 | action 0D, E4=2.8 E8=.7 |
| 69 | -325.143127 | .025 | 31/154/0 | action 00; retained profile |
| 70 | -325.842072 | .025 | 31/154/0 | action 0D, E4=.409522 E8=.122857; Q action 8F retains 2.8/.7 |
| 71 | -326.940399 | .025 | 31/154/0 | R action 0F, E4=1.12 E8=.336 |
| 78 | -343.714844 | .025 | 31/154/0 | R still approaching |
| 79 | -346.510590 | .025 | 31/154/0 | Q passes R eventual blocking X |
| 80 | -349.306335 | .025 | 31/154/0 | |
| 81 | -352.102081 | .025 | 0/0/0 | R flags/result remain 31/154 |
| 83 | -357.693573 | .025 | 0/0/0 | |
| 84 | -361.750000 | .025 | 0/0/154 | planar displacement 4.059370; possible correction |
| 85 | -364.547699 | .025 | 0/0/0 | |
| 86 | -367.345032 | .02575 | 0/0/0 | first sampled growth |
| 95 | -392.512543 | ~.1 | 0/0/0 | R X=-344.25; aux=154 |
| 106 | -423.266510 | .1 | 0/0/0 | Q miniature clears |
| 107 | -426.060120 | .1 | 0/0/0 | Q starts falling, Y=-.666667 |
| 180 | -528.234680 | .1 | 0/0/0 | Q Y=-548; R X=-344.244720 Y=0 scale=.025 |

Across all 360 samples, flags zero iff geometry_result zero. Both go 31/154 -> 0/0 on jump and recover at 66. Q loses them at 81 and never recovers in capture; R keeps them. Q aux=154 only at 84; R aux=154 at 95–121 inclusive, clears 122. Support zero throughout both. This does NOT identify 154 as a particular wall ID or demonstrate a master collision enable flag. Passing R's eventual contact X precedes flags loss by two frames and growth by seven; exact wall plane and side correction not proven. The 17.5 difference between exact observed contact-like positions does not prove thickness or radius. Q and R differ in action and speed (and later size), so C-Up necessity for this sequence is not sufficiency of speed alone.

## Original instruction evidence (paired by code, not address heuristic)

JP/USA entry pairs: 801D1228/801CBAF8 post-update; 801D1BC0/801CC4C0 orchestration; 801D29C0/801CD310 vector; 801D4FD0/801CF960 collision orchestration; 801D548C/801CFE24 candidate/query; 801D5B6C/801D04F8 scaled probes; 801D62AC/801D0C64 secondary probes; 801D4524/801CEEA8 support/resolution; 801D2734/801CD084 apply vector. Action 8F 801FA6FC/801F56EC; scale helper 801FA744/801F5734; quadratic 801ECEA0/801E7D78. Main queries 8002E790/8002EB10, 800303B0/80030730. JP calls from orchestration: 801D1EE4 vector, 801D1FDC collision (possible retry 801D208C), 801D20FC support. Resolved displacement copied to task+68/+6C/+70 at 801D2124/2134/2144, applied to object XYZ at 801D2788/27A4/27B8.

| Scratch u16 | JP | USA | Independent original MIPS anchors JP / USA |
|---|---|---|---|
| result | 80211856 | 8020CA66 | clear 801D1FB0/801CC8B0; populate 801D6808 or 801D6810 / 801D11F8 or 801D1200; read 801D68FC/801D1300 |
| aux | 80211854 | 8020CA64 | clear 801D5614/801CFF90; store 801D5E90/801D0848, 801D5FA4/801D096C, 801D620C/801D0BC4 |
| support | 8021185A | 8020CA6A | store 801D53FC/801CFD94; clear 801D5468/801CFE00; read 801D466C/801CEFF0 |

All three are big-endian fixed-address temporary collision scratch, not persistent save fields. Explicit MIPS pairing delta 0x4DF0, NOT generic +0x57F0. USA live parity unverified. No write/freezing authorization. The result assignment includes a fallback 1 when the selected halfword is zero, so not every nonzero result is necessarily an ID.

Eight stores to context+0A per region: JP/USA clears 801D5604/801CFF7C, 801D6480/801D0E28, 801D690C/801D1310; OR bit 0 801D597C/801D02E0; bit 4 801D6620/801D1008; loop bits 1/2/4/8 801D68E4/801D12E0; mask F0FF 801D69EC/801D13E0; OR 0100 801D6B78/801D156C. Final clear is conditional on result zero. Four probe loop JP 801D6838–68F4 calls 80029A88 at 801D68C8; USA call 80029E08 at 801D12C0. Return 0x7FFF sets corresponding bits; probe directions not assumed cardinal. JP main wrapper calls 800322EC and 80029DE8; USA 8003266C and 8002A168. JP movement readers 801D2DE8 and 801D33B8 branch on low-five-bit mask == 0x1F. Trace execution needed to establish which stores actually run during Q81 and Q84.

Transformation helper writes object+1C/+20/+24 uniformly: coefficient .0011718750465661287 times (anim_frame-12)^2 plus .025 in original single-precision order, phase=1 and frame<20, final .1. USA has extra conditional context+50/task+A4/+6C reset (context+59 zero); not yet a demonstrated regional outcome difference. Ordinary probe branch uses scale*70 (special predicate *150), secondary horizontal offsets scale*.7 times direction components, vertical scale*185 and -30. At .025, 70*scale=1.75; E4 caps 1.12 versus 2.8. Treat speed > probe distance and 51.3-degree angle from wall normal as toy hypotheses only; a real collision decision depends on actual candidate vector, plane, finite polygon, probe orientation, and branch order. User reports angle and starting distance influence success; not yet quantified.

## Staged experimental roadmap

1. Read-only capture sweep now: Q/R anchor each session. Vary ONLY sustained input on 71–120, X=0,+/-5,+/-10,+/-20,+/-30,+/-40 with Y initially 80,77,74,69 as appropriate (record actual raw values and movement; controller inputs are NOT world angles or constant speed). Keep frame70 identical to Q. For each capture classify blocked, clip, wall missed, transformation failed or indeterminate; repeat near boundary, not just successes. Measure world X/Z vectors from precontact frames, record actual planar speed, angle relative to reconstructed wall normal only when known. Distinct wall segments or changing yaw are confounds.
2. Distance/contact phase sweep: from Q alter sustained start by delaying full forward input 1,2,3,4 frames (70 unchanged) and capture the full run. This changes velocity and animation/contact phase; it is a screening experiment, not an isolated distance test. Later prepare independently positioned savestates with sub-unit offsets, same orientation/action/scale and verified input history. Sweep signed starting distance in 0.25–1 unit increments, include no-wall control. Never infer plane from only two X contacts.
3. Toolkit tracer capability gate: separate toolkit topic from stable/toolkit. Use an isolated Mupen64Plus 2.6.0 debugger-enabled core (DEBUGGER=1; debugger config enabled; pure interpreter first). Confirm documented DebugSetCallbacks, DebugBreakpointCommand, DebugGetCPUDataPtr and step/resume support against actual loaded version/capability. Existing Frame Inspector is core-callback based; non-debug RAM pointer access is not instruction tracing. See https://github.com/mupen64plus/mupen64plus-core/blob/master/doc/emuwiki-api-doc/Mupen64Plus-v2.0-Core-Debugger.mediawiki and https://mupen64plus.org/wiki/index.php/UIConsoleUsage . If stock debugger cannot capture pre/post state reliably, add narrowly scoped native core/plugin instrumentation in an isolated research build, not ROM patches. No arbitrary guest memory writes. Keep original normal core available.
4. First tracer implementation: register region-specific original VMAs only after ROM/overlay identity checks. Capture player task identity, relative core frame, monotonic player-update ID, PC, call depth, arguments/return values, selected GPR/FPR bits, flags and scratch halfwords. Start with entry/exit of common post-update and actual displacement application; correlate one known Q/R capture against stock emulator before adding probes. Respect MIPS delay slots and distinguish pre/post instruction, callback boundary, actual PC vs next PC. Bound event count and bytes; capture overflow explicit, never silent drop. Preserve pause/load/stop synchronization, disable trace on overlay/task change, no GUI roundtrip per instruction, export private JSON/TSV. Verify neutral run, known breakpoint hit, one-step semantics, non-player negative control, and Q/R stock-vs-debug trajectory equality; reject non-deterministic captures.
5. Expand narrowly to JP 801D29C0, 801D548C, 801D5B6C, 801D62AC, 801D68FC/690C, 801D5E90/5FA4/620C, 801D4524, 801D2734 and paired USA entries/stores. Capture function arguments, candidate displacement pre/post each call, all relevant branch outcomes and query return IDs; at actual selected geometry record, decode polygon vertices, normal and signed distances only after mapping struct via original code. Limit detailed capture to Q timeline 75–87 and R 90–100; instrument player-update IDs once calibrated. Compare which first branch differs at comparable contact, and whether the frame84 correction is candidate displacement or geometry response.
6. Offline model: compute measured wall normal n, start point p, proposed displacement d, signed plane distance n dot (p - vertex), perpendicular speed n dot d, probe positions, polygon bounds and chosen correction. Reimplement actual original query ordering and float precision from recovered semantics; replay the captured input records. Distinguish candidate vs final position and collision vs no support. Predict held-out angle/distance tests on same wall then at least two geometrically different walls. Record misses/false positives, not just accuracy on training trials. If no swept test, establish which discrete test misses; if plane-side selection chooses wrong face, demonstrate the exact branch and correction. Do not equate geometry_result with wall presence.
7. Causal interventions only after read-only tracing: separately reviewed guarded experiments on private savestates with update-synchronized temporary E4/E8 overrides at verified consumption points. S ordinary miniature running with normal profile; T transformation with miniature profile; baseline Q/R unchanged. Record effective movement (not just caps), phase, scale, yaw and resulting trajectory. Use several intermediate velocities, restore original code/data after each run; no persistent freezes or writes in ordinary practice. If test cannot maintain equivalent starting state, classify confounded. Independent USA live reproduction with verified regional pointers and original callback pairing required.
8. Native matching-C recovery is an independent decomp task with fresh stable archive, ownership checks, COMPILER_QUIRKS every attempt, exact native IDO, whole-unit/ROM/ELF/relocation/inventory proof and full hosted CI. No promotion based on a gameplay model or tracer. Research complete when mechanism predicts held-out successes AND failures with original branch-level evidence; no arbitrary claims of universal angle threshold.

Toolkit v0.11.96 PR #277 already includes 64-watch support. Tracer is a proposed separate feature, not implemented. Current research PR #281 is behind stable and needs fresh regression before merge. This research-only topic changes documentation and address-discovery metadata only; delta zero C/bytes. Tests: original trace equality, input diff, flag/result equivalence and both ROM SHA-1 verified; no native compilation. Hosted full regression and routing required before merging.


## Completed experiments — preserved original research notes

Source: [PR #290 comment 7203790922](https://github.com/Jake-Arnold/Goemon-64-Tools/pull/290#issuecomment-7203790922).

## Q-A1–A4 directional sweep — 2026-11-26, 21:29 UTC (RESEARCH_ONLY)

720 private TSV samples parsed; each trial contains 180 rows and identical sampled gameplay state through step 70 (ignoring absolute serial/frame). Same Q timeline, only steps 71–120 changed. A1 (+5,80) and A2 (-5,80) both process to (0,73), every non-serial/frame/requested-X field identical for all 180 rows: deadzone duplicates, not independent angles. A3 (+20,77) processes to (13,70), A4 (-20,77) to (-13,70); both enter 8F at 70 with E4=2.8/E8=.7, scale .025 through 85, same growth sequence, mini clears at 106. A3 user reports blocked then ordinary door entry; A4 video (sampled 1,3,5,7.5 s) shows wall approach, outside blue geometry, falling. A1/A2/A4 fall at 107 and Y=-548 at 180. A3 remains Y=0, action 0F at 107, 10 hex at 121; later position discontinuity consistent with user-reported door transition. No map ID captured.

| Trial | X,Z at 78 | Precontact speed at 78 | Heading from negative X toward positive Z | X,Z at 79 | X,Z at 84 |
|---|---|---|---|---|---|
| A1/A2 | -343.714844,-124.002670 | 2.800014 | -3.1641° | -346.510590,-124.157219 | -361.75,-124.929962 |
| A3 | -343.178436,-127.329468 | 2.800006 | -15.2733° | -344.25,-128.083557 | -344.228607,-131.346649 |
| A4 | -343.563416,-120.735840 | 2.800004 | +8.6038° | -346.329315,-120.300140 | -361.75,-117.866951 |

A3 is a better negative control than R for collision: retains action 8F, 2.8/.7 profile and same scale/animation schedule; actual approach speed 2.8, yet blocked at exact X=-344.25 on 79, aux 154; flags=31/result=154 after landing for entire capture. A1/A2/A4 clear flags/result at 81, aux 154 only at 84 and clear at 85. All three successful trials snap to exactly X=-361.75 at 84, despite different Z and prior X: A1/A2 planar displacement 4.059370, A4 4.416158. Strong evidence of axis-aligned correction, not an increase in movement speed. Support=0 throughout all four.

### New quantitative wall hypothesis

During A3 growth at steps 87–95, X = -346 + 70*scale within 0.000022 units for all nine samples; at miniature first contact X=-344.25=-346+1.75, full scale X=-339=-346+7. R previously blocked at same miniature coordinate. Candidate near collision face X=-346. Successful far correction X=-361.75 is consistent with candidate opposite face X=-360 minus 1.75; alternate explanations remain possible (e.g. inflated bounds/other fixed margin). Do NOT claim actual polygon vertices or 14-unit thickness established.

Extrapolate the free movement vector from steps 77 and 78 using same per-step heading rotation and magnitude. Predicted uncorrected X at 79: A1/A2 -346.510590; A3 -345.874992 (predicted Z=-128.083538 vs actual -128.083557; X actual -344.25); A4 -346.329320 (actual -346.329315). A3 falls ~0.125 units short of proposed near face; both success directions cross it. This supports a discrete side-selection hypothesis: if the next point crosses the near face before correction, near-side collision may be skipped; subsequent far-side correction pushes player out. Not yet instruction-traced, not a universal threshold. Z also differs so geometry segment/end effects are confounds. A3's direction changes gradually even at fixed stick, so input is not a fixed world angle.

Next: keep 1–70 same; test 71–120 at (0,77),(10,77),(15,77),(18,77),(19,77) against A3 (20,77), record all outcomes. Distinguish wall miss/door entry from blocked/clip. Compute predicted X at first contact, then test starting distance independently on same geometry. Read-only instruction tracer should first log the candidate and selected result at 79 and 84 (A3 vs A4), then inspect exact polygon/plane and branch selection. No memory writes.

Private TSV SHA256 A1 7d7fc32d78d02b94e500ad7cb51a19869f070ff0c3570643d7b697a9293de0d8; A2 ab36143a4ebc92205db829332de1df63daf8ea31433da87d8a865f05f99acd5d; A3 4fee0fc89ff1ac83e9d500f487ab9d9faeb98d8a9766132b0a4a81f0f9248a87; A4 1eca944228cec50c8a0a8842e06e64776722b5bd2ddcf4805700d620637b74ba; video b521787e94fe66a1df5e676a3966bf7d054ade7b852b3b3d14fcce99e0efa6f4. Private inputs not published. Stable/decomp advanced to 863311ba349822c129cc257c10d6d9f7dba5ea73; PR #290 parent is older, so preserving this evidence as a PR comment rather than pushing a stale branch. Historical status at the time of the comment; consolidated here on the refreshed base. Native IDO NOT_RUN, zero promotion delta.

---

Source: [PR #290 comment 7203853317](https://github.com/Jake-Arnold/Goemon-64-Tools/pull/290#issuecomment-7203853317).

## Held-out directional threshold sweep Q-A5–A9 (RESEARCH_ONLY)

Five private TSVs, 900 samples, one poll per frame, all sampled fields identical through relative frame 70 except absolute serial/frame. Same Q timeline; only sustained stick 71–120 differs, Y=77 throughout. Predicted uncorrected X79 computed before classification by extrapolating precontact displacement in complex X/Z space: p79*=p78+(p78-p77)^2/(p77-p76). This assumes approximately constant rotation ratio; compared against actual free trajectories, not the original engine algorithm.

| Test | Requested / processed X | X78 | Predicted X79 | Actual X79 | Actual X84 | Y180 |
|---|---:|---:|---:|---:|---:|---:|
| A5 | 0 / 0 | -343.714844 | -346.510590 | -346.510590 | -361.75 | -548 |
| A6 | 10 / 3 | -343.636108 | -346.417098 | -346.417297 | -361.75 | -548 |
| A7 | 15 / 8 | -343.442383 | -346.187967 | -346.187744 | -359.879639 | -548 |
| A8 | 18 / 11 | -343.312439 | -346.033763 | -346.033691 | -359.581757 | -548 |
| A9 | 19 / 12 | -343.204285 | -345.905296 | -344.25 | -344.228912 | 0 |

All five precontact planar speeds at step 78 within 0.000015 of 2.8. A8 heading -13.300592 degrees from negative X toward positive Z, A9 -14.932000 degrees. A8 candidate crosses inferred X=-346 by 0.033763; A9 candidate misses by 0.094704. Extrapolated X79 agrees with successful actual X to <=0.000224 units in these four clips; predicted A9 Z=-127.970768 vs observed -127.970810 (X correction). The earlier A3 negative control also predicted X=-345.874992 and resolved to -344.25. Fixed X=-346 rule proposed in prior comment correctly classifies all five held-out trials, plus earlier Q/A1–A4; not a universal rule and Z changes concurrently.

A9 repeats near-side growth correction X=-346+70*scale over steps 87–95, max absolute residual 0.000015945. A9 flags/result remain 31/154 from landing step 66 to end; aux=154 on 79–95, 97–119 and 121; end Y=0. No map transition asserted for A9. A5–A8 flags/result clear at 81, action 1A at 107, Y=-548 at 180; support zero in all samples. Importantly A7/A8 NEVER have nonzero geometry_aux, and never snap to -361.75: X84=-359.879639/-359.581757 and movement continues at ~2.8 per update. Thus the one-frame far-side correction in Q/A1/A2/A4/A5/A6 is NOT required for successful clipping. This falsifies the stronger earlier two-face-correction-as-necessary explanation; near-face miss is the best supported common event. The far-face plane at X=-360 remains a hypothesis. Need original query branch/plane reconstruction.

Next discriminating control: preserve A8/A9 transformation and steering, independently adjust starting X with verified otherwise-equivalent private save states (A9 ~0.2 closer to candidate face, A8 ~0.2 farther); predicted reversal if threshold is causal and the same face is sampled. Avoid unverified writes; validate position/yaw/scale/speed and actual frame-79 displacement, treat altered camera/initial history/geometry as confounds. Prioritize instruction-level tracer at step 79 for A8/A9; optional far-side comparison at 84 for A6/A7. Do not infer an angle-only threshold or generalize to other walls.

Private SHA256 A5 056b3b770df4044901371ea3f444fc1f7f1bb0f7b39635ddf5caa381daf4fedd; A6 8647ad97fe4085706966e86b905780edd7b770c74980264ad05589e756f7d7dd; A7 93678e24f7f889321fa377dfe0bc2746c36c536114a014c7ec0cda461a9413fe; A8 a29b27969c42882358a9358669ca3319ba38e91a5816a174407754cd114fb305; A9 0f62722456ada4ce08ccc6ae8927a2ab218fc381fd5151f86a77793bd2e3bda1. No raw traces committed. Live stable/decomp 863311ba349822c129cc257c10d6d9f7dba5ea73 remains ahead of PR #290 base; record in discussion pending refreshed source checkout and integration into research README/PROGRESS. Native IDO NOT_RUN; zero C/byte delta; no source changes.

---

Source: [PR #290 comment 7203943944](https://github.com/Jake-Arnold/Goemon-64-Tools/pull/290#issuecomment-7203943944).

## Distance intervention D1/D2 — both pre-registered reversals observed (RESEARCH_ONLY)

Three private 180-row JP traces (540 samples), one poll per frame. User applied one-time starting X changes: D1 float bits C3A25275 = -324.6441955566406, D2 C3A21F41 = -324.2441711425781; baseline -324.4441833496094, actual offset +/-0.20001220703125. Idle animation phase differs from original traces during frames 1–60 (extra emulator updates while editing); jump resets it, frames 61–70 identical to respective A8/A9 controls except X and absolute frame/serial. Starting X adjustment survives through idle/jump. User ran both offsets with (18,77), then D1 with (19,77).

| Trial | X78 | Predicted free X79 | Actual X79 | Actual Z79 | Y180 |
|---|---:|---:|---:|---:|---:|
| D1 18/77 | -343.512451172 | -346.233775494 | -346.233703613 | -127.458282471 | -548 |
| D2 18/77 | -343.112426758 | -345.833751080 | -344.250000000 | -127.458282471 | 0 |
| D1 19/77 | -343.407470703 | -346.108902378 | -346.108917236 | -127.957069397 | -548 |

Prediction method unchanged from angle sweep, complex X/Z displacement extrapolation. D1/D2 18/77: exact same precontact X displacement, Z trajectory, Y, scale, action, E4/E8 and controller samples as original A8 from 61–78, with constant X offsets through 78. Same precontact speed 2.79998957 and heading -13.3005924 degrees. Actual Z79 identical despite opposite outcome. D2 correction from predicted X=-345.833751 to -344.25 is +1.583751. During 87–95, D2 X=-346+70*scale within 0.000021428 units, reinforcing near-face hypothesis. D1 19/77 differs slightly from A9 in Z after step 74 and X offset by up to 0.003174 extra by step 78 (heading -14.888828 vs baseline -14.932 degrees); actual candidate crosses by 0.108917, no longer blocked. This is not a bit-identical trajectory in every field, but the 18/77 pair isolates distance much more tightly.

D1 both: flags/result clear at 81, no auxiliary geometry hit at any sample, action 26/fall at 107, final Y=-548. D2: flags/result stay 31/154 after landing, aux=154 at 79–95 and 97–121, clears 122, Y=0 throughout after landing. Support zero in all 540. Both previously specified predictions (A8 +0.2 blocks, A9 -0.2 clips) hold, plus D1 A8 clips as expected. Near-plane crossing common to success, far-side correction not necessary. Fixed X=-346 threshold correctly classifies new trials and prior same-wall sweep; no claim of universal threshold, exact geometry or original branch proof.

For the (18,77) pair, pre-step79 signed distance from candidate plane = 2.487548828 (D1) vs 2.887573242 (D2); normal displacement 2.721252441 from D1's actual uncorrected update. Candidate model: if preceding center lies beyond inflated contact boundary r=70*scale=1.75 and next center crosses plane, near-face may be bypassed. This is a hypothesis conditional on same geometry/state, not general collision code. Next priority read-only instruction tracer at frame79 D1/D2 18/77 (same direction, same Z at contact) to record candidate XYZ, exact geometry polygon/normal, query branch, return and resolved vector. No additional direction sweep needed before this. Optional sub-unit boundary test at constant 18/77 start X ~-324.410492 (from baseline actual X79+346; uncertainty original float rounding and camera), but no need for more tests to justify tracer.

SHA256 D1 18/77 ce6d394119efefd48dc6a2bc78fb1e678f001cd12709efb3d7257cfc6df57f10; D2 18/77 5f873313710a0c136a0c8fca7244a4d0671db7f1e283337b596219739b1b3cb6; D1 19/77 54448d286a6802ea6a30730f7a49263f3a5da3a237215c06ee56bffec2377a02. Private inputs not published. Live stable/decomp 863311ba349822c129cc257c10d6d9f7dba5ea73 remains ahead of PR base. Historical status at the time of comment; now consolidated here. Native IDO NOT_RUN; no source changes or promotion delta.
