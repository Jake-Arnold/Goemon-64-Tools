# Reproducing the decomp workspace

The repository contains the source, task plan, build scripts, lockfiles and
verified result records. Large or proprietary inputs stay in the ignored
`practice/diagnostics/` directory. This keeps the worktree reproducible without
publishing the USA game ROM or the IDO compiler.

## Private and pinned inputs

Create the local input directory and check out the exact upstream source used by
the verifier:

```sh
mkdir -p practice/diagnostics/decomp-100-inputs
git clone https://github.com/klorfmorf/mnsg.git \
  practice/diagnostics/decomp-100-inputs/mnsg-pinned
git -C practice/diagnostics/decomp-100-inputs/mnsg-pinned \
  checkout 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee
```

Supply a privately held USA retail ROM as
`practice/diagnostics/decomp-100-inputs/usa-retail.z64`. The expected SHA-1 is
`df8083a54296b8c151917c5333e1c85f014a2a66`. If a decompressed reference is
available, place it at `practice/diagnostics/decomp-100-inputs/usa-decompressed.z64`;
it must be exactly 33,554,432 bytes with SHA-1
`6ea0ed71032ce08fc2745f412d84936382197494`.

Provide the pinned native IDO 5.3 compiler at
`practice/diagnostics/decomp-100-inputs/mnsg-pinned/tools/ido-5.3/cc`, along
with the MIPS binutils used by the build. These binary tools are not stored in
Git. Keep all private inputs under the ignored diagnostics directory.

Check the local files before building:

```sh
git -C practice/diagnostics/decomp-100-inputs/mnsg-pinned rev-parse HEAD
sha1sum practice/diagnostics/decomp-100-inputs/usa-retail.z64
sha1sum practice/diagnostics/decomp-100-inputs/usa-decompressed.z64
```

The reported source commit and checksums must match the values above. The
retail ROM alone is sufficient for `decomp.verify`; the decompressed copy is
used by original-address research tools.

## Fresh proof and inventory

Run from the repository root, choosing new work and report paths each time:

```sh
python3 -m decomp.verify \
  --upstream practice/diagnostics/decomp-100-inputs/mnsg-pinned \
  --workdir /tmp/goemon-decomp-build \
  --retail-rom practice/diagnostics/decomp-100-inputs/usa-retail.z64 \
  --report practice/diagnostics/decomp-verify.json \
  --uv "$(command -v uv)" --jobs 2

python3 -m decomp.inventory \
  --baseline /tmp/goemon-decomp-build/baseline \
  --candidate /tmp/goemon-decomp-build/candidate \
  --report practice/diagnostics/decomp-inventory.json
```

Only run inventory after the verifier succeeds. The workdir and report paths
must not exist beforehand. The authoritative checked-in proof and current
function inventory are `decomp/results/combined.json` and
`decomp/results/inventory.json`.
