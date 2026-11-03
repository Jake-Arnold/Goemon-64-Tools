# External story-flag annotations added in v0.11.7

These entries come from pre-existing research, not the user's discoveries or
new semantic discoveries by this toolkit. The initial panel exposed only a
small curated subset; this update makes more external information usable.

Source: [abyssonym/mn64rando US parser dictionary](https://github.com/abyssonym/mn64rando/blob/9c580d03fe89354f79c3c83ba2e1bcf192f32577/tables/parser_config_en.yaml),
pinned commit `9c580d03fe89354f79c3c83ba2e1bcf192f32577`. Its numeric flag IDs are
mapped through the original game's already matched saved-bank accessor:

```text
address = 0x8015C608 + (flag_id >> 3)
mask = 1 << (flag_id & 7)
```

The pinned dictionary has 136 annotations inside the primary event-field range;
131 labels lack explicit question-mark/uncertainty markers. Before this update,
110 of those named IDs were absent from the 21-row curated tracker. This update
adds 37, leaving 73 other named annotations outside the displayed set. A named
external annotation is not equivalent to an individually verified meaning.

## Added areas and examples

The new rows cover the Super Pass/gate, early conversations/map, recruitment,
Chain Pipe, Mokubei/weapon upgrades, Koryuta, Wise Man/witch, boss milestones,
magic training instructions/success/failure/grants, priest/key dialogue, outer
space and minigame/travel signals.

| External annotation, paraphrased | Flag ID | Address / mask |
| --- | --- | --- |
| Super Pass receipt recorded | `0x000` | `0x8015C608 / 01` |
| Super Pass gate opened | `0x001` | `0x8015C608 / 02` |
| Koryuta freed | `0x014` | `0x8015C60A / 10` |
| Dharmanyo defeat recorded | `0x018` | `0x8015C60B / 01` |
| Sudden Impact grant recorded | `0x01C` | `0x8015C60B / 10` |
| Mermaid training success recorded | `0x01E` | `0x8015C60B / 40` |
| Super Jump grant recorded | `0x020` | `0x8015C60C / 01` |
| Yae recruitment recorded | `0x03A` | `0x8015C60F / 04` |
| Tsurami defeat recorded | `0x040` | `0x8015C610 / 01` |
| Super Jump training success recorded | `0x061` | `0x8015C614 / 02` |
| Outer-space arrival recorded | `0x06B` | `0x8015C615 / 08` |
| Mini-Ebisu start signal | `0x07D` | `0x8015C617 / 20` |

The code contains the selected 37 factual mappings and paraphrased labels with
attribution; it does not bundle the full third-party dictionary or require a
copy of that repository at runtime. Existing locally traced/user-tested entries
retain their separate provenance rather than being relabelled as imported work.

## Evidence and use

Every added numeric ID has references in the previously generated index for the
verified decompressed US ROM. The evidence column shows the number of aligned
opcode-pattern leads and a first decompressed ROM offset, followed by the explicit
**external annotation / not locally gameplay-verified** status. Pattern matches
are not complete CFG analysis, proof of execution, or independent verification
of the annotation's meaning. No new gameplay tests were requested to rediscover
the externally named states.

In **Story progress**, filter by **external** to show exactly the 37 added rows.
The filter also accepts names, addresses, masks and evidence text. Hidden rows
continue refreshing and return when the filter is cleared. Current total:
**58 named flags plus four bank/inventory watches = 62 rows**. Reads still cover
the same 28 canonical bytes because the added entries fit the sampled prefix.

Grant/recruitment/travel flags are progression records, not promises that a
whole-byte write grants inventory, runs callbacks or moves actors immediately.
Some are start signals rather than permanent completion milestones. The added
rows remain observational; no new write controls or automatic state repair were
introduced, and existing unsafe defaults are unchanged.

Validation: 218 Windows Python tests passed, including new external-ID/provenance
and cross-byte mask checks plus live filtering/hidden-row refresh. Actual read-only
Goemon64Recomp sampling returned all 62 rows with no errors; the real Tk panel was
visually inspected with the external filter active. This does not upgrade those
37 meanings to locally gameplay-tested status. No new executable or native build.

## Follow-up user note: Muscle Gym and story order

The user reports that the Kyushu disappearance flag (ID `0x017`,
`0x8015C60A & 0x80`) enables the Muscle Gym to appear in Oedo Town, allowing
story progression. The tracker now records that association with user-report
provenance; no new forced-bit or spawn-code validation was performed here.

Requested presentation follow-up: order named story milestones against the
previously supplied GameFAQs walkthrough (FAQ 3273), retaining alternate branches,
optional/retry states and evidence distinctions. This remains a follow-up rather
than assigning an unverified numeric-ID story order during decomp work.
