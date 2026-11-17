# USA ROM room actor browser (read-only)

The **Room actors…** button in the toolkit's **Scene browser** opens a searchable table of original USA ROM placement records for the selected stage.

1. In **Scene browser**, select a stage. Choose **Load original USA ROM…** using the verified 16 MiB original USA game ROM. This creates the existing entrance atlas and a separate local actor placement cache.
2. Choose **Room actors…**. The window follows the selected stage and can filter by actor ID (e.g. `0x082`) or known label. The table includes actor ID, label/provenance, definition number, record offset, group offset and grid cells.
3. Changing the stage selection updates the table. An open ROM is not required on later launches if the independently checksummed cache remains valid. The local file is stored at the toolkit's practice-data directory as `room-actors.json`.

This is **not a live actor inspector**. It counts records from the game's *static room layout*, not actors currently instantiated in RAM. It does not read emulator memory, change actor state, create NPCs, or spawn anything.

The loader reuses the existing USA ROM validation and decodes the same 16-byte room definitions and 20-byte placement records as the entrance scanner, but preserves **every referenced placement record**. A shared group referenced by several spatial-grid cells is counted only once; repeated uses of the same definition at different offsets remain separate placements. Every source table offset is validated. It does **not** infer XYZ from unidentified record fields.

Names are annotated separately: original-code / room research where identified; external/unverified when a matching label exists in the optional local research catalog; otherwise the numeric actor ID remains visible. A label does not imply that an instance spawns under the current save or overlay conditions.

## CLI

```bash
python3 -m practice.room_actors --rom '/path/to/Mystical Ninja Starring Goemon (USA).z64' --stage 353
python3 -m practice.room_actors --rom '/path/to/Mystical Ninja Starring Goemon (USA).z64' --all --report /tmp/goemon-usa-room-actors.json
```

The optional report contains placement metadata (no ROM bytes). The real verified USA retail ROM yielded **333 mapped rooms**, **3,881 room placement records**, **255 distinct actor IDs**. Stage 353 (Oedo Town South) yielded 30 placements.

## Validation

Focused parser tests: `python3 -m unittest tests.test_room_actors -v`.

Headless Linux Tk dialog test: `xvfb-run -a python3 -m unittest tests.test_actor_dialog -v`.

In the 2026-11-17 feature implementation environment, the five focused tests passed against synthetic fixtures and the original ROM was parsed successfully. Full repository integration tests and live emulator UI acceptance were not run; host GitHub DNS was unavailable. USA-to-Japan actor layouts are not assumed interchangeable.

## Next stage

A genuine **loaded actors** view requires recovering the live actor registry, actor allocation/free path and an in-game object identity field; a spawner also needs full engine initialization and script/overlay safety. Neither exists in this feature.
