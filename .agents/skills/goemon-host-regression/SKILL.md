---
name: goemon-host-regression
description: "Use to create deterministic host regression and sanitizer tests for Goemon function semantics, flags, callbacks, resources and linked lists."
---

# goemon-host-regression

Derive cases from observed original MIPS and neighboring `decomp/test_*.c` / `test_*.py`. Cover signed boundaries, nulls, field sentinels, callback mutation, call order and list operations. Use fixed seeds, ASan/UBSan where compatible, and one mutant that the test must reject. Record actual case counts and commands. HOST_TESTED is not IDO equality, G2 proof or in-game verification. Commit no original ROM words.
