# Goemon 64 — dialogue-adjacent item grants, event coupling and glitch-candidate survey

**20 November 2026. Region scope:** Japanese rev-0 (`Ganbare Goemon: Neo Momoyama Bakufu no Odori`) and USA (`Mystical Ninja Starring Goemon`).  
**Evidence tier:** `STATIC_ROM_VERIFIED / RESEARCH_ONLY`. This is script-data and original-MIPS analysis; it is **not** a live demonstration of any new glitch.  
**Canonical context:** `chatgptweb/decomp`; supersedes no original matching-C counts or runtime achievements.

## Why this is valuable

The already identified Gourmet Sub Bomb Text Skip candidate is a save-data assignment immediately following a text opcode. A complete scan of *all* 1,311 resource records in each SHA-1-authenticated 32 MiB expanded original ROM finds **45** 4-word immediate assignments to the 0x304-byte live saved-data structure directly after an `0x8010` text opcode and segment-8 text operand. They affect **42 distinct saved-data offsets**. All 45 have cross-region matches preserving the resource ID, saved-data offset, assigned value and preceding text-pointer segment. The region-specific command offsets are different.

**45 is a structural census, not a count of exploitable text skips.** Interpreter branching, cutscene state, callback side effects and actual Start handling determine reachability and cancellation. Native or indirect writers may exist outside the scanned pattern.

Twenty assignments occur in resource 93, largely item-acquisition and area-title sequences. The other 25 occur in resources 95, 96, 97, 98, 101, 102 and 106. The full resource distribution is `93:20, 95:1, 96:2, 97:9, 98:3, 101:2, 102:7, 106:1` in *both* regions.

## Confirmed 21 named grant fields (23 immediate assignment sites)

Item names originate in the separately identified, third-party Game Tools Collection save-editor mapping, not in C variable names. Original ROM assignment operands are independently checked in both versions, and original English dialogue near multiple commands explicitly names the corresponding received item, including Chain Pipe, Mermaid, Miracle Snow, Achilles' Heel and Miracle Star. Exact external labels should not be treated as proof of every native item consumer.

| Saved field relative to JP `0x80161DF8` / US `0x8015C608` | External item/ability label | JP file + offset(s) | USA file + offset(s) | Number of direct immediate setters |
|---|---|---|---|---:|
| `+0x0B4` | Chain Pipe | 102 `+0x405C` | 102 `+0x6670` | 1 |
| `+0x0B8` | Meat Saw-Hammer | 93 `+0x31D4` | 93 `+0x3CF0` | 1 |
| `+0x0BC` | Firecracker Bomb | 102 `+0x579C` | 102 `+0x7E10` | 1 |
| `+0x0C0` | Koryuta's Flute | 102 `+0x4F98` | 102 `+0x75EC` | 1 |
| `+0x0C8` | Windup Camera | 93 `+0x2E40` | 93 `+0x394C` | 1 |
| `+0x0CC` | Kunai of Severe Cold | 93 `+0x2F9C` | 93 `+0x3AA8` | 1 |
| `+0x0D0` | Yae Bazooka | 93 `+0x30D8` | 93 `+0x3BEC` | 1 |
| `+0x0D4` | Flaming Medal | 93 `+0x2D14` | 93 `+0x3818` | 1 |
| `+0x0E4` | Sudden Impact | 98 `+0x1B20` | 98 `+0x2A54` | 1 |
| `+0x0E8` | Mini-Ebisu | 97 `+0x8EE4` | 97 `+0xCBC8` | 1 |
| `+0x0EC` | Flying | 98 `+0x2884` | 98 `+0x37C0` | 1 |
| `+0x0F0` | Mermaid | 98 `+0x224C` | 98 `+0x31C8` | 1 |
| `+0x0F4` | Triton Shell | 101 `+0x0F50`, `+0x0FCC` | 101 `+0x1904`, `+0x19A0` | 2 |
| `+0x104` | Achilles' Heel | 97 `+0x8980` | 97 `+0xC654` | 1 |
| `+0x108` | Key to Training | 97 `+0x70DC` | 97 `+0xADF0` | 1 |
| `+0x10C` | Quality Cucumber | 97 `+0x7DC0` | 97 `+0xBABC` | 1 |
| `+0x250` | Miracle Star | 93 `+0x22C4` | 93 `+0x2E00` | 1 |
| `+0x254` | Miracle Moon | 93 `+0x2184` | 93 `+0x2CC0` | 1 |
| `+0x258` | Miracle Flower | 93 `+0x2218` | 93 `+0x2D54` | 1 |
| `+0x25C` | Miracle Snow | 97 `+0x98D4` | 97 `+0xD5C0` | 1 |
| `+0x268` | Map of Japan | 102 `+0x5154`; 106 `+0x1A3C` | 102 `+0x77C0`; 106 `+0x2918` | 2 |

**New precision:** 19 of 21 mapped fields have one direct immediate scripted setter; Triton Shell and Map of Japan have two. This is a count of the exact four-word assignment pattern, **not evidence that no native or dynamically computed setters exist**.

## New: nine grants are immediately followed by saved-event flag setters

A second instruction-level script scan found **ten occurrences**, covering nine named grant fields, where the 16-byte immediate inventory write is followed immediately by an `0x8020` event-flag setter. This same order and flag number is present in both original ROMs.

