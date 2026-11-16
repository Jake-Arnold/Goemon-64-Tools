# Bundled numeric entrance coordinates

The **single repository-owned coordinate table** belongs here:

```text
practice/data/entrance-coordinates.json
```

This is a functional *data* file: destination scene ID, source scene,
entrance ID/type, numeric X/Y/Z, heading and mode, plus atlas provenance and
validation checksum. Do **not** put ROM bytes, game assets, save states,
extracted room geometry or copyrighted text assets here.

## Produce the table once

Use a locally owned original USA ROM, outside Git:

```bash
python3 -m practice.entrances \
  --rom "/path/to/original-usa.z64" \
  --output "/tmp/goemon-entrance-coordinates.json"
```

The command reads and identifies the USA ROM, extracts the numeric entrance
table and writes the validated atlas JSON. It prints a count of scenes and
entrances. Send **only the resulting JSON** for review/commit, or copy that
file to `practice/data/entrance-coordinates.json` in the Git checkout for
a local test. Never commit the ROM.

When this JSON is committed to the toolkit branch it becomes the preferred
lookup source for **both** USA and Japanese scene warps. No ROM or user cache
is required thereafter. The toolkit still supports validated per-user and
old-checkout caches as a fallback until this file is provided, and they do
not override a valid checked-in atlas.

Do not invent destination coordinates or collapse multiple entrances of
one scene to a single XYZ point. The existing validated atlas schema
(`goemon-usa-entrance-atlas-v1`) includes all known variants and a
checksum, and the GUI picks the unique source-specific/default entry or
asks for an explicit choice when ambiguous.

## Validate the checked-in data

```bash
python3 - <<'PY'
from practice.entrance_ui import repository_entrance_atlas_path
from practice.entrances import load_atlas
atlas = load_atlas(repository_entrance_atlas_path())
if atlas is None:
    raise SystemExit("No repository entrance atlas has been supplied yet")
print(len(atlas['payload']['rooms']), "scenes")
print(len(atlas['payload']['entries']), "entrances")
PY
```

The repository must not claim to bundle an exhaustive coordinate table
until this real extracted JSON has been reviewed and committed.
