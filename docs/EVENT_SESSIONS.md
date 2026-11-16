# Repeated persistent-event experiments

The **Event sessions → Event flag sessions** subtab captures only the 100 persistent event bytes at
`0x8015C608..0x8015C66B`. The adjacent **Advanced RAM comparison** subtab retains the former State discovery
A/B/C focused/wide comparison. All session capture/analysis is read-only, even when the
toolkit's other unsafe controls are enabled. `--read-only` can be used for research.

## First experiment

1. Connect to the host you want to study. With both games running, explicitly
   choose `project64` or `recomp` on Dashboard.
2. Choose one event that you can repeat from a known pre-event state. Use your
   own emulator savestate/save or equivalent host facility. Logical toolkit
   checkpoints do not reproduce every actor/script and are not a proven reset.
3. Enter an experiment name, for example **Benkei first conversation**, and click
   **New session**. A ROM SHA-1 is optional; supplied hashes remain unverified
   against the running game. Each backend has separate sessions.
4. Set role to **idle**. Capture **A**, wait a few seconds without performing the
   event, capture **B**, then **Record trial**. Add a short note if useful.
5. Set role to **event**. From the pre-event state capture **A**, perform only the
   chosen action, wait until dialogue/cutscene finishes, capture **B**, then
   **Record trial**. Room/character/pointer changes between A and B are allowed;
   wait for stable gameplay at each capture, even if the NPC moves you elsewhere.
6. Restore the same pre-event state yourself and repeat step 5. A fresh A is
   required for each trial. Two independent event trials plus idle evidence are
   the first useful minimum, not a confirmation threshold.
7. Add **control** trials for a distinct competing explanation, such as an
   inventory-only change without the genuine quest dialogue. Give that control
   a descriptive note. Do not mix different quest stages as repeats of one event.

For persistent one-time progression, use A/B only. Optional **C** records a
return to A for reversible experiments; it does not remove persistent candidates.
Reversion is assessed per bit, including partial reversions within one byte.
Capturing A starts a new pending pair; recapturing B clears an old C. Discard
captures cancels the pending trial without deleting recorded trials.

The recorder rejects active loading/scripts, incomplete reads and context changes
*during one capture*. It now allows different maps, characters and player/task
pointers *between* A/B/C captures and between trials because the captured data is
the fixed, global saved-event bank. Reconnecting still requires a fresh A.

A/B feedback shows the source/destination map, character and pointers; the session
summary counts context-changing trials. Selecting a ranked row shows exact context
for its associated captures. These changes are provenance, not extra ranked flags.
A room transition can change unrelated saved flags, so repeat the same event and
use a comparable transition-only control where possible. Keep separate events in
separately named sessions, even though context equality no longer blocks recording.
Existing v1 same-room sessions remain compatible. Captures are not atomic:
identical before/after context cannot rule out every intervening change.

## Reading the shortlist

Each row identifies an address, bit mask and set/clear direction. **Event support**
is supporting trials / total event trials. **Opposite** and **Unchanged** identify
contradicting or absent changes; **Idle/control overlap** counts controls where
that bit changes in either direction. Noise overlap lowers priority without
discarding the evidence. Both directions can appear separately.

Select a row to see exact supporting, opposite, unchanged, control and C-reversion
trial IDs plus their roles and notes. Rankings cover every bit in the event block;
they do not use the old State discovery UI's truncated candidate list. Repeated
observations do not establish causality, event-trigger semantics or write safety.
No row is automatically marked confirmed, and no memory edits are performed.

## Local files and reopening

New sessions and each recorded trial save atomically to
`practice/diagnostics/event_session_<id>.json` in source runs, or
`%LOCALAPPDATA%/GoemonSpeedrunTools/diagnostics/` in packaged runs. These files
contain local event-byte samples and research notes; keep them out of Git.
The existing diagnostics ignore rule covers them. There are no full RAM dumps.

**Open session** restores recorded trials and recomputes rankings. Pending captures
are not persisted. Imported sessions save subsequent trials to the diagnostics
directory, not automatically back over the selected source file. Failed writes
retain the previous session file and pending captures for retry. Unsupported
schemas, malformed contexts and files over 2 MB are rejected. The v1 limit is
500 trials per session; start a separate experiment when appropriate.

Each session stores backend, optional unverified ROM hash, timestamps and trial
context. Do not pool different ROM versions or assume the file proves which ROM
was running. ROM identity verification and a shared semantic registry are later
milestones. Analysis runs off the Tk thread; captures synchronously read a bounded
100-byte block plus small context checks. Wide sampling and dynamic structures
remain in the existing State discovery tools.
