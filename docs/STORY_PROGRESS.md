# Story progress panel

The panel now has internal subject tabs: **All**, **Fortune Dolls**, **Benkei & Kihachi**, **Ushiwaka & Training**, **Keys & Locks**, **Collectibles & Miracles**, **External annotations**, **Other story**, and **Diagnostics**. Each flag is listed once in All and in exactly one matching subject tab. Select a tab to work on that subject; its filter and editor still use live RAM.

Fortune Dolls includes silver/gold pickup flags, reward flags, the read-only quarter-progress word at `0x8015C704`, and the read-only annotated total at `0x8015C708`. Raw Bank A/B views are in Diagnostics, not interleaved with story quests. Live Memory no longer duplicates the entire story flag catalogue or the low-byte alias of the quarter counter.


Select an individual saved flag and choose **Clear** or **Set**, or select an
ownership word and choose **Absent** or **Present**, then click **Apply state**.
The selector initially shows the observed state. The write preserves other bits
in a packed flag byte, checks the displayed raw bytes before writing, and verifies
readback. A changing game thread can still race the write. Aggregate bank rows
are read-only. Writes are disabled in `--read-only` mode and during transition
states; edits do not automatically run rewards, cutscenes or scene transitions.
The separate saved mirror is not modified.

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
- Story rows are no longer repeated in Live Memory. The Ushiwaka summary and
  Unlocks remain available. The Achilles' Heel ownership word and its recorded
  reward flag are distinct, not duplicate flags.

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
