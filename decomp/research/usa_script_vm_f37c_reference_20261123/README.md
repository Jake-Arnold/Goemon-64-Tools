# Independent ASM-reference relocation research

RESEARCH_ONLY, against authenticated stable/decomp 1ddb1b0941b0f39d4db6b0a3534fc1f230b51e0e. Existing strict named-relocation acceptance is unchanged. The script independently assembles original private Splat source, a shadow reference with local symbol visibility, and original native IDO C. It checks original named relocations against the actual upstream baseline objects and requires all native/independent-reference relocations, linked original instructions and pool bytes to agree. Negative controls alter pool/address/branch provenance; they must fail. No production ELF or relocation record is edited. See evidence.json.

Read current project policies and compiler quirks. Use a clean built, authenticated original-USA upstream checkout at 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee. From this directory, using absolute paths and a previously absent OUT directory:

```sh
python verify.py --repo "$REPO" --baseline "$BASE" --binutils "$BIN" --lib "$LIB" --out "$OUT"
```

Private generated ASM, ROMs, tools and ELF files must remain outside the repository. This is not a canonical promotion or a policy exception. Full mixed-unit and whole-ROM integration for this candidate remains to be accepted.
