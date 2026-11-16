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

## Mandatory agent workflow for every new USA or JP memory discovery

**Agent trigger:** any newly discovered RAM address, typed field, mapped bit,
original MIPS read/write site, or regional mapping correction. Apply the
procedure **in the same research task**, whether the first discovery came
from USA or Japan. The goal is *automatic candidate generation*, **not**
automatic verification or editing.

1. **Pin the input identity.** Source ROM region/revision (USA NG5E-0 or
   Japan-0), guest virtual address, read width, byte order, event bit mask,
   current scene/character/context, type of memory and evidence provenance.
   Translate *guest RDRAM* addresses only; host/ASLR process offsets and
   compressed ROM offsets are not interchangeable with them.
2. **Classify ownership** before any arithmetic: fixed/long-lived system
   global; saved inventory and packed event flags; or dynamic pointer,
   overlay, code VMA, VM resource, scene-scoped allocation, or unknown.
   Only the first two categories qualify for an offset **hypothesis**.
3. **Resolve known mappings first**, including field-width differences and
   explicit exceptions. On the toolkit branch use the registry in
   `practice/region_memory_crosswalk.py`; for decomp-only checkouts read
   this document and the toolkit branch's published registry. New source
   USA field: `candidateJP = addressUSA + 0x57F0`. New source Japan field:
   `candidateUSA = addressJP - 0x57F0`.
4. **Produce a paired entry** in research notes for both regions, even if
   the counterpart is unknown, with the status **offset-candidate**, not
   `verified`, and an explicit test plan. If a field name/mask already
   exists, compare its independent regional evidence rather than creating a
   duplicate. Do not assume widths, masks or packed layout are unchanged.
5. **Validate independently** by reading the candidate against the expected
   event/variable in the other regional build, preserving an idle/control
   sample; use original MIPS readers/writers or a reversible guarded
   gameplay test where warranted. A single equal value or raw A/B
   difference is evidence, **not proof of causality**. Record failures and
   conflicting evidence just as prominently as positives.
6. **Promote only with explicit evidence**, date, scene and target ROM
   identity. No speculative auto-writes, freezes, warps or changes to
   production unlock flags. Commit the test and both-region mapping record
   on the relevant feature branch; follow separate toolkit/decomp PR bases.

### Practical agent lookup (both directions)

```bash
# Existing USA story flag -> explicit JP match and original mask.
python3 scripts/crosswalk_address.py --source usa --address 0x8015C60C --mask 0x20

# Japanese Snowflake -> explicit USA exception (not naive subtraction).
python3 scripts/crosswalk_address.py --source jp --address 0x80162057

# Unlisted fixed USA global -> JP hypothesis only.
python3 scripts/crosswalk_address.py --source usa --address 0x8015C777 --kind static-global

# Unlisted Japanese persistent flag -> USA hypothesis only.
python3 scripts/crosswalk_address.py --source jp --address 0x80161F67 --kind saved-event --mask 0x08
```

The CLI returns machine-readable JSON with field key, both addresses,
mask/width, evidence status and notes. If an address is unlisted it
**requires** a supplied `--kind` before generating a target candidate.
Known dynamic/VM examples are rejected; the denylist is illustrative,
not proof that any other address is static.

### Evidence record template for future agents

```yaml
discovery:
  source_region: usa | japan
  source_rom_revision: NG5E-0 | Japan-0
  source_address: "0x8015C60C"
  source_type: saved-event | static-global | dynamic | overlay | unknown
  field_name: benkei_encounter
  guest_width_bytes: 1
  endian: big
  bit_mask: "0x20"
  source_evidence: "exact original script / gameplay A-B / source file + commit"
  scene_and_character: "explicit or unknown"
crosswalk:
  target_region: japan
  target_address: "0x80161DFC"
  derivation: "explicit pair / +/-0x57F0 candidate / known exception"
  target_status: user-confirmed | offset-candidate | disputed | conflict
  target_evidence: "tested observation, citation or unverified"
  independent_validation: "A/B, idle control, MIPS access, game-visible effect"
  write_permission: false
  unresolved: "specific remaining test and conflicting hypotheses"
```

Use the template as an evidence checklist; the example address and labels
must never be copied as new facts for unrelated discoveries.

### Width and exception examples

| USA finding | JP counterpart | Scope |
| --- | --- | --- |
| `0x8015C607` weapon select | `0x80161DF7` | User-confirmed static byte |
| `0x800C7AA4` gameplay submode | `0x800CD294` | User-confirmed state byte |
| `0x8015C574` map overlay | `0x80161D64` | User-confirmed observed value; not a safe toggle |
| `0x8015C60C & 0x20` Benkei | `0x80161DFC & 0x20` | User-confirmed event bit |
| `0x8015C5E0` u32 max HP | JP cheat reads low byte `0x80161DD3` | Low-byte accessor, not independent JP u32 validation |
| `0x8015C866` Snowflake | `0x80162057` | Explicit **+0x57F1** exception |
| `0x800C7AE6` pause candidate | `0x800CD2D6` | **Disputed; do not promote** |
| `0x8015C609 & 0x20` first battery | `0x80161DF9 & 0x20` | **Unverified JP** |
| USA player object `0x801FC60C` | No offset mapping | Dynamic/lifetime-sensitive |
| USA script VM `0x801C77E0` | No offset mapping | VM resource/overlay scope |

The fixed-data relocation rule is strong evidence for **finding where
to look**, not a license to treat every 8 MiB address as its counterpart.
