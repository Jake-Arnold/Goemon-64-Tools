# Japanese dispatcher and allocator research — 25 November 2026

Inputs: authenticated Goemon-64-Tools stable/decomp `11f76ecc7234a6f91047b538c179ce564fa7c5f9` (source archive 15031871479), privately supplied pinned upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, Japan expanded SHA1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`, retail SHA1 `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b`, IDO5.3 cc SHA256 `76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0`. Original ROMs and proprietary toolchain are NOT included. Place GNU MIPS tools and their runtime dependencies on PATH/LD_LIBRARY_PATH. The pinned upstream must have its original Splat per-function reference regenerated from the authenticated private Japan ROM. Read repository policies and compiler ledger before each attempt. All command output paths must be private scratch locations.

```
python3 factorial/replay.py --repo "$REPO" --upstream "$PRISTINE" --out "$WORK/native"
python3 factorial/diagnostics.py --repo "$REPO" --upstream "$PRISTINE" --normal "$WORK/native" --out "$WORK/diagnostics"
bash factorial/test_host.sh
```

`4408`: direct/explicit x unmasked/masked produces 26/26, 21/26, 23/26, 23/26 respectively. `3C90`: same matrix 88/111, 87/111, 67/111, 108/111. The sanitized diagnostic table records IDO generator virtual-register choices, not final physical machine register names. Diagnostic and ordinary linked instructions and relocations agree across all eight variants. The direct donor load has destination xr15 and base xr2; introducing a register local changes destination to xr3 without changing base; the mask creates an additional temporary. In 3C90 the local also changes pointer allocation from xr2 to xr3. No new exact 3C90 source, no claim of a general allocator law. All sixteen GCC/Clang ASan/UBSan host runs passed 131072 cases each (2,097,152 total).

Dispatcher candidate is 120 bytes and has four true reference relocations; the independently assembled named reference has two synthetic D_3ADD4 records in addition to those four. The 72-byte-table negative control fails original instruction equality. Candidate and negative each pass 36 host cases under both GCC and Clang. Local replay script requires an exact verified JP2842 canonical native predecessor with all source owners and link script retained, plus separately regenerated pristine per-function ASM. It rejects any predecessor ELF fingerprint change. It never edits a ROM, raw opcode or relocation record. Review the saved full integration status before claiming a promotion. The script mutates the supplied private scratch checkout; never pass a working repo or pristine input as checkout.

```
PYTHONPATH="$REPO" python3 dispatcher/integrate.py --checkout "$JP2842_SCRATCH" --pristine "$PRISTINE" --work "$WORK/jp2843" --uv "$UV" --jobs 8
```

The integration imports the exact authenticated repository's existing `decomp` native modules; use that full source archive (not included). Canonical publication additionally requires strict stored integrity and successful hosted ROM-free regression and routing checks on the current PR merge revision. No gameplay claim.

Fresh authenticated canonical JP2842 predecessor reproduced through every historical native stage. New JP2843 dispatcher full expanded/retail ROM, 7376 function identities, 26393 stable global identities, independent 80652 semantic relocations, exact one-name ownership and strict inventory all PASS. The two named predecessor offset references were independently assembled as numeric constants in a full original-ASM shadow, with original ROM equality and no native code or relocation editing. See dated G2 proof; no claim of historical source layout or gameplay. Hosted candidate CI and normal merge required before publication.
