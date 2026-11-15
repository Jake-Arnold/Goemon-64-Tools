# USA / Japan unlock address mapping — research-enabled

The same **34-row Unlocks tab** is used by both ROMs. The original USA guest addresses, options and write logic remain unchanged. Japanese guest addresses are drawn from the published [Japan (NG5J) GameShark codes](https://gamehacking.org/game/20438), prior source-named mappings, or **explicitly labelled hypotheses**. The Japan reference ROM matches the NG5J release documented by the code database.

## What is known versus guessed

- **9 named:** directly named Japanese cheat entries and existing project correspondences. User has live-confirmed Sasuke, Yae, Triton Shell, Cucumber and the three fish counts; Super Pass/Lord's Pass and Benkei weakness/Achilles' Heel are named cheat matches, not confirmed from a new live write.
- **16 array inferred:** Japanese GameShark **`50000404`** codes prove four contiguous, four-byte-spaced arrays for upgrades, super weapons, subweapons and jutsu. Individual item labels use USA ordering and consistently matching address displacement **`+0x57F0`**. These labels are still hypotheses.
- **4 offset inferred:** Goemon/Ebisumaru party, Gold Key and Silver Fortune Doll progress have plausible byte addresses at USA address `+0x57F0`; no individually named Japanese code proves them.
- **5 guesses:** Sasuke battery event bit and four individual Miracle Treasure names. The Japanese treasure array exists, but the individual English item order has not been established. Japanese Snowflake is assigned slot 4 (`0x80162057`), rather than extrapolating from USA's unusual `0x8015C866` address.

**All 34 entries can be edited individually for live research.** The normal Japanese **Unlock All includes 29** named/array/offset candidates and **excludes the five most speculative** (they remain individually writable). No confirmation dialog or ROM recompile is needed for Python toolkit edits. `--read-only` still blocks writes.

| USA unlock row | Group | USA guest address | Japan guest address | Japanese mapping confidence |
| --- | --- | --- | --- | --- |
| Goemon in party | Party | `0x8015C69F` | `0x80161E8F` | Regional-offset candidate |
| Ebisumaru in party | Party | `0x8015C6A3` | `0x80161E93` | Regional-offset candidate |
| Sasuke in party | Party | `0x8015C6A7` | `0x80161E97` | Named source |
| Yae in party | Party | `0x8015C6AB` | `0x80161E9B` | Named source |
| Goemon pipe upgrade | Weapon upgrades | `0x8015C6AF` | `0x80161E9F` | Array-based inference |
| Ebisumaru hammer upgrade | Weapon upgrades | `0x8015C6B3` | `0x80161EA3` | Array-based inference |
| Sasuke kunai upgrade | Weapon upgrades | `0x8015C6B7` | `0x80161EA7` | Array-based inference |
| Yae katana upgrade | Weapon upgrades | `0x8015C6BB` | `0x80161EAB` | Array-based inference |
| Chain Pipe | Weapons | `0x8015C6BF` | `0x80161EAF` | Array-based inference (JP On = 01) |
| Meat Saw Hammer | Weapons | `0x8015C6C3` | `0x80161EB3` | Array-based inference |
| Fire Cracker Bomb | Weapons | `0x8015C6C7` | `0x80161EB7` | Array-based inference |
| Flute | Weapons | `0x8015C6CB` | `0x80161EBB` | Array-based inference |
| Windup Camera | Weapons | `0x8015C6D3` | `0x80161EC3` | Array-based inference |
| Ice Kunai | Weapons | `0x8015C6D7` | `0x80161EC7` | Array-based inference |
| Bazooka | Weapons | `0x8015C6DB` | `0x80161ECB` | Array-based inference (subweapon slot 3) |
| Medal of Flames | Abilities | `0x8015C6DF` | `0x80161ECF` | Array-based inference |
| Sudden Impact | Abilities | `0x8015C6EF` | `0x80161EDF` | Array-based inference |
| Mini Ebisumaru | Abilities | `0x8015C6F3` | `0x80161EE3` | Array-based inference |
| Super Jump | Abilities | `0x8015C6F7` | `0x80161EE7` | Array-based inference |
| Magic Mermaid | Abilities | `0x8015C6FB` | `0x80161EEB` | Array-based inference |
| Triton Shell | Items and keys | `0x8015C6FF` | `0x80161EEF` | Named source |
| Gold Key | Items and keys | `0x8015C713` | `0x80161F03` | Regional-offset candidate |
| Cucumber | Items and keys | `0x8015C717` | `0x80161F07` | Named source |
| Lord's Pass | Items and keys | `0x8015C703` | `0x80161EF3` | Named source |
| Silver Fortune Doll progress | Items and keys | `0x8015C707` | `0x80161EF7` | Regional-offset candidate |
| Sasuke battery 1 collected | Items and keys | `0x8015C609` | `0x80161DF9` | Experimental guess |
| Achilles' Heel | Items and keys | `0x8015C70F` | `0x80161EFF` | Named source |
| Red fish count | Fish counts | `0x8015C71B` | `0x80161F0B` | Named source |
| Blue fish count | Fish counts | `0x8015C723` | `0x80161F13` | Named source |
| Yellow fish count | Fish counts | `0x8015C71F` | `0x80161F0F` | Named source |
| Star | Miracle items | `0x8015C85B` | `0x8016204B` | Experimental guess |
| Moon | Miracle items | `0x8015C85F` | `0x8016204F` | Experimental guess |
| Flower | Miracle items | `0x8015C863` | `0x80162053` | Experimental guess |
| Snowflake | Miracle items | `0x8015C866` | `0x80162057` | Experimental guess |

## Region-specific write encodings

**Chain Pipe:** USA `On = 0x02`, Japan super-weapon `On = 0x01`. The UI changes its displayed On code when switching regions; the unchanged USA `Unlock.values = (0, 2)` is translated for Japan before writing. Bulk unlock also writes Japan `01`. Weapon upgrades remain `00/01/02`; regular acquisitions are `00/01`. Fish counts retain the established `8/5/3` maxima.

**Battery 1:** Japanese event byte `0x80161DF9` and bit `0x20` are **both guesses inferred from the USA address**. The bitwise writer preserves other bits. This candidate must not be treated as confirmed.

**Miracle treasures:** Japanese repeat cheat `50000404 0000 / 8016204B 0001` sets four slots at `0x8016204B`, `0x8016204F`, `0x80162053`, `0x80162057`. The Star/Moon/Flower/Snowflake association above is guessed in slot order and can be corrected independently.

**Bazooka:** Candidate `0x80161ECB` (Japanese subweapon slot 3), **not `0x80161ECF`**, which is assigned to Medal of Flames (subweapon slot 4). Source-backed array addresses are independently published, but individual identity requires gameplay verification. The earlier Bazooka pickup observation at `0x80161DBE` / `0x80161DBF` is an event-bit delta, not a proven weapon slot (see [pickup trace](JAPAN_BAZOOKA_PICKUP_TRACE.md)).

## Rapid in-game validation sequence

Use a disposable emulator savestate. Toggle one inferred row at a time, inspect the game inventory/ability screen, change rooms if the UI caches item state, and restore the savestate. Start with **Bazooka**, **Medal of Flames**, **Chain Pipe**, Gold Key and the weapon upgrade rows. For treasures, collect exactly one and compare the four JP slots. If an inferred row maps to a different item, change just that row's key in `practice/region_unlocks.py`; USA mappings never need to change.

Sources: [Japan GameHacking NG5J](https://gamehacking.org/game/20438), [Japanese weapons guide](https://w.atwiki.jp/match6974/pages/24.html), [USA project unlock definitions](../practice/unlocks.py).
