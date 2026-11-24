# Japan C-Right6 original-ROM promotion replay

Pinned base `02e042d969c382217f4561fffd9cc719523de970`; upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`; original native IDO 5.3. Authenticate all private inputs using the repository runbooks. The source manifest in this directory is a **prospective** immutable six-function manifest, not proof of acceptance on its own.

Reproduce with the existing original-ROM build tools and Python dependencies. Start with a private, verified JP2118 checkout (replay the existing historical stages using `decomp.japan_1686_promotion` and its predecessor runbooks) and two separately authenticated pristine Japan-0 Splat splits: the original upstream Splat layout (`config/japan_0/splat.yaml`) for native100 and the all-ASM layout used by the JP6 isolated checkpoint. Both use the exact same original expanded ROM. Set the paths to your private checkout, dependencies, runtime, and compatible uv adapter. From the repository root:

```sh
bash decomp/research/cright_promotion_checkpoint_20261124/replay_jp6_from_2118.sh \
  "$JP2118_CHECKOUT" "$JP_PRISTINE" "$JP_NATIVE100_REFERENCE" "$DEPS" "$RUNTIME" "$UV" "$NEW_PRIVATE_WORK"
```

Each predecessor stage runs its native stage/build/verify and snapshots the linked ELF. The historical C-Right relocation-provenance reference is independently assembled; it is not normalized against candidate output. The new stage independently checks exact JP2528 predecessor ELF, original named target relocations, original owner split, unchanged code/relocations during the guarded ABS-symbol type restoration, complete original expanded/retail ROMs, positive ELF function identities, canonical relocations, stable globals and strict C/ASM ownership. It must also reproduce the independently integrated candidate ELF hash. No canonical repository records are changed by the replay driver.

Only after successful native output may the local candidate be activated:

```sh
python3 -m decomp.research.cright_promotion_checkpoint_20261124.activate_jp6 "$NEW_PRIVATE_WORK/jp2534"
python3 -m decomp.japan_cright6_integrity
CC='gcc -no-pie' python3 -m decomp.local_ci
```

Activation creates local candidate manifest/proof/inventory only, and full CI must succeed before normal reviewed PR publication. The final CI includes both USA and Japan canonical integrity checks. Preserve all frozen historical proofs. Do not commit the private working directory, generated assembly, objects, ROMs or tools. No original gameplay is implied.

If a native100 compile was interrupted after staging while the linked JP2428 predecessor remains unchanged, `python3 -m decomp.research.cright_promotion_checkpoint_20261124.resume_native100 --checkout "$CHECKOUT" --reference "$JP_NATIVE100_REFERENCE" --work "$NEW_PRIVATE_WORK/jp2528-native" --uv "$UV"` restarts that stage with the frozen original predecessor, new target objects, and the same full native gates. Verify the recompressed retail ROM again before invoking the JP6 stage.
