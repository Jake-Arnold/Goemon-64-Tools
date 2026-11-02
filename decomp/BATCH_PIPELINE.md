# Batch decompilation workflow

This is a local research pipeline for the pinned US build. It generates C drafts,
compiles them with the original IDO flags, resolves references at original ELF
addresses, and compares exact function bytes. Successful probes become **review
candidates**, not automatically verified decompilation entries.

The matching manifest, original-ROM acceptance checks, companion application and
unsafe-option defaults are unchanged. No game process is opened or written.

## Requirements and storage

Run compiler jobs inside Linux/WSL with the existing verified mnsg baseline,
MIPS binutils, the baseline Python environment and clean local tool checkouts:

- mnsg: `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`
- m2c: `a21c1dcd7255b176c032bb932f521846e98d4372`
- optional decomp-permuter: `ec2efeebb33e2b1de81e39fbf7cbe3cd97350472`

Use research storage outside Git, or the explicitly ignored `decomp/local/` or
`practice/diagnostics/` directories. Queue databases contain extracted original
assembly and instruction bytes; attempts contain generated C, objects, ELF probes
and logs. **Do not commit them.** Public reports contain metadata/hashes only.
All attempts are retained. Existing reports and review destinations are not
replaced. The pipeline does not use distributed workers or upload game data.

## Initialize once

From the toolkit checkout:

```bash
python -m decomp.batch init \
  --cache /root/goemon-batch/cache \
  --baseline /path/to/verified-run/baseline \
  --m2c /path/to/pinned/m2c \
  --python /path/to/baseline/.venv/bin/python \
  --permuter /path/to/pinned/decomp-permuter
```

Initialization verifies the source/tool pins, clean tracked sources and complete
baseline ROM checksum. It indexes all 7,363 baseline assembly entries and excludes
74 functions in the published matching reference, leaving 7,289 queued entries.
All baseline assembly functions were located. Already-upstream C is excluded.
Reinitializing the same baseline preserves attempts and refreshes those exclusions.
A different baseline needs its own cache.

## First-pass batch

```bash
python -m decomp.batch run \
  --cache /root/goemon-batch/cache \
  --limit 100 --max-size 128 --region main \
  --workers 2 --seconds 10 > /root/goemon-batch/first-pass.log
```

The default name scope is generated `func_...` entries; `--scope all` also includes
named SDK/runtime entries. `--region main`, `overlays` or `all` selects ELF sections,
not guessed address prefixes. Candidates are ordered by size and name. Each
function has a total elapsed process budget. Local workers run concurrently;
subprocess deadlines kill their process groups. No indefinite permuter runs occur.

SQLite commits each result. A Linux cache lock prevents competing coordinators.
After interruption, the next owner marks unfinished attempts interrupted without
deleting artifacts. Only dispatched work is claimed. Completed jobs are skipped
on resume; `--retry --max-attempts 2` explicitly permits another attempt per recipe.
Interrupted attempts count against that budget. New context/tool/recipe identities
create a separate attempt history instead of overwriting previous results.

## Context and bounded search

The default context supplies MIPS scalar types only. Missing parameter/structure
information is deferred, not replaced with invented types. `NULL` is supplied as
a standard null constant for standalone compilation. Inline-assembly translations,
extra functions and generated data require further review/layout work.

To reuse reviewed declarations:

```bash
python -m decomp.batch context \
  --baseline /path/to/verified-run/baseline \
  --source /path/to/reviewed_context.h \
  --output /root/goemon-batch/reviewed-context.c

python -m decomp.batch run \
  --cache /root/goemon-batch/cache \
  --context /root/goemon-batch/reviewed-context.c \
  --limit 100 --workers 2 --seconds 10
```

