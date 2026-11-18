# Project64 read-only saved-event writer probe — USA/Japan

These original-ROM research scripts capture CPU register values when a native saved-event setter executes or when another instruction writes the watched saved byte. They never modify game memory. Project64's JavaScript debugger API and interpreter core are required. **No live Project64 test has yet been performed**; host-mock tests and original-ROM MIPS-anchor checks passed.

## Original instruction evidence

| ROM | Original 32 MiB SHA-1 | Ghost byte | Mr. Arrow byte | Setter entry | Final SB instruction |
| --- | --- | --- | --- | --- | --- |
| USA NG5E | 6ea0ed71032ce08fc2745f412d84936382197494 | 0x8015C63B | 0x8015C628 | 0x80024038 | 0x80024084 |
| JP rev-0 NG5J | 6f8745fecc3a5e7d4918c7a73353eb0726116ded | 0x80161E2B | 0x80161E18 | 0x80023CF8 | 0x80023D44 |

The final SB writes byte 0(V0) in the JR RA delay slot. At that instruction, A0 retains the native flag ID and RA holds the caller return address; RA-8 proposes the conventional JALR callsite, pending checking the actual caller.

Four additional original MIPS **computed-ID setter** calls exist in resource 43 at offsets +0x608, +0x63C, +0x670 and +0x10C8 in both regions. Each calls via JALR T9 and loads flag ID from actor +0xD4 into A0 in the delay slot. The first three use an actor state at +0xD1; the fourth also tests actor +0xD6. **It remains unproven** that the instantiated Ghost Toys actor type 0x195 or the pickup actor type 0x87 calls any of these four functions.

## One short capture

1. Run the original USA or Japanese retail ROM in Project64. In Options > Settings enable advanced settings and debugger, select **Always use interpreter core**, and preferably disable **Pause emulation when window is not active**.
2. Load the target scene before starting the script. Put goemon_flag_trace_usa.js (USA) or goemon_flag_trace_japan_0.js (Japan) in Project64's Scripts folder, then start it through Debugger > Scripts.
3. Activate one Ghost Toys torch or collect Oedo Mr. Arrow. Copy the [GOEMON ...] console line or screenshot the paused Commands debugger registers. The line includes PC, A0, RA, S0, V0, old byte and native caller candidate.
4. NATIVE_SET proves the instruction path reached the native setter for flag 0x19A/0x19B/0x19C/0x104. OTHER_WRITE is some other instruction modifying a watched byte and requires further inspection. Ignore save-load and scene-initialization hits. Resume with F4 only if necessary.

**Manual fallback:** Debugger > View Memory > navigate to the target byte > right-click Write Breakpoint, or Ctrl+W. Record the current instruction and A0/RA when paused. References: https://hack64.net/docs/pj64d/ and https://hack64.net/docs/pj64d/apidoc.php

## Tests and proof boundaries

- Both original regional ROM SHA-1s validated; native final store and four original resource-43 JALR/LHU delay-slot sites checked in each image.
- Both JavaScript files passed Node syntax checks and a two-region synthetic debugger API test that exercises address selection, target flag filtering, caller registers and other-writer fallback without modifying RAM.
- No actual Project64 debugger script execution, game trace, IDO C compilation, fresh full-ROM G2/inventory or full local decomp CI. **No C function promotion.**

## Oedo key/door runtime crosswalk — 18 Nov 2026

[Paired USA/JP evidence and original-MIPS callsite map](../../docs/OEDO_KEY_DOOR_JP_RUNTIME_CROSSWALK_20261118.md). The USA flag/door semantics were already documented on 3 November; the incremental finding is a **Japanese live Project64 interpreter trace** that independently confirms the pickup flag `0x114`, lock flag `0x113`, and original `file_43` return PCs.

- **`oedo_key_door_japan_0.js`** monitors JP scene `0x00D` door and key event `0x114`, plus saved byte `0x80161E1A`.
- **`oedo_key_door_usa.js`** watches the independently established USA counterpart at `0x8015C62A`. **No live USA trial of this new script has been performed.**
- Both use targeted read/write and set/clear/test execution hooks only, detect either Project64's legacy `gpr` API or the newer `cpu.gpr` API, and **never pause or write game memory**. Enable interpreter core, close other active scripts, and confirm the ROM region before running. These are narrow Oedo probes, not a general flag tracer.
- Reproducible ROM-free mocks: `node decomp/research/pj64_flag_trace/test_oedo_key_door_mock.js`, **4/4 PASS** across both region profiles and both register APIs. These new scripts were not themselves used for the original live capture; their predecessor JP v5 script was.
