# USA/Japan guest-memory crosswalk: scoped +0x57F0 rule

**16 November 2026; experimental v0.11.32 toolkit feature branch.**

## What is supported

Multiple independently checked USA/JP *static* fields share a guest address
delta of `0x57F0`. Recent Japanese live-game reports confirmed:

| Field | USA | Japan | Evidence |
| --- | --- | --- | --- |
| Equipped weapon index | `0x8015C607` | `0x80161DF7` | User cycled `01/02/03` |
| Gameplay submode | `0x800C7AA4` | `0x800CD294` | User-confirmed |
| Map overlay state | `0x8015C574` | `0x80161D64` | User-confirmed; not a safe toggle |
| Benkei first encounter event (`& 0x20`) | `0x8015C60C` | `0x80161DFC` | User-confirmed |

Existing Japanese unlocks include **33 user-tested entries** from 15 November
(source and field provenance in `practice/region_unlocks.py`). The *separately
identified* Sasuke first battery byte `0x80161DF9 & 0x20` remains unverified.

The proposed Japanese pause value `0x800CD2D6` is **disputed**: the user did
not observe it behaving as the pause-menu flag. It remains a labelled research
row only. Other game/scene-state candidates similarly require isolated tests.

## What has been added to the toolkit

`practice/region_memory_crosswalk.py` builds one field registry from:

1. Explicitly scoped static global addresses from the existing USA and Japan
   tools, including the four user-confirmed fields above;
2. All 34 existing USA/Japanese unlock crosswalk entries;
3. All *named* saved USA event flags in `CURATED_FLAGS`;
4. All `PLASMA_FLAGS` from existing USA original-script annotations.

Every row records both addresses, mask (when applicable), width, provenance
and evidence status. Most Japanese story flags remain **offset candidates**.
A mask is essential: several story events share the same byte.

The toolkit's **Japan Live (diagnostics) → USA → JP crosswalk** panel can
refresh raw Japanese memory, capture a baseline, compare later reads and copy
changed fields. All actions in this new panel are **read-only**. A changed
byte does not confirm that the assigned story-event meaning is correct.
Prior edit, freeze, reload and unlock permissions have not been expanded.

Export the complete named catalogue as CSV:

```bash
python3 scripts/export_region_memory_crosswalk.py > goemon-usa-jp-crosswalk.csv
```

No ROM, running emulator, memory writes or personal data are required.

## Critical boundaries

- **Do not apply the delta universally.** USA VM globals, script cursors,
  dynamically allocated Impact controllers, player-object/task pointers,
  loaded overlays and code VMAs are excluded from automatic conversion.
- Known Japanese layout exception: the Miracle Snowflake byte is
  `0x80162057`, whereas `0x8015C866 + 0x57F0 = 0x80162056`.
- The Japanese published Max HP/Ryo/Lives cheat fields are low-byte or
  low-halfword accessors into USA-style full-width words. The registry labels
  those *subfields* rather than claiming every Japanese full word verified.
- The USA item slot at `0x8015C5F3` converts to a Japanese address described
  as fish riceballs by the existing Japanese field catalogue. The role is
  **unresolved**, explicitly labelled `conflict`.
- Japanese saved-event *bitfield region* translation is a testable hypothesis,
  not verification of every mapped event.
- No automatic candidate promotion into existing writable toolkit controls.

## Validation

ROM-free unit tests live at `tests/test_region_memory_crosswalk.py`.
They cover the new reported mappings, bit masks, known exceptions,
negative evidence, exclusion of dynamically allocated/VM fields, read-only
reads, big-endian values and baseline diffs.

The Ubuntu workflow [43972242638](https://github.com/Jake-Arnold/Goemon-64-Tools/actions/runs/43972242638) passed **301 ROM-free non-GUI tests (300 passed, 1 skipped)** and **124 Xvfb Tk GUI tests**. This includes the added registry and Tk smoke tests. The registry comprises **119 named entries** (27 static, 34 unlock, 45 curated story and 13 Plasma flags).

Synthetic tests do not replace checks against the actual USA/Japan games.
A Japanese live runtime comparison and Windows regression are still required
before calling the new story translations validated.
