# Project-wide guest-data address authority for decompilation

The **single authoritative** USA/Japan guest-memory field catalogue is
`practice/data/address_catalogue_v1.json` from the toolkit repository's
`main` branch. The decompilation branch MUST NOT fork or manually maintain
a competing address/bit-mask list. Each named logical saved-event flag has
a USA/Japan pair, preserving exact mask, region, revision and source evidence;
the 2026-11-18 reviewed snapshot includes 142 named event bits **per region**.
An offset-derived JP candidate is not gameplay confirmation.

Decomp original-function/ELF/linker/ROM identities and accepted matching-C
counts remain authoritative **only** in `decomp/manifest.json` and its
original-ROM verified results. A RAM mapping is not a C symbol correspondence.

## Access the single reviewed source without copying it into decomp canon

After fetching the toolkit `main` ref, extract its pinned source bytes to a
temporary file and validate/read them with this metadata-only tool:

```bash
git fetch origin main
git show origin/main:practice/data/address_catalogue_v1.json > /tmp/goemon-address-catalogue-v1.json
python3 -m decomp.memory_registry /tmp/goemon-address-catalogue-v1.json
python3 -m decomp.memory_registry /tmp/goemon-address-catalogue-v1.json \
    --field crosswalk:japan:event:placed_silver_doll_0ca
```

The reader has no network access, game writes or code execution, and rejects
orphaned saved-event pairs. It accepts `crosswalk_status: "unresolved"`
without fabricating another region's physical address. For dynamic objects,
VM addresses, overlays, ROM offsets and original code VMAs, do not translate
by the static saved-data `+0x57F0` rule.

## Discovery writeback (decomp → canonical registry)

New guest-data findings on `chatgptweb/decomp` belong in the versioned
`decomp/address_discoveries_v1.json` discovery manifest once PR #56 is
landed. Record original address, region/revision, type/width, precise mask,
read/write MIPS site, confidence, lifetime and reciprocal proposed candidate
or explicit unresolved status. Review a **metadata-only PR targeting
toolkit `main`** to import these findings, regenerate the main canonical
registry and enforce reciprocal consistency. This is evidence transfer, not
a decomp code/history merge, automatic write permission or matching-C
promotion. Changes discovered in toolkit `main` are read from the same
registry snapshot by the command above. No parallel list is maintained.
