# IDO 5.3 / MIPS matching-C compiler quirks

This is a cumulative evidence-led knowledge base for reusable compiler behavior found while matching original Goemon 64 functions. Consult it before variant searches. Record new findings in the same commit as the associated decomp research or promotion, even when a function remains assembly-owned.

## Entry template

### [Short description] — [verified / hypothesis]

- **Region / function / ROM offset / VMA:**
- **Compiler and flags:**
- **Minimal C example or source reference:**
- **Observed versus expected code generation:**
- **Working expression/type/layout or failed variants:**
- **Reproduction command and evidence paths:**
- **Verification level:** isolated native / combined G2 / research only
- **Applicability and limitations:**

Do not treat an isolated instruction match as proof of relocation or full-ROM equality. Keep observations specific, reproducible and deduplicated; link research artifacts rather than embedding copyrighted original code bytes.