| Grant field | Script event-flag ID set immediately afterwards | Direct-script sets / tests of that flag (JP and USA) |
|---|---:|---:|
| Key to Training `+0x108` | `0x27` | 1 / 2 |
| Quality Cucumber `+0x10C` | `0x0F` | 1 / 3 |
| Achilles' Heel `+0x104` | `0x29` | 1 / 3 |
| Mini-Ebisu `+0x0E8` | `0x31` | 1 / 3 |
| **Miracle Snow `+0x25C`** | **`0x35`** | **1 / 3** |
| Sudden Impact `+0x0E4` | `0x1C` | 1 / 2 |
| Mermaid `+0x0F0` | `0x1F` | 1 / 3 |
| Flying `+0x0EC` | `0x20` | 1 / 3 |
| Map of Japan `+0x268` (two occurrences) | `0x09` (both) | 2 / 2 |

The setter/tester counts are for resource-script `0x8020` and `0x8022` tokens, **not a complete native reference count**. None of these nine flag IDs has a direct script `0x8021` clear in the scanned resources.

**Why this matters:** Item ownership and story/event completion are represented by different saved-state fields. Their *directly adjacent assignments* suggest that a dialogue cancellation before the grant usually leaves **both** states unset. The Japanese VM dispatcher (`func_8003D2FC_3DEFC`) loops from a completed immediate assignment into the following flag command without returning to the input/update boundary. A one-frame input should not normally be able to divide these two consecutive opcode executions. This is an instruction-order inference, not a live guarantee about interrupt behaviour. For Miracle Snow, simply preventing the item-grant command is therefore **not evidence of a progression skip**; it would also prevent flag `0x35` from being set by that script block.

## More promising special case: Chain Pipe's earlier story flag

Japanese resource 102 `+0x3F44` (USA resource 102 `+0x6558`) sets **story/event flag `0x10`**, and the same scripted sequence later grants Chain Pipe at JP `+0x405C` (USA `+0x6670`). Between these two original positions there are text/callback/VM-field commands, but the four-byte-aligned scan finds no `0x8006` conditional, `0x8008` reset, `0x800A` jump, `0x8011` choice or `0x8022` test token. Native callbacks may still alter the VM cursor; reachability must be verified.

This is a **better candidate for creating an already-advanced event state without the associated inventory item** than the immediately coupled Miracle Snow/Mermaid grants: the event-bit write occurs *before* the later item assignment, with dialogue between them. The flag's broader gameplay meaning and whether any Start/B interruption can stop execution after the first write are unverified. Japan already has a separate, physical Chain Pipe Skip; this is an investigation into script state, not a claimed new skip.

Koryuta's Flute at JP resource 102 `+0x4F98` similarly has one direct immediate item setter but **no immediately following `0x8020`**. The pre- and post-grant script contains several dialogue and VM-local commands. This is a practical target for investigating the known one-frame Flute Skip at the code level, without asserting that the skip works by cancelling this grant.

## Two high-fanout flags set after dialogue

JP flag **`0x17`** is set once (resource 116 `+0x1074`), directly after dialogue discussing consulting a fortune teller, and is tested **36 times** in aligned script data. JP flag **`0x18`** is set once (resource 94 `+0x3C80`), directly after a Chugoku-region warning, and tested **30 times**. Corresponding USA setters occur at resource 116 `+0x156C` and resource 94 `+0x56BC`, and have the same test counts. Native tests and reachability remain unbounded.

These are **higher-leverage dialogue-skip candidates** than a flag tested only once, because changing their value might select multiple downstream scripts. It could also cause softlocks or simply change dialogue. No playable glitch is demonstrated.

## Practical research priorities

1. **Trace Start/B effects on the VM cursor and item writes**, starting with the known Bomb Text Skip and known Flute Skip. Use read/write logging; do not change retail ROMs or working saves.
2. **Chain Pipe split-state experiment:** monitor JP flag-`0x10` byte `0x80161DFA` mask `0x01`, JP item word `0x80161EAC`, and VM cursor `0x8007D288` from before the flag-set dialogue until after the item grant. Determine whether any ordinary interruption leaves the first set and second unset.
3. **Miracle Snow paired-state control:** JP item word `0x80162054`, event flag-`0x35` at `0x80161DFE` mask `0x20`, original resource 97 `+0x98D4/+0x98E4`. Confirm the consecutive instruction ordering and test whether they diverge under normal input.
4. **High-fanout story flags:** watch JP flags `0x17` and `0x18` across their setter dialogue and selected downstream conditionals. Capture the exact event/scene and flag consumer before claiming a skip.
5. Locate the *native* item-consumer functions for Chain Pipe, Flute, Mini-Ebisu, Mermaid and Miracle Snow and decompile their action-gating logic. The current script scan proves grant *writers*, not their downstream use.

## Verification, caveats and provenance

Reproduce with the independently verified original expanded 32 MiB ROMs:

```bash
python3 verify_goemon_dialogue_adjacent_grants.py JAPAN_EXPANDED.z64 USA_EXPANDED.z64
```

Checks: both exact ROM SHA-1s, original file-table ordering and bounded resource spans, 45 text-adjacent assignments / 42 fields per region, identical paired signatures, 21 named grant addresses and exact resource offsets, direct setter uniqueness, immediate event-flag pairs, event-bit set/test counts, and 0x17/0x18/0x32 counts. Source asset is provided separately in the user conversation, not bundled into GitHub with copyrighted binaries.

**Not checked:** instruction-level user input to abort in any of the 45 sites; full save-file persistence; live-run/test ROM differences; use of grants through native readers; dynamic writer aliases; successful new route or speedrun time savings. The original Japanese and USA ROMs were *read*, never modified.
