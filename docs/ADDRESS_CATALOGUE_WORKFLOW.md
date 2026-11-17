# Goemon Memory Address Registry — canonical source and research workflow

## Source of truth

The versioned **`practice/data/address_catalogue_v1.json`** is the authoritative source of actual N64 guest byte addresses, widths and packed-bit masks consumed by toolkit runtime controls. **The registry is not a second, manually maintained watch list.** Unlocks, Story Progress, Japanese memory fields, the reciprocal USA↔Japan crosswalk, parts of the inspector and the new Live Memory catalogue resolve their known addresses by stable registry ID through `practice/address_registry.py`.

Existing Python modules retain their UI labels, input validation, game-transition logic, editor enablement and experimental hypotheses; they must **not** redefine address authority. A future mapping correction is made in a reviewed discovery manifest, synchronised into the canonical registry and verified against affected controls. In particular, the existing experimental Japan Story & event flag On/Off controls remain editable, including offset candidates. Registry confidence does not gate those explicit manual actions.

The machine-generated registry can list multiple masks for the same address, byte aliases within a word and conflicting research references. A complete word and one of its individual bits are distinct records. The `id_aliases` property preserves source-specific stable IDs where two named source declarations refer to the same field. The record `sources` lists the origin of reviewed mappings and every relevant textual mention. The catalogue carries no executable code, RDRAM writer handles or permission grants.

## Source manifests

The reviewed toolkit discovery manifest is `practice/data/address_discoveries_v1.json` with `format: "goemon-address-discoveries-v1"`. Decomp agents publish the same format to `decomp/address_discoveries_v1.json` on their **separate** `chatgptweb/decomp` baseline. Both source paths are version-controlled JSON.

Each address entry provides, to the degree established, stable `id`, `name`, `region`, `revision`, `address`, `category`, `data_type`, `width`, `signed`, `endian`, `mask`, `counterpart`, `confidence`, `evidence`, `source`, `context`, `mips_refs`, `live_readable`, `control`, `owner`, `discovered`, `updated` and `source_revision`. Unknown metadata must be `null`, not guessed.

An abbreviated record:

```json
{
  "id": "decomp:vm_text_stream_cursor",
  "name": "Script text-stream cursor",
  "region": "usa",
  "revision": "NG5E-0",
  "address": "0x801C77E8",
  "category": "script_vm",
  "data_type": "u32",
  "width": 4,
  "signed": false,
  "endian": "big",
  "mask": null,
  "counterpart": null,
  "confidence": "research_observed",
  "evidence": "Original VM instruction sequence; text-token pointer, not VM PC",
  "source": "decomp/VM_RUNTIME_CURSOR_FIELD_REPORT.md",
  "context": "Active text command; never dereference without pointer validation",
  "mips_refs": ["func_8003DBEC"],
  "live_readable": true,
  "control": null,
  "owner": "script VM",
  "discovered": "2026-11-13",
  "updated": "2026-11-17",
  "source_revision": "decomp commit SHA"
}
```

The address is a **guest RDRAM location**, not a ROM offset, guest instruction target, GameShark command word, or emulator host pointer. A location whose category is code, ROM, overlay patch or external cheat remains **reference-only**. A typed pointer may be read as an unsigned scalar, but its stored target cannot automatically be dereferenced. Dynamic/scene-dependent fields require a valid original scene and object lifetime. Never derive Japanese variants of VM state, dynamic objects or code VMAs from the `0x57F0` offset; preserve the known Miracle Snowflake `0x57F1` exception.

## Import and integrity checks

From a repository checkout with Python 3.12+:

```bash
python3 -m scripts.sync_address_catalogue --write
python3 -m scripts.sync_address_catalogue --check
python3 -m unittest tests.test_address_registry -v
```

`--write` updates the canonical JSON and `practice/data/address_catalogue_audit.json`, adding recorded discoveries and aliases without overwriting independently reviewed legacy identities. `--check` fails when a new entry is missing or source declarations conflict with canonical addresses/types/masks. This is run by toolkit CI. Do not edit the generated JSON manually to hide a discrepancy: correct the discovery manifest and review provenance. Earlier source modules remain reconciliation inputs, **not** fallback authority for the runtime.

The registry builder imports existing structured sources, including `inspector.py`, `unlocks.py`, `story_progress.py`, `region_memory_crosswalk.py`, Japanese field and scene probes, native debug fields, the 25 external leads and decomp/VM/Ebisumaru research manifests. It also indexes guest-looking literals in audited toolkit modules and 115 distinct research-document address references as **unclassified research references** when no safe decoder or lifetime is known. A newly encountered source address cannot silently disappear because it lacks a bespoke live-watch implementation; unclassified references stay visible but read-disabled.

For new discoveries, the same agent task must (1) record the exact finding and provenance in the manifest, (2) run `--write`, (3) run `--check`, and (4) add tests when introducing new semantics or offset exceptions. Do not treat a successful data import as independent validation.

## Cross-branch metadata update

`.github/workflows/address-catalogue-decomp-sync.yml` periodically fetches only `decomp/address_discoveries_v1.json` from `chatgptweb/decomp`, never the decomp source tree. It validates the imported JSON, preserves conflicting revisions as `disputed` records, writes only the three address metadata/audit files to a new `toolkit/address-metadata-sync-*` branch, runs tests and opens a **reviewable PR targeting main** where permitted by repository token settings. If an earlier sync PR is open, it avoids duplicate PRs. It never merges PRs automatically.

A separate agent can import a downloaded/staged decomp manifest manually:

```bash
python3 -m scripts.import_decomp_address_manifest \
  --upstream /path/to/decomp-addresses.json \
  --revision <decomp-commit-sha>
python3 -m scripts.sync_address_catalogue --write
```

The `<decomp-commit-sha>` is a literal CLI placeholder, not an XML tag. Importing two descriptions of the same byte does not confer extra confidence. A conflicting address is retained as a disputed lead; editing the existing mapping requires review.

## In-app catalogue and live values

Open **Live memory → Address catalogue** from either game version. It loads the bundled registry offline, even before a game connects. Filter by address, partial hex, name, category, region, decode type, confidence, source or flag ID. Sort columns, inspect all metadata and overlaps, copy the address/mask, add a supported type to the ordinary Live watches, or open the existing Unlocks editor. All existing Live memory, Story Progress and Unlocks layouts remain available. Only selected entries are read, and reads run off Tk's main thread via the verified current-region guest memory adapter. JavaScript/ROM/overlay and unknown-width entries are never blindly polled or written.

**Refresh Address Catalogue** retrieves only the versioned discovery JSON at the fixed canonical GitHub URL, with size and schema limits, no arbitrary redirects, no code execution and no write authorisation. A successful refresh is cached under the per-user toolkit data folder; corrupted, missing or offline updates leave the bundled registry available. An upstream discovery can appear in catalogue search without a toolkit code release when its decoder type is already supported. This refresh is *descriptive only*: it cannot modify the addresses used by existing writes, enable new editors, or silently promote unverified candidates.

## Audits and limitations

`practice/data/address_catalogue_audit.json` reports counts by region/category/confidence, record count, distinct regional address locations, live-readable entries, unsupported research records and disputed entries. This **counts field records, not unique memory locations**: several bits at one address have separate IDs.

Synthetic big-endian reads and Tk/Windows test coverage are not a substitute for live USA and Japanese emulator/gameplay verification. The current catalogue intentionally does not dereference dynamic pointers or auto-write proposed addresses. Old cheat instruction patches and code VMAs remain visible as research leads, not game state variables.
