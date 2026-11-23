# USA / Japan original-function donor crosswalk (seed v1)

**Research metadata only. No new matching-C promotion, gameplay proof, runtime write, or automatic address arithmetic.** This register is based on the authenticated original USA and Japan-0 regional research already incorporated into `stable/decomp` as of commit `56e4754255403f012cc9bc88ba39ec1f4fadfb6c`.

## What is linked

- **118 explicit original-address C-source donor relationships**: 99 documented USA→Japan ports from eight published regional metadata manifests; 19 Japan→USA ports from the original-ROM verified 19-function recovery manifest.
- **92 distinct USA originals**, **109 distinct Japan originals** (multiple original functions share donor sources; this is intentionally *not* a bijection).
- Each link records both original function names and ROM offsets, exact instruction extent, original instruction SHA-256 and the reviewable source manifest. Lookup is bidirectional by searching either region endpoint.
- These historical native-G2 ports already contribute to their respective region counts. The table adds **0** new accepted C. Current published snapshot: USA **2,164 C**, Japan **2,370 C**.

## Using the register

```sh
jq '.links[] | select(.usa.name == "func_801D600C_6013EC")' decomp/regions/function_source_donor_links_v1.json
jq '.links[] | select(.japan_0.original_rom_offset == "0x6061AC")' decomp/regions/function_source_donor_links_v1.json
```

A same-byte donor can be reused for many different original addresses, especially no-ops, registration wrappers and setters. **A C-source donor relationship is not necessarily a unique semantic function counterpart.** For example, the same-named USA/JP `func_80004170_4D70` has different regional bodies; it is explicitly excluded from equivalence claims. Never extrapolate the persistent-data-global `+0x57F0` rule to function VMAs or ROM offsets.

## Coverage and extension

The **7,376 original positive-sized ELF function identities per region** are the universe, not 118 assumed one-to-one pairs. This is an initial *evidence-backed* mapping, not an exhaustive crosswalk. Unmapped functions remain unknown, not absent. Future discovery should add links with region, name, original ROM offset, size, original-code fingerprint, confidence/classification, source manifest, compiler and full-ROM proof tier and reviewed PR. Semantic counterparts with different original instructions must be represented as a distinct `semantic_correspondence` relationship with original call-graph/struct/overlay evidence, never silently as byte-identical donors. Changed-region copy/paste requires original IDO 5.3 and the complete original-ROM / ELF / relocation / strict-inventory / full-local-CI promotion gates.

## Provenance

This seed imports the explicit 11 + 36 + 4 + 37 + 2 + 4 + 2 + 3 earlier Japanese source-port records and 19 later USA cross-region source-port records. See each `provenance.manifest` in the JSON. The starting 38 short-function donor hints in research PR #183 are *not* included as accepted links without their original per-function evidence and post-72-promotion deduplication. Research PR #184 also overlaps one USA function accepted in the latest 72-function canonical promotion and is not a source of new accepted counts.

**Tests for this metadata-only change:** identity/ROM suffix consistency, SHA-256 format, no duplicate original-offset pair, manifest counts and cross-region direction, source provenance existence in the live branch, and three representative original-ROM byte-hash checks on the uploaded authenticated USA and JP images. Full canonical local CI and any new native compiler attempt: NOT_RUN (no matching-C changes).
