# USA / Japan unlock address mapping

The shared **Unlocks** tab retains these 34 original USA entries and controls in both game versions. An exact Japanese address is shown only when supported by an explicitly named Japanese source. Otherwise the visible Japanese address is **`unknown`**; there is no USA-address fallback or arithmetic offset.

Only Sasuke and Yae **On** have an independently tested Japanese toolkit write path (one byte `00→01` with ROM/PID/process validation). Other Japanese addresses listed here are read leads, not write permissions. Japanese bulk unlock is disabled.

| Original unlock | Group | USA N64 guest address | Japan-0 N64 guest address | Japan control |
| --- | --- | --- | --- | --- |
| Goemon in party | Party | `0x8015C69F` | `unknown` | Read-only |
| Ebisumaru in party | Party | `0x8015C6A3` | `unknown` | Read-only |
| Sasuke in party | Party | `0x8015C6A7` | `0x80161E97` | On only (guarded) |
| Yae in party | Party | `0x8015C6AB` | `0x80161E9B` | On only (guarded) |
| Goemon pipe upgrade | Weapon upgrades | `0x8015C6AF` | `unknown` | Read-only |
| Ebisumaru hammer upgrade | Weapon upgrades | `0x8015C6B3` | `unknown` | Read-only |
| Sasuke kunai upgrade | Weapon upgrades | `0x8015C6B7` | `unknown` | Read-only |
| Yae katana upgrade | Weapon upgrades | `0x8015C6BB` | `unknown` | Read-only |
| Chain Pipe | Weapons | `0x8015C6BF` | `unknown` | Read-only |
| Meat Saw Hammer | Weapons | `0x8015C6C3` | `unknown` | Read-only |
| Fire Cracker Bomb | Weapons | `0x8015C6C7` | `unknown` | Read-only |
| Flute | Weapons | `0x8015C6CB` | `unknown` | Read-only |
| Windup Camera | Weapons | `0x8015C6D3` | `unknown` | Read-only |
| Ice Kunai | Weapons | `0x8015C6D7` | `unknown` | Read-only |
| Bazooka | Weapons | `0x8015C6DB` | `unknown` | Read-only |
| Medal of Flames | Abilities | `0x8015C6DF` | `unknown` | Read-only |
| Sudden Impact | Abilities | `0x8015C6EF` | `unknown` | Read-only |
| Mini Ebisumaru | Abilities | `0x8015C6F3` | `unknown` | Read-only |
| Super Jump | Abilities | `0x8015C6F7` | `unknown` | Read-only |
| Magic Mermaid | Abilities | `0x8015C6FB` | `unknown` | Read-only |
| Triton Shell | Items and keys | `0x8015C6FF` | `0x80161EEF` | Read-only |
| Gold Key | Items and keys | `0x8015C713` | `unknown` | Read-only |
| Cucumber | Items and keys | `0x8015C717` | `0x80161F07` | Read-only |
| Lord's Pass | Items and keys | `0x8015C703` | `unknown` | Read-only |
| Silver Fortune Doll progress | Items and keys | `0x8015C707` | `unknown` | Read-only |
| Sasuke battery 1 collected | Items and keys | `0x8015C609` | `unknown` | Read-only |
| Achilles' Heel | Items and keys | `0x8015C70F` | `unknown` | Read-only |
| Red fish count | Fish counts | `0x8015C71B` | `0x80161F0B` | Read-only |
| Blue fish count | Fish counts | `0x8015C723` | `0x80161F13` | Read-only |
| Yellow fish count | Fish counts | `0x8015C71F` | `0x80161F0F` | Read-only |
| Star | Miracle items | `0x8015C85B` | `unknown` | Read-only |
| Moon | Miracle items | `0x8015C85F` | `unknown` | Read-only |
| Flower | Miracle items | `0x8015C863` | `unknown` | Read-only |
| Snowflake | Miracle items | `0x8015C866` | `unknown` | Read-only |

Note: Entries with `unknown` Japanese addresses display no read value and have disabled write controls. The original USA mappings and behaviours are unchanged. Anonymous Japanese GameShark repeat slots are not assigned to named weapon upgrades without independent evidence.

Japanese-only candidate fields such as Super Pass (`0x80161EF3`), Benkei's weakness (`0x80161EFF`), and world-map access (`0x80162063`) have no confirmed equivalent in this USA Unlocks catalogue (**USA: `unknown`**). They remain visible through Japanese diagnostic/story research views; they are not silently assigned to unrelated USA items.
