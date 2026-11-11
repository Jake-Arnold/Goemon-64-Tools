---
name: goemon-target-triage
description: "Use to choose or prioritize the next Goemon assembly function instead of wasting variants on exhausted candidates."
---

# goemon-target-triage

Check `manifest.json`, `results/inventory.json`, `MASTER_WORK_QUEUE.md` and recent execution reports. Exclude already promoted functions and the unchanged 762-target scalar sweep. Prioritize well-bounded original regions with known ABI, nearby matching C and a specific remaining mismatch. Return only ROM/VMA/size, unit, rationale, source-backed hypothesis, test and stop condition. Triage changes no counts.
