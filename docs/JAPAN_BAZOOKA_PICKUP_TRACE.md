# Japan-0 Bazooka Pickup — Event Sessions Observation (15 Nov 2026)

## User-provided live evidence

The user captured two Japanese Project64 RAM states **before and after collecting the Bazooka**. The Event Sessions screenshot had a pre-existing session label **"Benkei first conversation"**, but the user expressly identifies the measured transition as **Bazooka pickup**.

The session was a 100-byte region beginning at **0x80161D80**, with **one event trial**, **zero idle trials**, **zero control trials**, **zero context-changing trials**, and **three changed-bit candidates**. The screenshot displayed **"ROM identity unverified"** for this event session. That is a session-provenance warning, not proof the game ROM itself is incorrect.

| Address | Bit mask | Observed change | Event support | Idle/control overlap |
| --- | --- | --- | --- | --- |
| `0x80161DBE` | `0x01` | Cleared (1→0) | 1/1 | 0 |
| `0x80161DBF` | `0x10` | Cleared (1→0) | 1/1 | 0 |
| `0x80161DBF` | `0x80` | Set (0→1) | 1/1 | 0 |

These are **observed changed bits**, not established Bazooka inventory flags. Their relative timing is consistent with the Bazooka action, but one before/after trial cannot distinguish the item acquisition flag from incidental dialogue, room state or other effects. The precise full old/new byte values were not displayed.

## Next verification

Repeat an idle/control capture, a pickup from a fresh prior savestate, and a comparable unrelated item pickup. Inspect Japanese inventory/weapon slot candidates (already source-backed in `practice/japanese_fields.py`) alongside the three changed bits. Promote a concrete Bazooka unlock mapping **only after its causal bit/address is identified**.

In the shared Unlocks table, **Bazooka remains `unknown` in Japan-0** until that mapping is established. Do not write one of these three candidate bits as a definitive Bazooka toggle.

## Other user-live-tested controls

User reports that Japanese Sasuke unlock, Yae unlock, Triton Shell, Cucumber, all fish counters, and scene teleports work. The initial failure to warp while currently controlling Sasuke (2) or Yae (3) was caused by `_normal_gameplay` accepting only character IDs 0/1. The fix accepts all four playable IDs and retains the same scene reload sequence.
