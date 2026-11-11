---
name: goemon-vm-graphics
description: "Use for Goemon VM display-list emitters, two-word graphics writes, float callback ABI and number formatting."
---

# goemon-vm-graphics

Read phase 05, `script_vm.c`, header and current emitter probes. Preserve each pair of command words, buffer cursor updates, callback order, FPU register path and branch delay slots. Host-test first/last words, sentinel buffers and state changes. Compare native IDO instructions; equivalent host graphics output is not binary identity. Keep ASM if production full-ROM gate has not passed.
