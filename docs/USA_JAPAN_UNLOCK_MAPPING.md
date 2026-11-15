# USA / Japan unlock mapping — 33/34 user-confirmed

The original 34 USA Unlocks rows, addresses, values and controls remain unchanged. The Japanese NG5J sources and historical address-inference provenance are retained for research. **Live verification is a separate fact:** on 15 November 2026 the user reported that every Japanese unlock worked in Project64, including the four individual Miracle items, all weapon upgrades, all weapons, all abilities, Gold Key, and Silver Fortune Doll progress. **Only Sasuke battery 1 remains unverified.** This is a user gameplay report, not an assistant-operated emulator test.

The published [Japanese GameShark codes](https://gamehacking.org/game/20438) support the four-slot arrays; previous hypotheses remain identified in the *original source provenance* column. Values in the *live gameplay report* column supersede older speculative labels for confirmed row identities.

Default Japanese **Unlock All now writes 33 user-confirmed rows**. The battery candidate remains individually editable for research but is excluded from bulk writes. `--read-only` continues to disable editing.

| USA unlock row | Group | USA guest address | Japan guest address | Original source provenance | Live gameplay report |
| --- | --- | --- | --- | --- | --- |
| Goemon in party | Party | `0x8015C69F` | `0x80161E8F` | Regional-offset candidate | User-confirmed (15 Nov 2026) |
| Ebisumaru in party | Party | `0x8015C6A3` | `0x80161E93` | Regional-offset candidate | User-confirmed (15 Nov 2026) |
| Sasuke in party | Party | `0x8015C6A7` | `0x80161E97` | Named source | User-confirmed (15 Nov 2026) |
| Yae in party | Party | `0x8015C6AB` | `0x80161E9B` | Named source | User-confirmed (15 Nov 2026) |
| Goemon pipe upgrade | Weapon upgrades | `0x8015C6AF` | `0x80161E9F` | Array-based inference | User-confirmed (15 Nov 2026) |
| Ebisumaru hammer upgrade | Weapon upgrades | `0x8015C6B3` | `0x80161EA3` | Array-based inference | User-confirmed (15 Nov 2026) |
| Sasuke kunai upgrade | Weapon upgrades | `0x8015C6B7` | `0x80161EA7` | Array-based inference | User-confirmed (15 Nov 2026) |
| Yae katana upgrade | Weapon upgrades | `0x8015C6BB` | `0x80161EAB` | Array-based inference | User-confirmed (15 Nov 2026) |
| Chain Pipe | Weapons | `0x8015C6BF` | `0x80161EAF` | Array-based inference (JP On = 01) | User-confirmed (15 Nov 2026) |
| Meat Saw Hammer | Weapons | `0x8015C6C3` | `0x80161EB3` | Array-based inference | User-confirmed (15 Nov 2026) |
| Fire Cracker Bomb | Weapons | `0x8015C6C7` | `0x80161EB7` | Array-based inference | User-confirmed (15 Nov 2026) |
| Flute | Weapons | `0x8015C6CB` | `0x80161EBB` | Array-based inference | User-confirmed (15 Nov 2026) |
| Windup Camera | Weapons | `0x8015C6D3` | `0x80161EC3` | Array-based inference | User-confirmed (15 Nov 2026) |
| Ice Kunai | Weapons | `0x8015C6D7` | `0x80161EC7` | Array-based inference | User-confirmed (15 Nov 2026) |
| Bazooka | Weapons | `0x8015C6DB` | `0x80161ECB` | Array-based inference (subweapon slot 3) | User-confirmed (15 Nov 2026) |
| Medal of Flames | Abilities | `0x8015C6DF` | `0x80161ECF` | Array-based inference | User-confirmed (15 Nov 2026) |
| Sudden Impact | Abilities | `0x8015C6EF` | `0x80161EDF` | Array-based inference | User-confirmed (15 Nov 2026) |
| Mini Ebisumaru | Abilities | `0x8015C6F3` | `0x80161EE3` | Array-based inference | User-confirmed (15 Nov 2026) |
| Super Jump | Abilities | `0x8015C6F7` | `0x80161EE7` | Array-based inference | User-confirmed (15 Nov 2026) |
| Magic Mermaid | Abilities | `0x8015C6FB` | `0x80161EEB` | Array-based inference | User-confirmed (15 Nov 2026) |
| Triton Shell | Items and keys | `0x8015C6FF` | `0x80161EEF` | Named source | User-confirmed (15 Nov 2026) |
| Gold Key | Items and keys | `0x8015C713` | `0x80161F03` | Regional-offset candidate | User-confirmed (15 Nov 2026) |
| Cucumber | Items and keys | `0x8015C717` | `0x80161F07` | Named source | User-confirmed (15 Nov 2026) |
| Lord's Pass | Items and keys | `0x8015C703` | `0x80161EF3` | Named source | User-confirmed (15 Nov 2026) |
| Silver Fortune Doll progress | Items and keys | `0x8015C707` | `0x80161EF7` | Regional-offset candidate | User-confirmed (15 Nov 2026) |
| Sasuke battery 1 collected | Items and keys | `0x8015C609` | `0x80161DF9` | Experimental guess | Unverified |
| Achilles' Heel | Items and keys | `0x8015C70F` | `0x80161EFF` | Named source | User-confirmed (15 Nov 2026) |
| Red fish count | Fish counts | `0x8015C71B` | `0x80161F0B` | Named source | User-confirmed (15 Nov 2026) |
| Blue fish count | Fish counts | `0x8015C723` | `0x80161F13` | Named source | User-confirmed (15 Nov 2026) |
| Yellow fish count | Fish counts | `0x8015C71F` | `0x80161F0F` | Named source | User-confirmed (15 Nov 2026) |
| Star | Miracle items | `0x8015C85B` | `0x8016204B` | Experimental guess | User-confirmed (15 Nov 2026) |
| Moon | Miracle items | `0x8015C85F` | `0x8016204F` | Experimental guess | User-confirmed (15 Nov 2026) |
| Flower | Miracle items | `0x8015C863` | `0x80162053` | Experimental guess | User-confirmed (15 Nov 2026) |
| Snowflake | Miracle items | `0x8015C866` | `0x80162057` | Experimental guess | User-confirmed (15 Nov 2026) |


## Region-specific value behaviour and remaining research

- **Chain Pipe** remains USA On `02`, Japan On `01`; the shared UI and write adapter translate region-specific values without modifying USA code.
- **Silver Fortune Doll progress** at JP `0x80161EF7`, **Gold Key** at `0x80161F03`, and **all four Miracle items** at `0x8016204B`, `0x8016204F`, `0x80162053`, `0x80162057` are now user-tested and working. Their original derivation remains in the provenance column, not misrepresented as a published individually named cheat.
- **Bazooka** at `0x80161ECB` and **Medal of Flames** at `0x80161ECF` were previously array-inferred; the user's latest testing confirms that the individual controls work in the Japanese game. The old dialogue/pickup event-bit changes at `0x80161DBE–0x80161DBF` are separate evidence, not competing inventory addresses.
- **Sasuke Battery 1** is the sole outstanding mapping: `0x80161DF9`, bit `0x20` are still an unverified USA-offset/bit-mask hypothesis. No independently named Japanese GameShark code proves the battery flag. It is intentionally skipped by default Unlock All and retains an on-demand manual toggle.
- The new Event Sessions **Sasuke battery probe** preset selects the read-only, 100-byte Japanese guest RAM window `0x80161DC0–0x80161E23`, which contains `0x80161DF9`. The generic Japanese preset `0x80161D80–0x80161DE3` does not. It pre-fills the experiment without overwriting saved sessions or writing game RAM. See [Sasuke battery investigation](JAPAN_SASUKE_BATTERY_RESEARCH.md).

Original USA definitions: [practice/unlocks.py](../practice/unlocks.py). Japanese mapping and user verification: [practice/region_unlocks.py](../practice/region_unlocks.py).
