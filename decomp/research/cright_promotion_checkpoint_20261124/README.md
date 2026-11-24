# C-Right promotion checkpoint — research only

Ten source candidates from #205, #209, #210 and #214, authenticated to live `stable/decomp@878d8cffdf3baf98a5dfcf4dc6fc5cb5b7ca45d1`. Fresh full-flag native IDO reproduces 338/338 instructions and 62/62 per-function named relocations at original VMAs. The #214 filenames were swapped relative to evidence: the store-after-constants source is the actual positive (SHA-256 08da2274…), baseline-labelled file is the negative (ff3cacfd…, 68/73, first +0x3C). Both are preserved here. No new compiler finding.

USA: fresh canonical 2319-C verifier PASS; 4 C / 728 B integrated into that exact predecessor, full expanded and retail ROMs exact; 7376 positive FUNC identities, 82102 semantic relocations and 26714 stable globals exact after guarded one-byte symbol type corrections. Prospective strict inventory 2323 C +13 upstream / 5040 ASM.

JP: 6 C / 624 B integrated in pristine all-ASM original build only; exact expanded/retail ROMs, 7376 FUNC, 80810 pristine relocs and 26393 stable globals. Canonical JP2528 predecessor still needs full replay. A pristine proof is not canonical.

Full baseline local CI exit 0, not candidate CI. Canonical verifier adapter, promotion integrity and candidate full CI NOT_RUN; no canonical manifest, ownership or accepted counts changed. Do not merge this checkpoint as promotion. Preserve prior failed variants as ASM. Full source-only replay ZIP delivered in the originating session (SHA-256 ff8f5fd2da70b07fdbea300164cd0a066e0758e3da836f148322712998a51524); it includes native replay, regional active-owner split/compile/relink, ROM/ELF/global/relocation audit and summary. No ROMs, extracted ASM, ELF objects, game assets or proprietary compiler committed.
