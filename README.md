# Goemon N64 — original-ROM matching-C decompilation

This is the `stable/decomp` workspace, not a runnable desktop toolkit. Start with [BRANCHES.md](BRANCHES.md), [AGENTS.md](AGENTS.md), [the decompilation README](decomp/README.md), and [current continuation](decomp/CONTINUE.md). Use `decomp/*` topic branches and PRs against `stable/decomp` only.

The legacy desktop application, packaging assets, speed-control experiments and application-only tests have been removed. Their complete source and historical root README remain at [the pre-cleanup commit](https://github.com/Jake-Arnold/Goemon-64-Tools/tree/160587eb162d957128c8c7dac62439ae5efc3942). Research documentation and the minimal compatibility helpers under `practice/` remain; the ROM input and pickup extractors still import `practice.entrances`. No matching-C source, promotion manifest, proof, test or native build input under `decomp/` has changed.

## Current toolkit (separate checkout)

Use [stable/toolkit](https://github.com/Jake-Arnold/Goemon-64-Tools/tree/stable/toolkit) for the desktop application and its current installation instructions. Clone separately:

```bash
git clone --branch stable/toolkit --single-branch https://github.com/Jake-Arnold/Goemon-64-Tools.git goemon-toolkit
```

From that toolkit checkout only, use `bash Run-Linux.sh` on Linux or `.\Run.bat` on Windows. Consult its README for dependencies and use `--read-only` when no game-memory edits are wanted. Do not launch the toolkit from `stable/decomp` or merge the two branches.

## Verification and current status

The [executor protocol](decomp/plans/EXECUTOR_PROTOCOL.md), [compiler-quirk ledger](decomp/COMPILER_QUIRKS.md), [task registry](decomp/tasks/README.md), and [canonical proof and inventory](decomp/results/README.md) govern decompilation. GitHub Actions runs the complete ROM-free regression; original-ROM, IDO, ELF identity and relocation checks remain independent requirements for native promotions. Historical counts are not current acceptance criteria. See [PROGRESS.md](PROGRESS.md) for recorded evidence.
