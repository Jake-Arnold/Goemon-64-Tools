# Repository-bundled warp entrance coordinates

`practice/data/entrance-coordinates.json` **is now committed** to this
repository. It is the validated original-USA ROM numeric entrance atlas
provided on 16 November 2026:

- 333 indexed room IDs.
- 888 distinct entrance records, covering 266 destination rooms.
- 592 exit records, 266 native default spawns, 16 flute points and 14
  save points.
- ROM identity: `df8083a54296b8c151917c5333e1c85f014a2a66`
  (SHA-1), checked by the original extractor.
- Atlas checksum:
  `980a9676b364af83f48437c5fa421dc9dc9e64a82ef8954cad52f4a11b0e7a90`.

The JSON contains **only functional numeric entrance metadata**:
destination scene ID, source scene when applicable, entrance ID/type,
X/Y/Z, heading and mode, and validation provenance. No original ROM,
models, scripts, audio, textures, game saves or other game assets
are distributed.

The toolkit loads this checked-in file by default for both USA and
Japan; no ROM extraction or local cache is needed. Existing per-user
and legacy caches remain available as fallback only if the packaged
table is missing or invalid. A scene can have several entrances, so
the user selects by destination AND specific entrance/source route.

## Updating the source data (only when necessary)

If a verified newer extractor or correction is needed, use a locally
owned original USA ROM outside Git:

```bash
python3 -m practice.entrances \
  --rom "/path/to/original-usa.z64" \
  --output "/tmp/goemon-entrance-coordinates.json"
```

Review changes against the committed atlas, verify the extracted count,
schema and SHA256 checksum, and commit **only the JSON** after review.
Never commit the ROM. For a real coordinate correction, retain multiple
entrance positions rather than collapsing a scene to one XYZ.

## Verify the checked-in table

```bash
python3 - <<'PY'
from practice.entrance_ui import repository_entrance_atlas_path
from practice.entrances import load_atlas
atlas = load_atlas(repository_entrance_atlas_path())
assert atlas is not None
assert len(atlas["payload"]["rooms"]) == 333
assert len(atlas["payload"]["entries"]) == 888
print("Verified repository atlas:", len(atlas["payload"]["rooms"]),
      "scenes,", len(atlas["payload"]["entries"]), "entrances")
PY
```

`tests.test_repository_entrance_atlas` also asserts the shared original-USA
Oedo South entrance is `(-289, 0, -167)`, heading 256, mode 16, that
other entrances to that room remain distinct, and that the atlas loads
without reading a ROM.
