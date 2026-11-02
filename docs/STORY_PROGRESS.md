# Story progress panel

Open **Story progress**, next to Unlocks. It refreshes from the connected US game
on Recomp or Project64 through the existing guest-memory reader. v0.11.7 displays
21 curated story flags, 37 additional external annotations, two raw bank views
and two inventory-word watches. See [external source/evidence details](EXTERNAL_FLAG_CATALOG.md).
These are the mappings already documented by gameplay, original-ROM traces and
credited existing annotations; the panel does not claim new flag discoveries.

## What it adds

- Benkei milestones: encounter, first dialogue, fight, later Miracle Item
  condition and Kihachi referral.
- Ushiwaka flag-derived stages: introduction, blue/yellow/red fish requests,
  fish reward, temple stage, training passed/failed/declined and grant recorded.
  Success takes priority over failure in the mapped temple dispatcher; a
  declined offer takes priority over the failure branch. Individual bits remain
  visible even when multiple conditions are set.
- Kihachi food/hint and Miracle Snow-recorded state, plus the existing Baron-in-Iga
  observation, with address, bit mask, raw byte and evidence labels.
- Separate word watches for Mini-Ebisu ownership (`0x8015C6F0`) and Achilles' Heel
  inventory (`0x8015C70C`). Their low bytes are the existing `C6F3`/`C70F` watches;
  their progression flags are different fields.
- Bank A/B first-16-bit raw views, explicitly labelled as storage with unknown
  lifecycle/scene meanings. They do not reuse saved-bank semantic labels.
- Matching named rows in Live memory, and a clearer Ushiwaka summary/link from
  Unlocks. The stale Achilles' Heel candidate label in Live memory is corrected
  from the original reward-script trace.

The registry is a selected set, not an automatic confirmation of every
randomizer annotation. Filter **external** to see the 37 added source annotations;
names, addresses and evidence are searchable too. Source details and unresolved roles remain in
[the ROM report](ROM_FLAG_TRACE.md), [Benkei/Kihachi tracing](BENKEI_KIHACHI_TRACE.md)
and [the Iga evidence note](IGA_CUTSCENE_LEADS.md).

## Reading advisories

If Mini-Ebisu's grant flag is set while ownership is zero, the panel points out
that the reward branch may be skipped. If ownership is present without the grant
flag, it reports that combination separately. The same separation applies to
Achilles' Heel inventory and its progression flag. Unexpected ownership-word
values are shown explicitly rather than treated as a normal binary record.

These are observations, not a complete validation of the save. Samples are
sequential and can straddle dialogue/script writes or reloads. A discrepancy may
be temporary or caused by intentional manual edits. The panel does not repair
memory, execute callbacks, award items, move actors or change existing unsafe
defaults. Location, character and untracked conditions can affect actual dialogue;
the summaries are mapped milestones/conditions, not a complete scene predictor.

When disconnected or a read fails, affected values become **Unavailable**, never
silently zero/clear. Independent bank/inventory reads can remain available.
Refresh updates existing rows to retain selection and scrolling. The horizontal
scrollbar makes the evidence column accessible on smaller windows.

## Validation and delivery

218 Windows Python tests passed, including packed stages, mixed pass/fail state,
branch priority, inventory discrepancies, per-bank isolation, partial reads,
disconnect handling and read-only GUI operation. Model reads total 28 canonical
guest bytes per sample and never write memory. Actual read-only sampling on
running Goemon64Recomp succeeded with all 62 rows and no read errors; it displayed
Mini-Ebisu ownership present with the grant flag clear. The actual Tk layout was
visually inspected. Project64 uses the same previously validated connection/
byte-order adapter but was not rerun live for this panel.

Restart from this task checkout (`Run.bat`) to receive v0.11.7. Existing running
copies and packaged executables are not changed automatically; no new executable
was built. There is no user-data migration, new raw capture file or runtime
dependency. The portable C and matching-decomp source are unchanged.
