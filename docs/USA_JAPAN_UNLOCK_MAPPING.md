# USA / Japan unlock address mapping

The shared **Unlocks** tab retains these 34 original USA entries and controls in both game versions. An exact Japanese address is shown only when supported by an explicitly named Japanese source. Otherwise the visible Japanese address is **`unknown`**; there is no USA-address fallback or arithmetic offset.

All **nine mapped Japanese rows are directly writable by default**: Sasuke/Yae On and Off, Triton Shell, Lord's Pass (JP Super Pass), Achilles' Heel (JP Benkei's weakness) and Cucumber On and Off, plus all three fish counts. No confirmation dialog or party-state guard is used. A short-lived writable emulator handle performs a one-byte update and readback; ROM/RDRAM identification still happens when connecting. `--read-only` disables edits. Japanese Unlock All updates only those nine rows, skipping the 25 unknown ones.

| Original unlock | Group | USA N64 guest address | Japan-0 N64 guest address | Japan control |
| --- | --- | --- | --- | --- |
| Goemon in party | Party | `0x8015C69F` | `unknown` | unknown — not writable |
| Ebisumaru in party | Party | `0x8015C6A3` | `unknown` | unknown — not writable |
| Sasuke in party | Party | `0x8015C6A7` | `0x80161E97` | Direct On/Off |
| Yae in party | Party | `0x8015C6AB` | `0x80161E9B` | Direct On/Off |
| Goemon pipe upgrade | Weapon upgrades | `0x8015C6AF` | `unknown` | unknown — not writable |
| Ebisumaru hammer upgrade | Weapon upgrades | `0x8015C6B3` | `unknown` | unknown — not writable |
| Sasuke kunai upgrade | Weapon upgrades | `0x8015C6B7` | `unknown` | unknown — not writable |
| Yae katana upgrade | Weapon upgrades | `0x8015C6BB` | `unknown` | unknown — not writable |
| Chain Pipe | Weapons | `0x8015C6BF` | `unknown` | unknown — not writable |
| Meat Saw Hammer | Weapons | `0x8015C6C3` | `unknown` | unknown — not writable |
| Fire Cracker Bomb | Weapons | `0x8015C6C7` | `unknown` | unknown — not writable |
| Flute | Weapons | `0x8015C6CB` | `unknown` | unknown — not writable |
| Windup Camera | Weapons | `0x8015C6D3` | `unknown` | unknown — not writable |
| Ice Kunai | Weapons | `0x8015C6D7` | `unknown` | unknown — not writable |
| Bazooka | Weapons | `0x8015C6DB` | `unknown` | unknown — not writable |
| Medal of Flames | Abilities | `0x8015C6DF` | `unknown` | unknown — not writable |
| Sudden Impact | Abilities | `0x8015C6EF` | `unknown` | unknown — not writable |
| Mini Ebisumaru | Abilities | `0x8015C6F3` | `unknown` | unknown — not writable |
| Super Jump | Abilities | `0x8015C6F7` | `unknown` | unknown — not writable |
| Magic Mermaid | Abilities | `0x8015C6FB` | `unknown` | unknown — not writable |
| Triton Shell | Items and keys | `0x8015C6FF` | `0x80161EEF` | Direct On/Off |
| Gold Key | Items and keys | `0x8015C713` | `unknown` | unknown — not writable |
| Cucumber | Items and keys | `0x8015C717` | `0x80161F07` | Direct On/Off |
| Lord's Pass | Items and keys | `0x8015C703` | `0x80161EF3` | Direct On/Off (JP Super Pass) |
| Silver Fortune Doll progress | Items and keys | `0x8015C707` | `unknown` | unknown — not writable |
| Sasuke battery 1 collected | Items and keys | `0x8015C609` | `unknown` | unknown — not writable |
| Achilles' Heel | Items and keys | `0x8015C70F` | `0x80161EFF` | Direct On/Off (JP Benkei weakness) |
| Red fish count | Fish counts | `0x8015C71B` | `0x80161F0B` | Direct hex count |
| Blue fish count | Fish counts | `0x8015C723` | `0x80161F13` | Direct hex count |
| Yellow fish count | Fish counts | `0x8015C71F` | `0x80161F0F` | Direct hex count |
| Star | Miracle items | `0x8015C85B` | `unknown` | unknown — not writable |
| Moon | Miracle items | `0x8015C85F` | `unknown` | unknown — not writable |
| Flower | Miracle items | `0x8015C863` | `unknown` | unknown — not writable |
| Snowflake | Miracle items | `0x8015C866` | `unknown` | unknown — not writable |

Note: Entries with `unknown` Japanese addresses display no read value and have disabled write controls. The original USA mappings and behaviours are unchanged. Known Japanese rows use single-byte direct writes without dialog prompts. Anonymous Japanese GameShark repeat slots are not assigned to named weapon upgrades without independent evidence.

The user identified **Super Pass** (`0x80161EF3`) as the Japanese counterpart of USA **Lord's Pass**, and **Benkei's weakness** (`0x80161EFF`) as USA **Achilles' Heel**. These two source-backed Japanese addresses are mapped above. Other Japanese-only candidate fields such as world-map access (`0x80162063`) still have **USA: `unknown`**.
