# Goemon Practice Toolkit: one active development branch

**Canonical development branch:** `chatgptweb/toolkit-unified`  
**Current toolkit version:** v0.11.27  
**Upstream release branch:** `main` (not modified by this consolidation).

## What the unified branch contains

This branch was forked without rebasing, squashing, or deleting code from
`chatgptweb/japan-native-recomp-toolkit-v01118` at its v0.11.26 head.
It retains all original-USA and Japan-0 controls and native Linux support
already present in that current implementation:

- Shared USA/Japan Scene Browser, entrance selection, Unlocks,
  Story Progress, Live Memory, experiment/event sessions and freeze controls.
- Original-USA source-backed **333 scene IDs / 888 distinct entrances**
  committed as `practice/data/entrance-coordinates.json`. Both regions
  use exactly the same selected entrance XYZ, heading and mode.
- Project64 (Windows), Mupen64Plus and experimental native Japanese
  recomp attachments, with region/PID/RDRAM write validation.
- Current Goemon-only Japanese post-load XYZ correction, guarded one-shot
  mapped writes and native Japan checkpoint/scene experimental features.
- Ubuntu launch script and GNOME desktop/dock identity/icon installer.
- Versioned regression suites (`bash scripts/test_japan_party.sh` and
  Windows `scripts/test_japan_party.ps1`).
- Default write-enabled toolkit mode, with region-specific safety checks.
  Old intentionally removed USA-only/unsupported Japanese actions stay
  unavailable rather than being re-enabled by older branch code.

## What to do with the old toolkit branches

Treat the following as **historical research or superseded toolkit
implementations**, not parallel development destinations:

- `chatgptweb/japan-native-recomp-toolkit-v01118`: exact v0.11.26
  source from which the unified branch was forked.
- `chatgptweb/japan-toolkit-consolidation`: older v0.11.17 toolkit,
  superseded by the current shared regional UI.
- `chatgptweb/japan-main-integration-20261116`: older v0.11.17
  shared-region UI; main controller methods were checked against the
  current v0.11.26 implementation.
- `chatgptweb/toolkit-linux-native`: earlier Linux process/input/old
  speed-channel experiment. Some speed UI was intentionally removed
  from the active toolkit at user request; do not restore it by merging
  this entire branch.
- `chatgptweb/native-emulator-savestates`: earlier emulator save
  controls. The current unified toolkit retains supported native
  save/load actions and still rejects unsupported native recomp
  savestates.
- `chatgptweb/japan-mupen-rdram-probe` and
  `chatgptweb/japan-mupen-ambiguity-fix`: earlier Japan Mupen
  discovery experiments. Current backend has superseded connection
  and ROM/pointer verification.
- `chatgptweb/dual-region-foundation`: initial shared regional
  groundwork.
- `chatgptweb/impact-value-search`: earlier research/value-search
  experiments. Current UI keeps the supported Value Search and State
  Discovery features but not removed redundant dashboard panels.

The remaining branches called `decomp`, `file11`, `japanese-decomp`,
`overlay`, `impact-research`, `symbol`, `ebisumaru-research`,
`usa-external-memory-leads` and other Codex research are separate
decompilation, reverse-engineering or ROM/port studies. They must not
be indiscriminately merged into the toolkit branch. Extract a *specific*
reviewed toolkit-relevant change only when needed.

**Do not force-push, reset or delete historical branches to consolidate
the toolkit.** The branch names can remain for provenance even though
there is only one active development target for toolkit UI/backend work.

## Development rule

All new toolkit UI, Linux integration, process attachment, practice
feature, debugger and current-region memory edits go to
**`chatgptweb/toolkit-unified`**. Every user-facing change bumps
`practice/version.py`, updates the README release section and
`PROGRESS.md`, and adds or updates targeted tests. Decomp changes
remain in the authoritative decomp branch and/or reviewed research PRs.

Merge this branch into `main` only after regression tests and actual
USA/Japan runtime smoke checks have passed. The unified PR remains
**draft** until then; this consolidation makes no claim that live native
Japanese warp/write results have been verified.

## Switch an existing Ubuntu toolkit checkout

```bash
cd ~/Desktop/Goemon-64-Tools-JP-Recomp
git fetch origin
git switch chatgptweb/toolkit-unified || git switch --track origin/chatgptweb/toolkit-unified
git pull --ff-only
bash scripts/test_japan_party.sh
bash Run-Linux.sh
```

If the GNOME desktop launcher has not already been installed for this
checkout, run `python3 scripts/install_linux_launcher.py` once, then
open the application from Ubuntu's app grid. Existing launcher
preferences and XDG coordinate cache are unchanged; the bundled
source-verified original-USA entrance table takes precedence.

## Consolidation audit and limitations (2026-11-16)

The original toolkit source and the two earlier integration branches
were inspected through the GitHub connector; the current v0.11.26
`practice/toolkit.py` contains **all method names** present in the
earlier `japan-toolkit-consolidation` and
`japan-main-integration-20261116` toolkit controllers, and
`practice/ui_extension.py` likewise contains all method names.
Selected legacy method lines differ because old branches reference
Project64/Mupen-only Japanese connections and earlier warp logic;
they should not overwrite the currently working native recomp
integration. This is a feature/scope audit, **not** a full equivalent
code test or proof that every experimental historical branch feature
is present.

The other toolkit-related branches were compared by ancestry, file
changes and selected method sets. They have diverged history and may
include unrelated decomp changes; no blind git merges or risky
conflict resolutions were attempted. This is a **single canonical
toolkit branch**, not a promise to transplant every abandoned
experimental implementation. No old feature branch or its history
was deleted.

**Validation still required on the user's machine:** compile/test the
entire `practice` tree; run the Bash GUI tests under Xvfb; connect the
USA and Japanese recomp targets; exercise mapped writes, full scene
reload, shared XYZ placement and the Ubuntu dock icon association.
