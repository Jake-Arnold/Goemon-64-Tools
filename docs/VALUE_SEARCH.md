# Read-only Value Search — US Goemon N64 toolkit

The **Value search** tab scans the original game's **8 MiB RDRAM** using the validated native/Linux or Windows memory connection. It never writes game memory and does not require a normal player object or character ID. During Impact boss battles and the title screen, the ordinary player object may be absent or invalid; scanning global RAM remains possible if the game-memory connection itself is valid.

## Finding a displayed number (oil, Ryo, timer)

1. Connect the toolkit and open **Value search**.
2. Select a numeric representation: unsigned/signed 8-, 16-, 32-bit integer or 32-bit float. For a displayed integer, begin with **u16**, then try **u32**.
3. Enter the visible value and click **New exact scan**.
4. Change that value through normal gameplay.
5. Choose **Exact** with the new number, or **Decreased / Increased**, then click **Filter surviving results**.
6. Repeat to reduce false matches. Select a surviving address and click **Watch selected address** to copy it into Live Memory's persistent custom watches.

The first search tests naturally aligned addresses. Select **Include unaligned addresses** and start a fresh scan if no plausible match is found. This increases scan time and spurious matches. Float exact values compare their IEEE-754 byte representation.

## Finding an undisplayed boss HP value

1. Begin a **New unknown initial value** search at the beginning of a boss phase.
2. Land a single confirmed hit. Filter **Decreased**.
3. Allow the game to continue without hitting the boss. Filter **Unchanged**.
4. Land another hit and filter **Decreased** again.
5. Test a different damaging action and observe candidate changes. Repeat on a fresh fight to distinguish health from counters and scripted phase variables.

**Changed** and **Unchanged** compare raw bytes; **Increased** and **Decreased** compare numeric interpretations. Each filter compares against the previous *capture*, not the original initial scan.

## Operational and safety notes

- Each scan reads RDRAM in **64 KiB chunks** using ram.read_guest() in canonical N64 big-endian order, then processes data in a background thread so the Tk UI stays responsive.
- A value's physical location may move between boss phases, maps, or game sessions; do not treat surviving addresses as universal or proven field mappings.
- Scans are not instruction-atomic: game values can change during the read, causing false positives or negatives.
- Each session holds an 8 MiB previous snapshot plus a bounded candidate bytearray and temporary snapshot. Candidate lists do not need millions of Python objects.
- Only the first **200** candidate addresses are shown. Narrow results rather than expecting a complete multi-million-row display.
- **Refresh visible values** reads only the visible candidate addresses without applying a filter; **Auto-refresh visible values** does this while the tab is selected. Neither action changes the stored comparison baseline.
- Searches are kept in memory and are not exported as raw RAM dumps. Custom watches save only an address, type and label, and can be removed from Live Memory.
- Exact initial scans for common values such as zero may be slow; unknown-value scans include millions of eligible positions until filtered.
- Unreadable or partial memory snapshots cause an error without accepting incomplete data. Changing the game connection requires a fresh search.
- This tool intentionally has no write/freeze control. Existing player-dependent checkpoint and write protections remain unchanged.

## Verification

Synthetic model tests: python3 -m unittest tests.test_value_search -v.

Tk smoke tests: xvfb-run -a python3 -m unittest tests.test_value_search_ui -v.

These tests exercise a fake read-only RDRAM reader and a Tk harness, including invalid normal-player pointer scenarios. They do **not** establish that a particular Impact resource value, oil variable, Ryo field or boss HP address has been found in live gameplay.
