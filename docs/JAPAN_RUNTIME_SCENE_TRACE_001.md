# Japanese Mupen64Plus live scene transition: observation 001

Observed from an actual running **Japan-0** ROM in Mupen64Plus on 2026-11-15. The toolkit was connected to an external Linux PID and reading the word-swapped guest RDRAM; no writes were used.

Full machine-readable snapshot: `research/japan_scene_runtime_2026-11-15.json`.

## Supplied live read-only comparison

- PID **959604**; host RDRAM base **0x7AA843EC0000**; memory **wordswapped**.
- Two snapshots only. The transition method, exact in-game position and whether a debug-menu jump or regular doorway was used were **not supplied**. Do not infer which route the player travelled from these values alone.

| Field (JP guest address) | Before | After | Interpretation |
|---|---|---|---|
| Total time raw (`0x8016205C`, u32) | `0000D500` | `0000D506` | Counter +6; unit unknown |
| Current scene candidate (`0x800CD2A2`, u16) | `012C` (300) | `0163` (355) | Current scene changes |
| Submode candidate (`0x800CD294`, u8) | `01` | `02` | Consistent with USA-observed overworld→town mode categories; not separately proven for JP |
| Previous scene candidate (`0x800CD2AC`, u16) | `0163` (355) | `012C` (300) | Becomes exactly the old current scene |
| Pending scene candidate (`0x800CD490`, u16) | `012C` (300) | `0163` (355) | Follows destination/current at sampled endpoints; actual pending transition timing unknown |

The repository's **USA-derived scene catalogue** names stage 300 **Kai Highway** and stage 355 **Oedo Town (Northwest)**. These are catalogue names only; an on-screen location confirmation for the JP release was not included in the capture. No scene-number translation or remapping is applied.

## Confidence change

**Runtime observed (single user trial):** JP `scene_map`, `scene_submode`, `scene_previous`, `scene_pending`. These four fields are now annotated as observed once, not merely generic offset candidates. The UI retains "repeat to confirm" wording. The Japanese time watch was already cheat-backed and is observed advancing by six raw units; unit conversion to seconds or frames remains unjustified.

**Still unverified in Japanese play:** JP `scene_phase`, `scene_transition`, `scene_exit`, `scene_pause`, `scene_character` and `scene_loading`. Absence of these names from the change list does not prove static semantics, only that raw values did not change between the two sampled endpoints.

The `+0x57F0` USA-to-JP offset remains an **address-specific hypothesis**, never an automatic rule for player objects, tasks, actor pointers or overlay functions.

## Toolkit changes

`practice/japanese_scene_probes.py` now resolves known scene numbers to their names in read-only displays and reports the single-trial runtime evidence separately. `practice/japanese_fields_ui.py` includes catalogue names in the copied before/after report for scene-related fields, labelled as USA-derived and not yet independently confirmed for Japanese. The normal Japan RAM access remains read-only; no scene warps, writing or cheat activations were introduced.

## Next validation gates

1. Capture the reverse transition **355 → 300** and an unrelated scene pair. Compare current, previous and pending IDs.
2. Confirm observed locations visually against catalogue labels; a debug-menu jump alone may produce different previous/pending behaviour.
3. Capture memory at **during-load** boundaries to determine whether `scene_pending` truly holds the upcoming destination before it becomes current. A two-snapshot diff cannot establish ordering.
4. Test player-character swaps or map transitions for `scene_character`, `scene_loading`, `scene_phase`. Nothing here identifies JP player pointers or positions.

This is an evidence upgrade for scene-state discovery, **not** a Japanese native Goemon64Recomp build or proof of a stable scene-write API.
