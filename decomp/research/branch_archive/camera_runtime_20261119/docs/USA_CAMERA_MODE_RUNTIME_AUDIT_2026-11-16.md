# USA camera mode — runtime-to-original-code audit (16 November 2026)

This report preserves a user's Project64 3.0.1.5664 observations and maps them to original-USA assembly. It is **research evidence only**, not a matching-C promotion. The original retail USA ROM SHA-1 is `df8083a54296b8c151917c5333e1c85f014a2a66`; the decompressed 32 MiB source image was authenticated as SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. Original assembly was extracted locally from the pinned upstream checkout `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`. Splat emitted file_11 but the full multi-overlay run exceeded the environment timeout; no new complete build is claimed. No ROM bytes, assembly files, user screenshots or gameplay recordings are committed.

## Runtime evidence

| Address / field | Width | Interpretation |
|---|---:|---|
| `0x800C7B00` | 16 bits | Global default camera-mode input, **not necessarily the effective camera mode** |
| `0x801FC624` | 32 bits | Pointer `P` to active camera task; observed `0x8016A090` in town |
| `P+0x98` | 8 bits | Effective task `mode_id`; at observed P, `0x8016A128` |
| `P+0x73` | 8 bits | Provisional `pending_mode` (upstream camera structure) |
| `P+0xD1` | 8 bits | Provisional `current_mode` (upstream camera structure) |
| `P+0xD2` | 8 bits | Provisional `scripted_mode` (upstream camera structure) |

The user observed `0x800C7B00 = 2` in tested outdoor town/overworld gameplay, `0` during loading transitions and sustained indoor gameplay, and a return to `2` outdoors. Manual alternate values changed camera perspective in a screen recording. These observations support camera-mode selection rather than raw zoom-distance control. Values are not an exhaustive enum. Re-read the camera pointer after scene transitions. USA addresses should not be transferred to the Japanese ROM by a single guessed offset.

## Authenticated original function boundaries

`file_11` maps compressed-source-independent decompressed ROM `0x587370` to runtime VMA `0x801CB460`, so `VMA = 0x801CB460 + (ROM_offset - 0x587370)` within this overlay only.

| Original function | Original ROM range (end excluded) | Bytes | SHA-256 |
|---|---|---:|---|
| `func_801F97D4_5B56E4` | `[0x5B56E4,0x5B576C)` | 136 | `f6266809ac26ff75f44d5f23cab8c15ae338e6185b88b69ec85bd83dfb7c0b8a` |
| `func_801F9988_5B5898` | `[0x5B5898,0x5B5AB8)` | 544 | `e46bafeb74679758d09c3b199ae65f11dad8033e7cfa5ee3916593274fe3b8a2` |

These boundaries and slice digests were checked against the original extracted USA assembly and decompressed ROM. Both functions are in the current **assembly-owned** canonical `file11_152` chunk `[0x5B43A4,0x5B65D4)`. Total 680 bytes is a bounded *research ceiling*, not newly matched C.

### Reset helper: `func_801F97D4_5B56E4`

At PC `0x801F97E8` / ROM `0x5B56F8`, `SH zero,0x2E41(at)` zeros halfword `0x800C7B00` (observed during entering a building). It also clears the adjacent words `0x800C7B04/08/0C` and loops over **10 records of 0x28 bytes each**, clearing their u16 mode/selector and nine 32-bit fields. The reset-table base is `0x800C7B10`. This is an instruction-backed reset helper, not proof of a unique indoors-only call site.

### Mode and region updater: `func_801F9988_5B5898`

At PC `0x801F999C` / ROM `0x5B58AC`, `LHU t6,0x2E41(t6)` reads the global u16. PC `0x801F99AC` / ROM `0x5B58BC`, `SB t6,0x98(t7)`, writes its low byte to the camera task. The same function converts global signed 32-bit XYZ values from `0x800C7B04/08/0C` to float fields at `P+0xC0/C4/C8`; it copies the low byte of the halfword at `0x800C7CA2` to task `P+0xBC`. Those task fields correspond provisionally to `path_pos` and `mode_group` in upstream camera C.

**Crucial additional behaviour:** the function checks an optional camera-region table starting at `0x800C7B10`, ten records at stride `0x28`. Each record has a u16 mode/selector at `+0x00`, six signed-int X/Y/Z boundary fields at `+0x04,+0x08,+0x0C,+0x10,+0x14,+0x18`, and three signed-int camera-position overrides at `+0x1C,+0x20,+0x24`. When region comparisons succeed, PC `0x801F9B20` / ROM `0x5B5A30` stores the low seven mode bits to `P+0x98`; the region's XYZ overrides are converted to float task fields. The comparison bounds and record meanings remain provisional.

**Therefore the task mode is not guaranteed to equal the global mode:** region processing may replace it. This refines the earlier interpretation of `0x800C7B00` as the final camera mode.

## Duplication audit

- `klorfmorf/mnsg` upstream `camera` branch already provides about 4,657 lines of provisional camera C, including `CAMERA_TASK_WORK`, `func_801D4828_590738`, and all four initially targeted task-mode fields. Reuse it; do **not** re-decompile the earlier camera controller. The two traced original functions sit later than the scope of this camera.c draft.
- Canonical `chatgptweb/decomp`: as inspected, **315 verified matching-C functions**, including **152 in file_11**, 16,660 accepted original instruction bytes, and 7,048 assembly entries. The verified manifest and `file11_152` fixture still assign both target functions to assembly.
- Reviewed pending sources on PR #23 (the file11 expansion fixture waves), PR #24 (transition-52 research files) and PR #41 (next-eight file11 callbacks at `0x5A6F30–0x5A7090`). No candidate covering either `0x5B56E4` or `0x5B5898` was identified. This is a targeted overlap review, not a claim that every historic branch underwent a native compilation audit.
- Earlier work on the same camera-mode global and visual zoom experiments is **reused as evidence**, not counted as a new discovery.

## Next bounded technical work

1. Trace callers of the **136-byte reset function** and identify the ordinary-gameplay writer that restores `0x800C7B00=2`. This is a smaller, more controlled C candidate than the 544-byte region updater.
2. Independently verify region record meaning, comparison boundaries, and camera position source under different maps; do not guess enum labels.
3. Only for original-address functions not already claimed elsewhere, try a small IDO 5.3 `-O2 -mips2 -G0` matching-C hypothesis. Preserve original symbol references and exact bytes/relocations. If the candidate differs, keep ASM.
4. A matching isolated probe is **not** production acceptance. A reviewed opt-in mixed-C/ASM stage still requires a complete 32 MiB original USA ROM match, all 8,825 file_11 semantic relocations, the 7,376-function inventory, full local CI, and canonical manifest promotion.

## Checks and limits

Local analysis authenticated the decompressed USA ROM and both original function slice SHA-256s, mapped all four PC/ROM pairs, and inspected canonical/pending fixture ownership. Three new Python `unittest` cases were run: without a ROM, 2 passed and 1 optional-ROM test skipped; with the authenticated decompressed ROM supplied, **3/3 passed**. No new IDO candidate, complete rebuild, combined G2, full repo local CI, Japanese proof or C promotion was run. Machine-readable source-only evidence: `decomp/results/usa_camera_runtime_trace_20261116.json`. Test: `tests/test_decomp_camera_runtime_evidence.py`.
