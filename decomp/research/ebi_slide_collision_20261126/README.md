# Ebi Slide collision follow-up: matched negative control and scale-dependent geometry

**2026-11-26 — RESEARCH_ONLY.** The long-standing Ebi Slide's landing-state movement mechanism is established in Test Q and PR #281. This follow-up strengthens the causal control and identifies the scale-dependent collision call path. It does not yet prove the exact wall-crossing decision. No new matching C, runtime changes or memory writes. Native IDO outcome NOT_RUN.

## Proven live control

JP Test Q and the same-wall no-C-Up control R each contain 180 consecutive samples with one controller poll per sample and 20 watches. Comparison of all fields other than serial and core frame is exactly equal over timeline frames 1–69. Across the entire timeline the sole input difference is buttons=8 versus 0 at frame 70; stick axes are identical. Q clip and fall were observed on video; R was blocked and remained miniature. Source trace SHA-256 fingerprints (private originals, not committed): Q `381019f6168a8b80d974e592ea0dc26de4bcd9a37c562c0650593d1b5320f871`; R `53e7c22109ef1a5bc184bd3af6828a9290ff882489216fc755f4cae2fc2c54ca`.

- At timeline 68 both take action 0D and have E4=2.8/E8=.7. At 69 both return to action 00 with those values retained and zero displacement.
- At 70, Q enters 8F and retains 2.8/.7; R enters 0D, changes E4 to .4095220864 and E8 to .1228566319. At 71 R enters 0F with 1.12/.336; Q stays 8F.
- Q reaches 2.8 horizontal units per core frame at 76, X=-357.693573 at 83, X=-361.75 at 84 (4.059370 horizontal displacement), and X=-364.547699 at 85 (2.800007 displacement). Y=0 throughout 8F. At 106 mini becomes zero, at 107 action 1A and Y=-.666667; Y=-548 at 180.
- R reaches X=-344.25 at 95, then approximately -344.248 despite sustained forward input through 120, with small tangential motion; Y remains zero. At 180 X=-344.244720, miniature=65535. The two exact contact coordinates differ by 17.5 units; their midpoint is -353. This is consistent with opposite contact boundaries but neither a single wall plane nor a radius of 8.75 has been proven. Do not infer wall thickness, radius or collision-disable flag from those coordinates alone.
- C-Up is required for this reproduced input sequence and prevents ordinary movement-profile recalculation. It changes action and potentially scale as well as velocity: this control cannot isolate which is causally sufficient for clipping.

## Original ROM inspection

Authenticated live `stable/decomp@8b195d8ce5a31723a71af428ee4f7bccf32b0bf8` source archive 15142908886, complete Git tree `3b7ec59747ce3557dd5b01d35ea94d1a8853e956`; upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`. Expanded Japan SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`, USA `6ea0ed71032ce08fc2745f412d84936382197494`, independently decompressed from supplied retail ROMs. Inspected original big-endian MIPS with supplied GNU objdump 2.45.90. Player overlay file_11 JP ROM 0x58CB60 VMA 0x801D0B90, USA ROM 0x587370 VMA 0x801CB460; main code ROM 0x1050 VMA 0x80000450. No original ASM or ROM bytes included. Regional pairs below are grounded by original call sites and instruction semantics, not a guessed address delta. Function labels are semantic research labels, not historical source names.

| Japan entry | USA entry | Observed role |
|---|---|---|
| 801D1228 | 801CBAF8 | accepted post-update: passes task+E4/E8 to movement; subsequent position application |
| 801D1BC0 | 801CC4C0 | movement/resolution orchestration |
| 801D29C0 | 801CD310 | movement-vector calculation, called before collision processing |
| 801D4FD0 | 801CF960 | collision orchestration, may retry |
| 801D548C | 801CFE24 | candidate displacement and geometry query pipeline |
| 801D5B6C | 801D04F8 | scale-dependent geometry probes; queries main geometry routines |
| 801D62AC | 801D0C64 | additional scale-dependent probes |
| 801D4524 | 801CEEA8 | further resolution / support processing |
| 801D2734 | 801CD084 | applies resolved displacement to player object and related object |
| 801FA6FC | 801F56EC | action 8F wrapper; clears context+86 on completion |
| 801FA744 | 801F5734 | shared transformation animation/scale routine |
| 801ECEA0 | 801E7D78 | quadratic interpolation helper |
| 8002E790 | 8002EB10 | main geometry query with repeated candidate tests |
| 800303B0 | 80030730 | second main geometry query with repeated candidate tests |

JP 801D1BC0 calls 801D29C0 at 801D1EE4 with E4/E8 arguments, copies task+68/+6C/+70 into a scratch displacement, calls 801D4FD0 at 801D1FDC (possible second call at 801D208C), then 801D4524 at 801D20FC. At 801D2124/2134/2144 it copies the resolved vector back into task+68/+6C/+70. 801D2734 adds the resolved displacement to object+08/+0C/+10 at 801D2788/27A4/27B8. Static original call path establishes collision processing remains in the common update; it does not prove every branch executes on Q frame 84. 801D4524 action filter at 801D460C..4624 excludes action 35–38 hex from a later branch; 8F is not excluded by this particular filter. Other conditional paths still exist.