Contexts must be preprocessed C accepted by m2c and IDO; declaration-only contexts
are appropriate. The helper uses the existing upstream include paths/definitions.
It does not recover missing interfaces automatically. The snapshot is content
addressed and reused. The first job populates m2c's parse cache before concurrent
readers; if no cache is produced, later jobs disable cache writes to avoid races.
Compiler files, binutils, interpreter, dependency lock, flags and pipeline source
hashes are recorded in the recipe. A reviewed VM-header context was also exercised.

Optional bounded search is enabled by `--search-seconds 2` with a larger total
`--seconds` budget. It uses one local permuter worker per batch worker, with
function/external type mutation and AST removal disabled. Original assembly is
assembled/linked and checked against baseline bytes before being used as a target.
A zero scorer result is compiled and linked again and must pass the actual byte
and address comparison. Search exhaustion remains a recorded mismatch, preserving
the first-pass evidence. Low scorer values alone never count as a match.

## Reports and export

```bash
python -m decomp.batch report --cache /root/goemon-batch/cache \
  --output /root/goemon-batch/report.json

python -m decomp.batch export --cache /root/goemon-batch/cache \
  --output /root/goemon-batch/review-bundle
```

Use `--recipe RECIPE_ID` on either command to inspect/export an earlier context or
search recipe. Review exports recheck both candidate source hashes and linked ELF
hashes/code/entry addresses before creating the destination. They contain standalone
candidate C and a metadata report, not a patch to the matching manifest.

Results distinguish `linked_match`, `mismatch`, `needs_context`, `needs_layout`,
`unresolved_symbols`, generation/compiler/link failures, unsupported translations,
timeouts and interrupted attempts. Exported source can still need interface and
unit-layout review. Allocated data/common storage and extra functions are not
silently discarded to manufacture a match.

## Whole-ROM gate after review

Integrate reviewed candidates by their original translation units, preserving
remaining assembly and data layout, and add appropriate semantic coverage. The
current matching-manifest layout remains scoped to the original main-segment
mapping; overlay promotion still needs an explicit reviewed layout recipe.

The default verifier still builds a fresh baseline. After that baseline stage
passes, it writes a provenance certificate alongside the build outputs. Subsequent
reviewed batches can reuse it:

```bash
python -m decomp.verify \
  --upstream /path/to/pinned/mnsg \
  --baseline-cache /path/to/fresh-run/baseline \
  --workdir /root/goemon-batch/new-gated-build \
  --manifest /path/to/reviewed-bundle/manifest.json \
  --source-dir /path/to/reviewed-bundle \
  --retail-rom /path/to/user-retail.z64 \
  --report /root/goemon-batch/new-gate-report.json --uv /path/to/uv
```

The cache must retain its original source pin/clean tracked files, reference ROM,
built ROM, ELF, IDO files, dependency lock and dependency environment. Changed
provenance fails validation. The candidate is always cloned and built separately;
cache reuse never skips per-function addresses/bytes, assembly-marker exclusion,
C-object link evidence or complete ROM equality. Source hashes are measured from
the files actually copied into that candidate, including reviewed source bundles.

## Measured validation

[First-pass metadata](results/batch_pilot.json), [bounded-search metadata](results/batch_search_pilot.json)
and [gate validation](results/batch_validation.json) record actual runs. Observed on this machine with two local workers:

| Run | Elapsed | Result |
| --- | ---: | --- |
| 100-function first pass | 11.6 s | 21 linked probe matches / 424 instruction bytes |
| Same sample with two-second searches | 15.0 s | 22 linked probe matches / 456 instruction bytes |
| Fresh baseline plus candidate gate | 47.5 s | Existing 74 C functions and complete ROM match |
| Certified baseline plus reviewed-bundle candidate | 24.9 s | Same 74 functions and complete ROM match |

The pilot covers the 100 smallest eligible main-segment functions, so it is not
representative of the whole game. Many remaining failures need shared type information.

Probe matches do **not** change the 74-function verified reconstruction count or
the [whole-build inventory](INVENTORY.md). Full-ROM acceptance and reviewed unit
integration remain required. There is no new packaged executable or in-game test.
