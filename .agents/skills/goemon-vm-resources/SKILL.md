---
name: goemon-vm-resources
description: "Use for Goemon VM resource lookup, loader, retries, signed halfword indices and entry versus live resource IDs."
---

# goemon-vm-resources

Read `VM_RESOURCE_CALLGRAPH.md`, `VM_CHECKPOINT.md`, `script_vm.c` and header. Check live status of D468, D68C, DF98, F038. Keep the entry ID for DDC4 separate from global ID reloaded after callbacks. F038 needs signed half-index and two lookup paths; D468 needs its observed 32-byte frame. Reuse ROM-bound and callback mutation guards, acknowledge unknown retail callback effects, then require full-unit and G2 verification.
