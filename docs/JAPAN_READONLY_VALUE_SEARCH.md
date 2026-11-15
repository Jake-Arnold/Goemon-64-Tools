# Japan-0 read-only Value Search + custom watches

Implemented on `chatgptweb/japan-controlled-party-writes` as the first incremental USA→Japan parity milestone, November 15, 2026.

## Scope and safety

The **existing Value search tab** is enabled for the verified Japanese Mupen64Plus session. It uses `jp_rdram` rather than the USA `mem` pointer, and scans the canonical 8 MiB N64 guest address range `0x80000000`–`0x807FFFFF` in chunks via `read_guest()`. Supported types are u8/s8/u16/s16/u32/s32/f32; filters are Exact, Increased, Decreased, Changed and Unchanged. The scanner already runs in a worker, without depending on the USA player/task pointer. The UI never calls a guest-RAM writer in Value Search.

The **Japan Live / Party Test tab** now has a Japan-only read-only custom-watch editor. Add a name, exact guest address and numeric/hex type, then inspect decoded/hex values, baseline changes and copied change reports. The existing `practice.custom_watches` decoder and schema provide address/width checks and a 128-watch bound. Each new field is explicitly a **user candidate**, not a verified game-variable mapping.

The Japanese watch file is **`practice/japan_0_custom_watches.json`** for unfrozen local checkouts, or the application's configured data directory for frozen builds; the USA's separate `custom_watches.json` is never imported, rewritten or inferred safe for Japan. Value Search's **Watch selected address** adds the selected result only to this Japanese profile and switches to Japan Live.

A change of version, process or RDRAM, as well as a toolkit-requested emulator savestate load, invalidates scan results and Japanese field baselines. A scan worker's stale response is rejected by connection identity. The custom-watch definitions persist, but their observed values never persist as verified meanings.

Japanese party unlocks remain **the only Japanese memory writes**, behind their prior explicit opt-in and per-action confirmation. The new Value Search and watch controls are read-only even when party writes are opted in; the USA editor and freeze/checkpoint writers remain inaccessible.

## Validation reported by user

The user reported on 2026-11-15 that the preceding `./scripts/test_japan_party.sh` suite passed and both Sasuke/Yae **toolkit unlock buttons worked in a real emulator**. This confirms the prior party-write implementation's immediate use, not the two new parity controls or the characters' on-switch index values. No evidence yet confirms native Sasuke=2 / Yae=3 by observing `0x80161DCC` after real C-Down.

The new read-only parity tests were **authored on GitHub and not executed through the connector**. The script now includes `tests.test_japan_readonly_parity` in its Xvfb GUI phase, and existing Japanese UI tests use isolated temporary watch directories.

## Reproduce on Ubuntu

```bash
cd ~/Desktop/goemon-japan-mupen-test
git fetch origin chatgptweb/japan-controlled-party-writes
git switch --detach FETCH_HEAD
./scripts/test_japan_party.sh
python3 -m practice.toolkit --game-version japan --enable-japan-party-writes
```

1. Verify the **exact Japan-0 retail ROM**, select **mupen64plus**, attach to the existing emulator PID and verified RDRAM.
2. Open **Value search**. Select `u16`, enter the currently observed Ryo amount (from Japanese Live), click **New exact scan**. The published Japanese Ryo field `0x80161DDA` is a useful candidate to cross-check, but may not be unique and might change while scanning.
3. Change Ryo naturally, choose Increased or Decreased and **Filter surviving results**. Verify whether `0x80161DDA` survives. Do not infer that all other matches are Ryo.
4. Select the row and click **Watch selected address**. Confirm the **Japan Live / Party Test** tab opens and shows a new watch under **Custom JP watches**, using only the Japanese watch file.
5. Create a baseline, change the value, select Compare, and confirm both sourced and custom values show raw changes. Select the custom row, Remove selected, confirm sourced built-in fields remain intact.
6. Disconnect/reconnect, change region, and request savestate load. Verify stale Value Search results vanish and Japan watch values are cleared without removing saved definitions. Confirm USA-specific tabs and write actions remain unavailable in Japan mode.
7. Switch to USA to confirm its previous custom watches and Value Search behaviour remain unchanged.

**Performance:** All 8 MiB are scanned; an initial unknown-value scan can have millions of candidates and may be slow. The worker keeps Tk responsive and shows only the first 200 candidates. Avoid starting a scan during an unstable scene transition if a consistent value is required. A result is always an address *candidate*, not automatically a game symbol.

## Advanced RAM Comparison — Japanese A/B/C parity, first implementation

After selecting Japan, open **Event sessions → Advanced RAM comparison**. The USA **Event flag sessions** subtab is disabled until its Japan event-bank equivalent has been independently mapped. The existing advanced tab now displays Japan-specific experiments and uses `practice/japan_state_comparison.py` rather than USA memory fields.

- **Focused:** 4 KiB near the Japanese engine globals (`0x800CD000`) plus 4 KiB near candidate Japanese saved-game/inventory bytes (`0x80161C00`). These are *research ranges*, not verified Japanese save banks.
- **Wide:** all 8 MiB of independently verified Japanese N64 RDRAM, read in 64 KiB canonical guest-byte chunks. No player pointer is required.
- **Capture A**, perform one reversible in-game change, **Capture B**, optionally revert and **Capture C**, then **Compare**. Each capture runs in a worker; complete one before requesting another. With C present, only bytes exactly restored to the original A value survive the comparison.
- Candidate ranking is bounded to the 1,200 most relevant raw-byte changes, even if much more memory changes; total counts are preserved. No changed byte automatically gets a name or write permission.
- **Watch selected address** adds a one-byte Japanese custom watch (or f32 for recognised USA-only float output); it never invokes a USA editor. **Export comparison JSON** saves a `japan_state_probe_*.json` evidence report without embedding full RAM contents.
- All three captures must match Japanese region, PID, emulator RAM base, byte order, reader session and scope. Disconnect, region change and toolkit-requested savestate load invalidate capture caches.

**Useful first live A/B/C experiment:** select `Scene transition`, choose `focused`, capture A in Oedo, enter a nearby doorway normally, capture B after loading completes, then Compare. Independently observed current scene `0x800CD2A2`, previous `0x800CD2AC` and pending `0x800CD490` should provide checkable changes. This tests the UI without any stage or actor write. Repeat on the opposite doorway direction and separately test C-Down character swaps.

The associated synthetic backend and Tk tests are `tests.test_japan_state_comparison` and `tests.test_japan_state_comparison_ui`. They are included in `./scripts/test_japan_party.sh`, alongside the original USA Value Search and Advanced RAM Comparison regressions. **The new tests were authored but not executed in the connector environment.**

**Next:** verify Japanese Value Search/Custom Watches and A/B/C live on Linux Mupen64Plus, then map Japanese player/task pointers, true XYZ/action state and event-bank layouts. USA Mupen RDRAM attachment remains a separate improvement target.
