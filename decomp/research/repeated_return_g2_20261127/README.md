# Isolated native IDO repeated-return research — 27 November 2026

**RESEARCH_ONLY. No canonical promotion.** 9 USA + 9 Japan functions, 144 matching bytes per region. The original ROMs and pinned compiler were authenticated; all 18 independent native original-address links matched exactly, with matching function identity and extent in the linked ELF. Original USA extent also confirmed in pristine baseline ELF. Japanese original extent is Splat-derived. No original ROM, assembly extraction, object or compiler binaries are included.

Tested source base: 0ad88225c1a11f85454b259103f0f4c6ff49fa16. Publication parent: 35a93f259cc00cde13eaa591008323df1278c24f (intervening Batch #6, no name overlap in its published regional candidate lists). The proof is a record of the earlier isolated run, not a fresh full G2 proof on the publication parent.

## Reproduce

Use the authenticated pinned upstream checkout and the project's private native environment, with original USA and Japan retail/expanded images, generated Splat assembly, the exact original USA baseline build and MIPS binutils available. Use the tested stable base as --repo for exact historical proof metadata. Invoke:

    python3 replay.py --repo /path/to/stable-decomp --upstream /path/to/mnsg-japan --report /tmp/repeated-return-proof.json

The script authenticates ROMs, IDO, pinned upstream and USA baseline; independently assembles references, compiles candidate and negative controls, links the positives and checks code and ELF identity. The final report records exact compiler flags, source hashes, ledger hashes and outcome per attempt. The ordinary flags reject the empty body at +8, while -g2 matches. A changed volatile-local body rejects at +0. Source paths are relative to this directory. A fresh run against a later repo will report that repo's current ownership counts and ledger hash.

## Search and limitations

350 larger targets yielded no exact results; 76 repeated-return targets yielded 9 exact USA matches, 66 mismatches and one excluded pool/table. Ten targets overlapped the two cohorts. 1,395 initial native compiler attempts (including failed compilation) and 54 clean replay attempts. Both region candidate lists of intervening Batch #6 were checked for overlaps. Relevant older open research filenames and selected manifest/index contents were inspected; opaque pending sources were not exhaustively parsed.

The flags are outside the approved production flag set. Retain original ASM. Whole translation-unit equality, candidate full-ROM/ELF/semantic relocation proof, strict inventory and promotion integrity NOT_RUN. Do not treat byte-identical neighboring empty functions as proof of historical C file layout. The requested 100 new USA matches were not reached.
