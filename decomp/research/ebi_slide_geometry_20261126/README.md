# Ebi Slide: geometry controls and instruction-tracer roadmap

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