### Scale changes during action 8F

Original JP 801FA6FC passes a1=0.0011718750465661287, a2=12.0, a3=0.10000000149011612 to 801FA744. The helper reads context+30 (u16) and object+28 (f32 animation frame); when phase=1 and animation frame<20, calls 801ECEA0 at 801FA800 with the animation frame, coefficient, 12.0 and 0.02500000037252903. The original helper computes `coefficient * (frame - 12)^2 + 0.025` using the original single-precision operation order (first `(frame-12)*coefficient`, then multiply by `(frame-12)`, then add). At 801FA808/80C/810 the result is written uniformly to object+1C/+24/+20; the completed transformation writes 0.1 to all three at 801FA84C/850/854. These are confirmed scale stores, not newly established fixed RAM addresses. Actual sampled scale at Q contact is still unknown. This is an animation-frame formula, not a mapping from timeline frames to animation frames.

USA wrapper 801F56EC calls 801F5734 at 801F570C; its scale branch calls 801E7D78 at 801F5818 and writes the same three fields at 801F5820/824/828. It also has a regional difference not present in the inspected JP helper: when context+59 is zero, USA 801F5768..5778 clears context+50 and task+A4/+6C. This is a conditional field reset (not proof of changed Ebi Slide outcome). USA live reproduction remains necessary.

### Collision probes consume the same scale fields

JP 801D548C receives the actor object pointer from task+18 and calls 801D5B6C at 801D56B8, then the secondary query path 801D62AC at 801D5910 or 801D5948. 801D5B6C uses object+1C multiplied by 70.0 at 801D5C40..5C4C on the ordinary branch (150.0 on the special-character predicate branch), and reads object+1C/+24 to scale horizontal probe offsets at 801D5D0C..5D64; object+20 scales vertical query extents at 801D5DD4/5DE0 and 801D5EF0/5EF8. It passes these dimensions to main routines 800303B0 at 801D5DF8 and 8002E790 at 801D5F0C. The secondary path 801D62AC uses object+1C/+24 times the original double literal 0.7 (ROM 0x5CB980), and object+20 times 185 and -30 at 801D6370..6430. In both regions this is a scaled geometry pipeline, not a fixed-size model. USA calls 801D04F8 and 801D0C64 from 801CFE24, and the former calls corresponding main queries 80030730 and 8002EB10. Further branch-by-branch USA geometry parity is unverified.

Main JP 8002E790 and 800303B0 query candidate geometry repeatedly, with selection/comparison of returned quantities, then copy a selected record. JP 8002E790 calls 8002A680 repeatedly; 800303B0 similarly calls 80031F28. 80030308 combines positive/negative component extrema from candidates. In 801D5B6C several candidate records are compared by squared displacement at 801D6178..61A8, and chosen result position is copied out at 801D6244..6260. This supports an active correction model, but the actual contact record and branch at Q84 have not been captured. Do not claim collision is disabled or prove side-selection solely from static reads. The 4.059-unit displacement may be a correction rather than true speed.

## Next controlled live experiment (same savestate, read only)

Keep the 20 watches from Q (including position_y); add four, using the verified dynamic JP task base T rather than a fixed address if it changes:

- `object_scale f32 8016F798->1C` (object+1C; all three scales receive same stores)
- `animation_frame f32 8016F798->28`
- `transform_phase u16 8016F7DC->30`
- `contact_flags u16 8016F7DC->0A` (observed field cleared at 801D5604; bit 0 set at 801D5974..597C only under a pair of scratch-result tests; NOT a proven wall-collision indicator)

Exactly 24 watches; reapply after load and relocate if task signatures change. Do not write or freeze any of these fields. First repeat known Q, then R (no CU); measure scale, animation phase and contact flags across 80–86 and 94–97, including completion. Next compare ordinary normal-sized running from equivalent position at 2.8, and a slower grounded transformation from the same miniature start. These separate the fast movement profile from size/animation state; contact phases will differ, so a subsequent approach-distance variation may be needed to match phase. A delayed forward hold during 8F can move wall contact later without changing the activation sequence. Preserve positive and negative controls, exact geometry and approach direction. If flags remain ambiguous, use read-only original-instruction-level logging of the geometry query inputs, selected result record and pre/post coordinates (not speculative new field names).

Base canonical counts: USA 3066 matching functions / 210636 bytes, Japan 3004 / 201000 bytes; delta 0. No native compile or fresh full-ROM candidate build attempted; original ROM authentication is not G2. Documentation only. Previous #281 checks green on old base but live stable advanced; refresh through non-force merge of latest stable into existing topic and require fresh full hosted CI. Keep all private captures and ROMs outside Git. The exact collision decision and USA live reproduction remain open.
