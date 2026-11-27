# Semantic inventory of canonical matching C

Run from repository root:

```sh
python3 -m decomp.semantic_inventory --output /tmp/goemon-semantic-index.json
python3 -m unittest decomp.test_semantic_inventory
```

The generated JSON includes every canonical reconstructed function in USA and Japan 0 (excluding USA's 13 upstream functions). It derives membership and extents from canonical proofs, inventories and batch registry rather than maintaining a second promotion ledger. Unknown entries are retained. The sparse `annotations.json` records evidence-backed semantic aliases, behaviour, subsystem, counterpart and structure observations. Extend that file rather than hand-editing generated output. All paths are relative to `decomp/`. No original symbols, accepted source, native proof or inventory is modified.

Confidence concerns the described operation, not G2 acceptance or complete in-game purpose:

- Confirmed: directly established operation, e.g. a verified empty callback or indexed flag update.
- High: strong static/structural evidence; gameplay context may remain unresolved.
- Medium: local behaviour known, wider context unresolved.
- Unknown: no sufficiently specific classification yet.

`review_method` separates curated annotations, source-pattern classifications and known no-op digest/manifest forms. Only curated annotations assign semantic aliases. Automatic source extraction is a lexical analysis of hash-pinned C files, not a compiler or dynamic call graph. Named callees, reverse accepted callers, function references and literal `M2C_FIELD` offsets are leads; missing entries do not prove absence, and inferred types/offsets need validation. `gameplay_role` is optional. `counterpart` records reviewed relationships and differences, not guaranteed regional equivalence. `counterpart_candidate` identifies unique same-file, same-size, equal-original-digest pairs of at least 32 bytes, not verified semantic equivalence. Missing JP digests are not invented. Prior semantic atlas and other research are cited by path; unpromoted candidates are excluded from membership.

Baseline 997dc92c69ef8170a14eae4b4086a78aca6f0dd8: USA 3,529 / 259,300 bytes; JP 3,393 / 240,424 bytes. 121 curated regional annotations, 45 reviewed counterpart pairs, 247 digest candidate pairs (may overlap reviewed pairs), 5 structures and 27 fields. 5,963 pinned source bodies resolved; 4,761 functions remain Unknown. The existing native G2 proofs are unchanged. Neither a semantic classification nor its alias is a fresh native compile or runtime proof.
