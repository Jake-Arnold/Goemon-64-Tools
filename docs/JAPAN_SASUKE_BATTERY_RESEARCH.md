# Sasuke Battery 1 — Japanese ROM research handoff

## Current evidence (15 November 2026)

All 33 other Japanese Unlocks rows are reported working by the user in live Project64 gameplay. **Sasuke Battery 1 remains the only unverified Japanese row**.

- USA known event byte: `0x8015C609`, bit `0x20` (USA field verified previously).
- JP hypothesis: `0x80161DF9`, bit `0x20`, from the recurring RAM displacement `+0x57F0`. This byte and mask have **NOT** been verified as a JP battery event.
- Prior matching MIPS read/store context for the JP aligned word `0x80161DF8` was associated with byte-initialisation/clearing activity. It does **not** demonstrate a battery-acquisition script.
- No independent Japanese cheat from [GameHacking.org](https://gamehacking.org/game/20438) identifies this specific battery-progress bit.

## Implemented next-stage toolkit probe

Event Sessions now provides a **Sasuke battery probe** preset (Japan only). It sets the 100-byte research start to `0x80161DC0`; captures cover `0x80161DC0–0x80161E23`, including candidate byte `0x80161DF9`. The old generic JP 100-byte range beginning at `0x80161D80` ends at `0x80161DE3` and was missing the proposed byte.

Selecting the preset is read-only: it only fills the label and capture range, **does not start a session, modify RAM, clear an existing session, or enable bulk writes**. The existing New Session / Capture A / Capture B / Record Trial workflow is reused.

## Verification protocol

1. Use a pre-battery Japanese savestate and the **Sasuke battery probe** preset in Event Sessions. Create a new session after selecting the preset.
2. Capture an idle/control A/B pair without collecting the battery. Record this as idle or control.
3. Restore the same pre-event state, capture A, collect only Sasuke's battery, capture B and record an event trial. Repeat the event from the same savestate several times.
4. Examine the ranked changed bits, specifically whether `0x80161DF9 & 0x20` changes consistently without appearing in idle/control captures. Also inspect other changed bits in the 100-byte region.
5. Verify causality through a reversible manual bit toggle and gameplay-state effects before promoting the battery to user-verified. No automatic write or guess promotion should occur merely from a changed bit.

The next research objective is the correct battery-acquisition flag, not a larger speculative offset sweep. This workflow is useful even if the existing guess is wrong.
