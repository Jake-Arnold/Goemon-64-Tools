# Original-USA / Japan-0 guest-RAM crosswalk: agent research protocol

**16 November 2026.** Use on the canonical decomp baseline `chatgptweb/decomp`; work on `decomp/*` branches, not toolkit feature history.

## Finding

A substantial set of original USA and Japanese **long-lived, fixed guest RAM fields** follows the address displacement

```text
JP candidate  = USA guest virtual address + 0x000057F0
USA candidate = JP  guest virtual address - 0x000057F0
```

The agreement is **systematic empirical evidence**, not a universal ROM correspondence rule. Examples with reported original Japanese in-game evidence:

| Field | USA | Japan | Status |
| --- | --- | --- | --- |
| Engine state | `0x800C7A94` | `0x800CD284` | Previously documented regional runtime |
| Map | `0x800C7AB2` | `0x800CD2A2` | Previously documented regional runtime |
| Character index | `0x8015C5DC` | `0x80161DCC` | JP switch 0/1 and original MIPS writer traced |
| Weapon index | `0x8015C607` | `0x80161DF7` | User cycled weapons, 16 Nov |
| Gameplay submode | `0x800C7AA4` | `0x800CD294` | User confirmed, 16 Nov |
| Map overlay observed byte | `0x8015C574` | `0x80161D64` | User confirmed, 16 Nov; NOT a safe toggle |
| Benkei encounter bit | `0x8015C60C & 0x20` | `0x80161DFC & 0x20` | User confirmed, 16 Nov |
| Sasuke party available | `0x8015C6A7` | `0x80161E97` | Previous JP runtime testing |

**Counterexamples and unverified cases:**

- JP Miracle Snowflake confirmed inventory byte `0x80162057`; USA `0x8015C866`. Difference **+0x57F1**, not naive `+0x57F0`. The Japanese array has a specific low-byte layout.
- JP proposed pause flag `0x800CD2D6` (USA `0x800C7AE6`) was reported **not to behave as the pause flag**; keep it disputed until a better trace.
- USA Sasuke first-battery event `0x8015C609 & 0x20` is confirmed; JP `0x80161DF9 & 0x20` remains a hypothesis.
- Original USA HP/Ryo/lives use 32-bit fields, whereas known Japanese GameShark cheats may target the *low byte/halfword* of an aligned word. Compare exact access width and byte offset.
- Original USA player pointers, temporary character object data,  `0x801C77E0` VM state, overlay-specific static locations, Impact allocated `0x802F7000` sample controller, and JP `0x80151B10` XYZ are **not safely offset-translatable** as a class.

## Mandatory action on *every* memory discovery in either region

1. Identify exactly which retail ROM/revision and guest-address context were used, including loaded overlay, scene, character and revision-specific symbol definitions. Never mix host process addresses, emulator RDRAM base, ROM offsets, segmented pointers, decomp VMA, code VMA and game-data fields.
2. Decide if the discovery is a persistent fixed global or saved-game event/inventory bit. For these two categories only, look for an *existing explicit paired field* and known exceptions; if missing, calculate the `±0x57F0` counterpart. If the field is dynamic, code, overlay, VM, external pointer or unknown-owner, **do not translate**; instead find the corresponding original functions/struct in each ROM.
3. Record *both* addresses, exact width/endianness, mask for packed event bits, source status, target status, and why the field is believed to be equivalent. The target defaults to **`offset-candidate`**, even where source is original-MIPS-proven.
4. Check the counterpart in original regional assembly (readers/writers, register-base arithmetic, lifecycle, caller/overlay resolution), or run an independent read-only event A/B/C with idle/control captures. Require meaningful state correlation and reversals or MIPS trace before claiming semantics. A single coincident equal value or changing byte is not proof.
5. Do not silently flip a field to `confirmed` or introduce a game-memory write, freeze or debug warp. Any controlled write test requires a separately justified and guarded gameplay experiment and confirmation of the original source semantics.
6. Publish a compact evidence record alongside the specific function/symbol discovery; update the decomp branch PROGRESS. If a mapping affects toolkit features, port the reviewed record to a main-based `toolkit/*` PR, **never merge decomp history wholesale**.

For source JP discoveries, do the same in reverse. Do **not** assume the USA address was necessarily previously identified; record the new USA candidate if absent.

## Standard research record

```yaml
source:
  region: "USA NG5E-0 / Japan-0"
  guest_vaddr: "0x........"
  width_bytes: 1
  endian: big
  mask: "0x.. | null"
  field_identity: "specific, or unresolved"
  owner: "fixed-global | packed-save-event | dynamic | overlay | code | unknown"
  scene_or_overlay: "if relevant"
  original_mips_evidence: "function and guest code VMA, source document, or none"
  gameplay_evidence: "A/B/control trials, user report date, or none"
other_region:
  guest_vaddr: "0x........ | unknown"
  derivation: "explicit | +0x57F0 | -0x57F0 | exception | not-applicable"
  validation: "offset-candidate | observed | instruction-traced | gameplay-verified | disputed"
  width_and_mask_validated: false
  supporting_evidence: "cite or unknown"
  contradictory_evidence: "specific conflicts or none"
  next_test: "concrete independent action"
  may_auto_write: false
```

## Operational reference

The canonical toolkit `main` branch now includes [the agent-facing regional crosswalk protocol](https://github.com/Jake-Arnold/Goemon-64-Tools/blob/main/docs/USA_JAPAN_MEMORY_CROSSWALK_2026-11-16.md) (PR #50). Separate draft toolkit [PR #43](https://github.com/Jake-Arnold/Goemon-64-Tools/pull/43) contains a 119-row read-only candidate registry, CLI and UI; those runtime features are **not** part of canonical `main`. A decomp-only checkout should apply this protocol without importing toolkit classes or assuming branch histories are synchronized.

When available in the toolkit checkout, machine-readable lookups:

```bash
python3 scripts/crosswalk_address.py --source usa --address 0x8015C60C --mask 0x20
python3 scripts/crosswalk_address.py --source jp --address 0x80162057
python3 scripts/crosswalk_address.py --source jp --address 0x80161F67 --kind saved-event --mask 0x08
```

**Proof boundaries:** Region-paired address hypotheses are not original-ROM byte-for-byte equivalence, native IDO matching, relocation inventory checks or original-symbol identity. Preserve full G2/matching-C criteria independently.
