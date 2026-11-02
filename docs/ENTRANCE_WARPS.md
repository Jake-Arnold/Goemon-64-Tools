# v0.11.8 — Entrance-aware toolkit scene requests

The scene browser now reads original USA ROM entrance parameters instead of
reusing stale XYZ. It stages native pending coordinates before the existing
experimental `0x0C` reload, then makes one guarded position write to the loaded
player. This addresses the stale-coordinate problem; it does not establish that
the full native scene/collision/camera/script lifecycle is reconstructed.

The old exit-request route remains disabled. No new raw map-pointer writes or
velocity/collision-field guesses were introduced. Live warp testing was declined
for this checkpoint; simulated RAM, native-code review and ROM extraction are
separate evidence from in-game footing.

## Use

1. Restart the updated source toolkit using `Run.bat` from this checkout. Existing
   packaged executables have not been rebuilt.
2. In **Scene browser**, load your original USA ROM once if entrance data is not
   already cached. Retail `.z64`, byte-swapped forms and the verified decompressed
   build are accepted after normalization/checksum validation. Loading does not
   connect to or write a game process.
3. Select a stage and destination entrance. A unique route from the connected
   source room is preferred. When there is no such route, the native default
   spawn is selected if available. Ambiguous routes require an explicit choice.
4. Use the existing explicit experimental reload or native-menu button. The
   confirmation identifies the destination/coordinates. Selecting/double-clicking
   a stage remains read-only.

**Cancel scene request** stops monitoring/future placement; an engine reload
already requested can still finish. Read-only mode or disabling position restore
prevents placement. A stage without a decoded spawn is blocked before the reload.

The atlas is generated locally as `practice/entrances.json` for a source checkout,
or in the existing per-user toolkit data directory for a frozen executable.
It is ignored by Git. It contains functional entry metadata, not room assets or
a ROM. A failed new ROM load preserves the previous atlas.

## Extracted coverage

Both the original retail USA ROM (SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`)
and its verified decompressed build (SHA-1
`6ea0ed71032ce08fc2745f412d84936382197494`) produce the identical atlas:

| Data | Count |
| --- | ---: |
| Mapped room metadata entries | 333 |
| Instantiated ordinary exit definitions | 592 |
| Native save points | 14 |
| Flute points | 16 |
| Nonzero native default spawn records | 266 |
| Entry records combined | 888 |
| Distinct destination stages with coordinates | 266 |
| Mapped stages still without decoded coordinates | 67 |

The 67 stages have an all-zero native default record and no decoded ordinary
arrival/fallback point in this extraction. Some use special script/scene paths;
they are not assigned guessed origin coordinates. Duplicate grid references and
unused exit definitions are excluded. Multiple entrances into one stage remain
separate records. No complete special-entrance coverage claim is made.

## Data and native-code evidence

The pinned [mn64rando exit schema](https://github.com/abyssonym/mn64rando/blob/9c580d03fe89354f79c3c83ba2e1bcf192f32577/tables/entity_structures.yaml)
and room parser describe actor `0x08C`, destination room, raw X/Z/Y words,
direction and exit/mode bytes. Room metadata is read from file `0x0C` using the
known USA pointer table. The parser independently decodes the required LZKN64
blocks, checks metadata/group bounds and includes only instantiated definitions.
It never invokes the randomizer's mutating pipeline.

Native references reviewed in the checksum-verified baseline:

- `func_80215330_5D0800` reads the packed exit parameters and stages destination,
  coordinate, heading and mode fields through the system pointer. The surrounding
  transition flags/counters are not copied by this feature.
- `func_801CB5D0_5874E0` reads pending signed coordinates and converts them to floats
  for player creation; `func_800358E8_364E8` / `func_800357BC_363BC` forward them to
  `func_80035964_36564`, whose position stores are at object offsets `8/0xC/0x10`.
- `func_800214E4_220E4` indexes ten-byte default records at ROM `0x6C380`, guest
  `0x8006B780`. It copies three signed coordinates, heading and a mode word into
  saved entry fields, treating an all-zero triplet as unspecified. The save-load
  path copies those fields into pending entry parameters.

Consequently the toolkit float tuple is raw exit **X, Z, Y**: the randomizer's
`dest_z` is the height component shown as toolkit Y. Signed halfwords must not be
interpreted as large unsigned positions.

| Pending parameter | USA guest address | Width |
| --- | --- | ---: |
| Destination | `0x800C7CA0` | u16 |
| Entry mode | `0x800C7CA2` | u16 |
| X / height / horizontal | `0x800C7CA4/6/8` | three s16 |
| Heading | `0x800C7CAA` | u16 |

These are validated against the selected ROM record before sending the existing
reload request. The parameters are sent as one 12-byte block in canonical guest
byte order; failed pre-load staging restores the previous block only while still
in the unchanged source gameplay state and only if it still matches our write.
The source player object is not repositioned during staging.

After loading, placement requires the requested map, ordinary gameplay/phase,
no active load/transition/pause/script, matching global and task character IDs,
a stable player/task pair and the original connection. It rechecks the guard,
writes the three floats in one contiguous operation and records nearby readback.
It never rewrites actor IDs, guesses velocity offsets or repeatedly teleports.
Wrong maps, changed connections, disabled writes, cancellation, timeout or an
uncertain write end that request. Opening and cancelling a native menu alone is
not treated as a scene-load witness.

Cross-area logical checkpoints stage an integer approximation of their own saved
XYZ/heading before reloading, then retain the existing guarded exact-float/rotation
and progress restoration. They do not require an unrelated atlas entry. Overlapping
checkpoint/scene requests are blocked.

## Validation and limits

Tests cover ROM byte orders, decompression forms/truncation/limits, signed axis
ordering, actor/group selection, cache validation, full pending-block rollback,
loading/script/character/map guards, pointer changes, disconnect/cancellation,
failed/partial writes without retry, both RDRAM byte orders, default/ambiguous
entry selection, native-menu flow and checkpoint overlap. The scene browser was
rendered at 1280x900 and 1100x730 with both request buttons visible.

No live warp or anti-fall-through guarantee is claimed. Native reload, character
model selection, scene scripts, momentum and camera can still differ from an
ordinary door traversal. The feature supplies known coordinates and guards their
application; further in-game validation remains pending at the user's request.
