# Combined VM candidate research, current 2317 predecessor

RESEARCH_ONLY, no change to strict named relocation acceptance. Based on fresh complete E234 candidate, both remaining source candidates build in the actual mixed VM translation unit. 224 compiler-produced pool bytes resolve to the exact original ROM. Only the two existing coordinate-symbol metadata bytes and one pool alignment byte change; no native instruction, pool payload or relocation record is rewritten. Original data-owner labels are conventional assembler aliases. 32 MiB ROM exact; all 7376 positive function and 26714 stable global identities preserved; strict named relocations still FAIL (82103 -> 82102, 45 removed/44 added). See independent F37C and DF98 reference experiments in sibling directories. Full canonical new-claim G2/CI for the extra two NOT_RUN.

Reproduce with the fresh E234 candidate directory from the original private-ROM verifier, and the original compiler/binutils environment configured:

```sh
python replay.py --repo "$REPO" --predecessor "$WORK/candidate" --out "$NEW_WORK" --uv "$UV" --jobs 8
```

Do not commit private ROMs, compiled objects or generated upstream assembly. No gameplay tested.

`audit_reference_delta.py` independently derives all 45 removed and 44 added linked records from the two isolated reference proofs, rechecks the native mixed-unit object HI/LO pairs, local branch, float and all 40 destinations against the original ROM; 7 malformed proof/object controls rejected. This is still a research gate, not production authorization.

```sh
python audit_reference_delta.py --repo "$REPO" --rom "$WORK/baseline/config/usa/baserom.decompressed.z64" --object "$NEW_WORK/candidate/build/usa/src/script_vm.c.o" --combined evidence.json --out "$NEW_WORK/reference_delta.json"
clang -std=c11 -O1 -g -fsanitize=address,undefined -fno-sanitize-recover=all -fno-omit-frame-pointer host_candidates.c ../usa_script_vm_f37c_reference_20261123/f37c.c ../usa_script_vm_df98_reference_20261123/df98.c -o /tmp/goemon-vm-host-research
/tmp/goemon-vm-host-research
```

Host fixture PASS: 4,096 spawn cases, 131,072 dispatcher cases (all signed 16-bit opcodes, both values of unused argument); no original gameplay test. The full mixed-unit replay was independently repeated; resulting ELF SHA-256 is identical.
