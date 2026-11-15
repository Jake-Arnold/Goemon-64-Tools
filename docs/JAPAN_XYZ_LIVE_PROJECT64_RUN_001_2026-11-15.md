# Japan-0 Project64 wide XYZ report 001 — 2026-11-15

**Evidence:** user-uploaded `japan_state_probe_20261115_151245_163964.json`, produced by the live Windows Project64 Japanese toolkit. Original JSON is retained in the conversation; this repository record transcribes its key verified contents. No memory writes were performed by the experiment.

## Session

| Field | Live exported value |
| --- | --- |
| Format | `goemon-japan-xyz-heuristic-v1` |
| Game region | `japan-0` |
| Memory range | `wide` |
| Project64 PID | `33476` (transient, session-specific) |
| Host RDRAM base | `0xDFEA0000` (transient; not a guest address) |
| Endianness | `wordswapped` |
| RAM scanned | `8,388,608` bytes / **8 MiB** |
| Scene | `353` / `0x0161` — Oedo Town South |
| Character | `0` — Goemon |
| A | `2026-11-15T15:12:23.328783+00:00` |
| B | `2026-11-15T15:12:29.130343+00:00` |
| C | `2026-11-15T15:12:32.408438+00:00` |
| Candidate matches | **1,240** |
| Rows actually saved by old exporter | **200** (top-ranked) |

All three captures were in the same scene and active character, and every exported result records stable B-to-C endpoint. The remaining **1,040** matches are **not present in this historical file**. Do not infer their addresses or values from summary counts.

## Exact replicated potential player position

Five *different guest addresses* record the same complete XYZ triple at each observation:

| Guest float-triple start | A X | A Y | A Z | B/C X | B/C Y | B/C Z |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `0x80151B10` | -174.898819 | 0.0 | -142.228333 | -218.588043 | 0.0 | -191.803894 |
| `0x80151BA8` | -174.898819 | 0.0 | -142.228333 | -218.588043 | 0.0 | -191.803894 |
| `0x80151C40` | -174.898819 | 0.0 | -142.228333 | -218.588043 | 0.0 | -191.803894 |
| `0x80211870` | -174.898819 | 0.0 | -142.228333 | -218.588043 | 0.0 | -191.803894 |
| `0x802118E0` | -174.898819 | 0.0 | -142.228333 | -218.588043 | 0.0 | -191.803894 |

A sixth triple at `0x802119EC` matches the same X and Z movement while its middle float is **20.0**, not zero.

Displacement: **ΔX −43.689224**, **ΔZ −49.575562**, horizontal **66.0794** units. C exactly matches B for these addresses.

**Interpretation:** these are unusually strong, synchronized candidates for a world-position family. They could be copies, render transforms, collision references or a player-related structure. They do **not** yet identify which address, if any, is the authoritative live player task/XYZ record.

## Secondary hypotheses

- `0x8008F5F4`: (72.771667, 19, -76.898819) → (111.096329, 19, -103.286568); same-scene change/stability, different apparent coordinate frame.
- `0x8008F630`: (-76.898819, 19, 72.771667) → (-103.286568, 19, 111.096329); apparent swapped X/Z relative to above.
- `0x8008F7E4`: (57.007320, 20, -141.245270) → (111.096329, 20, -103.286568); 66.0794 horizontal displacement, a possible derived offset rather than the direct player transform.

None of those secondary interpretations is confirmed. The heuristic accepted many false positives from unrelated bytes interpreted as float32, and ranks should not be converted to probabilities.

## Follow-up cross-reference and exporter correction

The next Project64 run should repeat the wide A/B/C procedure in a different direction, preferably then another map. The **new full XYZ JSON export** emits *all* matching float candidates in guest-address order even when only the best 200 appear on screen. Use address intersections, float deltas, Y changes during jumping, and lifetimes across scene/character switches to prioritize the likely player copy. Never enable Japanese position writes, checkpoint restoration or warps on candidate evidence alone.

See [`JAPAN_XYZ_DISCOVERY.md`](JAPAN_XYZ_DISCOVERY.md) for the workflow and the revised export behaviour.
