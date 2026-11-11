---
name: goemon-upstream-review
description: "Use to review pinned mnsg source or Goemon camera branches without merging speculative code or types."
---

# goemon-upstream-review

Pin upstream `klorfmorf/mnsg` at `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`; read `LOCAL_MNSG_REVIEW.md` and phase 10. Map any borrowed type/function to actual ROM/VMA/overlay and original ASM. Treat generated memset and other linker differences as mismatches, not targets for binary patches. Do not wholesale merge another branch or edit pinned baseline. Small independently verified C is acceptable only after G2.
