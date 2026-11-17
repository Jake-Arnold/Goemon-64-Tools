# USA / Japan rev-0 ROM room actor browser (read-only)

The **Room actors…** button in the toolkit's **Scene browser** opens a searchable table of original USA or Japanese rev-0 ROM placement records for the selected stage. This is static ROM inspection, not runtime attachment to either game.

1. In **Scene browser**, select a stage. For USA, choose **Load original USA ROM…** to extract both the existing USA entrance atlas and the USA actor cache. For Japan, choose **Load Japan actor ROM…** and select the original rev-0 Japanese .n64 or normalised .z64. The Japanese button extracts actor metadata only and **never** changes the USA entrance or warp tables.
2. Choose **Room actors…**, then select **usa** or **japan_0** from its ROM region selector. Filter by actor ID (e.g. `0x082`) or known label. The table includes actor ID, provenance, definition number, record offset, group offset and spatial grid cells.
3. Changing the stage selection updates the table. Caches load across launches after validating schema, region, checksums, identity and row counts: `room-actors.json` for USA and `room-actors-japan-0.json` for Japan. A Japanese cache cannot satisfy a USA lookup.

This is **not a live actor inspector**. It counts records from the game's *static room layout*, not actors currently instantiated in RAM. It does not read emulator memory, change actor state, create NPCs, or spawn anything.

The USA loader reuses the existing USA ROM validation and decodes 16-byte room definitions and 20-byte placement records as the entrance scanner, but preserves **every referenced placement record**. A shared group referenced by several spatial-grid cells is counted only once; repeated uses of the same definition at different offsets remain separate placements. Every source table offset is validated. It does **not** infer XYZ from unidentified record fields.

USA names are annotated separately: original-code / room research where identified, external/unverified when a matching label exists in the optional local USA research catalog, otherwise the numeric actor ID. Japanese shared-ID labels are explicitly tagged **USA ID label / Japan unverified** and do not inherit the USA external-only catalog. A label does not imply that an instance spawns under the current save or overlay conditions.

## CLI

```bash
python3 -m practice.room_actors --rom '/path/to/Mystical Ninja Starring Goemon (USA).z64' --stage 353
python3 -m practice.room_actors --rom '/path/to/Mystical Ninja Starring Goemon (USA).z64' --all --report /tmp/goemon-usa-room-actors.json
python3 -m practice.room_actors --region japan_0 --rom '/path/to/Ganbare Goemon (Japan).n64' --stage 353
python3 -m practice.room_actors --region japan_0 --rom '/path/to/Ganbare Goemon (Japan).n64' --all --report /tmp/goemon-japan-room-actors.json
```

The optional report contains placement metadata (no ROM bytes). Verified independent extraction:

| Region | File_12 overlay base | Room-pointer table offset | Mapped rooms | Placement records | Distinct actor IDs |
| --- | --- | --- | ---: | ---: | ---: |
| USA | `0x8020D2A0` | `0x24060` | 333 | 3,881 | 255 |
| Japanese rev-0 | `0x80212090` | `0x23F58` | 333 | 3,884 | 255 |

Japanese room-pointer table guest address: `0x80235FE8`. Japanese .n64 original (swapped) SHA-1 `b6386455c0b8f573e315976bbb47548cbafcedb3`; normalised big-endian Japanese SHA-1 `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b`. Extraction reports from original byte-swapped and normalised Japan ROMs are identical.

The six stages with different per-room placement counts are `49` (+2 JP), `304` (-1 JP), `305` (+5 JP), `363` (-1 JP), `463` (-1 JP), and `464` (-1 JP). All remaining mapped rooms have equal counts. Stage 353 (Oedo Town South) has 30 placements in either version.

## Validation

Focused parser tests: `python3 -m unittest tests.test_room_actors tests.test_room_actors_japan -v`.

Headless Linux Tk dialog test: `xvfb-run -a python3 -m unittest tests.test_actor_dialog -v`.

On 2026-11-17 the original USA and original Japanese ROMs were both SHA-1-verified and parsed without room-structure errors; the Japanese byte-swapped and normalised sources yielded identical actor reports. Six focused parser tests and one Linux/Xvfb dialog test passed in a reconstructed minimal source fixture. The **full repository suite and actual running-emulator UI integration were not run**, because the native environment could not clone GitHub. No original C/decomp build, actor-spawn hook, or live runtime verification is claimed.

## Next stage

A genuine **loaded actors** view requires recovering the live actor registry, actor allocation/free path and an in-game object identity field; a spawner also needs full engine initialization and script/overlay safety. Neither exists in this feature.
