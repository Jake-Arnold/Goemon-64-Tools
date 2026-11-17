# Phase 1 actor-origin trace: Super Pass, Ghost Toys and Mr. Arrow (17 November 2026)

**Evidence:** authenticated USA NG5E and Japan-0 NG5J 32 MiB expanded retail ROMs, original MIPS/script words, original native room/stage/actor instance tables. Original SHA-1s: USA `6ea0ed71032ce08fc2745f412d84936382197494`; Japan `6f8745fecc3a5e7d4918c7a73353eb0726116ded`. This work is **read-only static research**; no gameplay capture was performed here, no native C compiled and no G2/ELF/full CI proof performed. Earlier JP gate-opening gameplay report remains one event trial (no controls).

## 1. Original native launcher of Super Pass event 202

In original native **resource 54**, the caller sequence in **both** regions at file-relative **`+0xA0C..+0xA1C`** loads the regional `func_8003D388`-equivalent event dispatcher into `t9`, supplies **`a0=0xCA` (event 202)**, makes **`jalr t9` at `+0xA18`** and supplies **`a1=1`** in the delay slot. Original dispatcher destination differs by region: USA **`0x8003D388`**, Japan **`0x8003CFF8`**; direct comparison of original instruction words confirms both.

The registered event table maps event 202 to resource 94: USA script entry `+0x4B70` and Japan `+0x312C`. In **that** event, the script sets bank-C **flag `0x05E`** at USA `+0x4C58` / JP `+0x3214`, then bank-C **flag `0x000`** at USA `+0x4CA0` / JP `+0x325C`, then assigns 1 to the **Super Pass item 32-bit saved word**. The paired flag storage is:
- `0x05E`: USA `0x8015C613 & 0x40`, Japan `0x80161E03 & 0x40`.
- `0x000`: USA `0x8015C608 & 0x01`, Japan `0x80161DF8 & 0x01`.
- Super Pass item word: USA `0x8015C700`, Japan `0x80161EF0`, whole 32-bit script assignment. Its editor checkbox targets a low byte at `0x8015C703 / 0x80161EF3`.

The native caller is identified; the player-facing condition that invokes the resource-54 caller is **not** fully resolved. The guard gate setter remains in resource96 events **270 and 272**, with flag `0x001` as previously reported. Those event registrations and script branches are proven; unique direct native actor callers for **270/272** were **not** verified by the bounded literal-call scan. Do not turn a registered event into an assertion about its actual caller.

## 2. Mr. Arrow flag `0x104` is an instantiated pickup parameter in *both* original ROMs

The existing USA room-pickup metadata named `0x104` as an Oedo Castle Mr. Arrow collection bit. This task **independently validated the original Japanese stage and instantiated actor definition**, rather than assuming the same stage number:

| Property | USA | Japan-0 |
| --- | --- | --- |
| Original stage index | **13** | **4** |
| Original room resource ID | 835 (`0x343`) | 835 (`0x343`) |
| Instantiated actor definition | 13 | 13 |
| Actor type (definition first big-endian halfword) | `0x087` (Mr. Arrow) | `0x087` |
| Actor definition bytes `+4..+5` | `0x0104` | `0x0104` |
| Bank-C saved-byte candidate based on original bank helper | `0x8015C628 & 0x10` | `0x80161E18 & 0x10` |

**Proof path:** both authenticated resource-12 stage pointer tables (table offset `0x24060`; region-specific code virtual bases USA `0x8020D2A0`, JP `0x802126CC`) point to valid room metadata; the region-specific metadata points to resource 835; its actor instance groups **actually reference definition 13**, and that exact 16-byte record has the region-equal actor type and flag parameter. Therefore this is **not merely an orphaned ROM record**. It remains proof of scene registration/instantiation data, **not of pickup collection or the native final bit-writing instruction**.

The original resource-77 native call with `a0=0x104` launches **event ID 260**, which is a separate numeric namespace from **saved flag ID 260**. Event260 (resource95) has no literal `0x8020/21/22` saved-bit command in its lexical span. It does contain original 32-bit assignments USA `0x8015C808=13`, `0x8015C828=1`, `0x8015C8E0=0` and Japanese corresponding `0x80161FF8=13`, `0x80162018=1`, `0x801620D0=0`. These are **not** a proof of packed-bit `0x104` set.

### Ten paired pickup actor definitions, full original instance verification

All ten previously USA-catalogued `0x86` (Mr. Elly Fant) and `0x87` (Mr. Arrow) pickup actor **definition records are byte-identical** in Japan and are referenced by original instantiated actor groups in each region. Their **stage IDs are different** and must be paired from their own stage pointer tables, never translated by address arithmetic:

| USA stage → JP stage | Original resource | Actor | Packed event ID |
| --- | --- | --- | --- |
| 9 → 0 | 831 | Elly Fant | `0x0FF` |
| 13 → 4 | 835 | Arrow | `0x104` |
| 52 → 43 | 871 | Elly Fant | `0x100` |
| 57 → 48 | 876 | Arrow | `0x105` |
| 95 → 86 | 900 | Elly Fant | `0x101` |
| 99 → 90 | 904 | Arrow | `0x106` |
| 145 → 235 | 943 | Elly Fant | `0x102` |
| 152 → 242 | 950 | Arrow | `0x107` |
| 174 → 264 | 962 | Elly Fant | `0x103` |
| 182 → 272 | 970 | Arrow | `0x108` |

These region-specific **stage indices** are unrelated to registered **VM event IDs**; e.g., JP stage272 is not event272. Actor definitions are data, not native setter proof.

## 3. Ghost Toys prerequisite bits identified in instantiated actor records

The original stage and room instance walk additionally identified **four `0x195` actor instances**, same 16-byte definition data and same `+4..+5` parameter in both ROMs:

| USA stage → JP stage | Original room file | Actor definition | Big-endian u16 parameter |
| --- | --- | --- | --- |
| 47 → 38 | 866 | 7 | **`0x19A`** |
| 47 → 38 | 866 | 8 | **`0x19B`** |
| 85 → 76 | 893 | 2 | **`0x19A`** |
| 85 → 76 | 893 | 3 | **`0x19B`** |

The values equal the two original bank-C event IDs tested by the resource43 Ghost Toys entrance controller (USA file43 `+0x64AC/+0x64BC`; JP `+0x63D0/+0x63E0`), which sets `0x19C` if both tests pass (USA `+0x64D0`; JP `+0x63F4`). Storage is USA `0x8015C63B` masks `0x04/0x08/0x10`; Japan `0x80161E2B` same masks.

The original native resource60 initializer **clears** `0x19A` and `0x19B` via the regional bank-C clearer (USA `+0x1CE8/+0x1CF8`; JP `+0x1C94/+0x1CA4`). Separately, original file43 callback `+0x1020` reads **actor halfwords `+0xD4` and `+0xD6`** as dynamic saved-event IDs and under its condition calls bank-C setter with actor `+0xD4` (both regions `+0x10C8`). This confirms a **native computed-ID writer mechanism** but does **not** yet prove that type `0x195` initializes its `+0xD4` with the `+4` room parameter or that this specific callback executes for the torch actors. **Actual setter dispatch/activation remains unverified.**

**Important false-positive avoidance:** a room actor of type **`0x08C`** also has field `+4..+5` equal to `0x19A/0x19B/0x19C` in some registered rooms, but `0x08C` is an **exit/entrance actor** whose field is a destination stage/map ID, **not a packed-event flag ID**. The CSV deliberately includes only the fourteen relevant type `0x86/0x87/0x195` definitions; blindly scanning every actor for a numeric halfword would create false flag origins.

## 4. Scanning and test boundaries

- Verified the original 32 MiB decompressed ROM SHA-1 in each region, both original event directories, and exact MIPS/script anchors for event202, the actor-`+0xD4/+0xD6` computed setter, Ghost prerequisite tests/unlock/clearers and event260.
- Walked original resource12 stage pointers, validated room metadata, decoded room instance grids and group pointers, proved all **fourteen** selected original actor definitions are *actually referenced* by the instantiated room groups in **both regions**. Both per-region 16-byte original definition records agree for every row. All stage pairs in the CSV derive from these original two ROMs.
- A bounded aligned script scan found **no literal `0x8020` set pairs for `0x19A/0x19B/0x104`**. That is an absence claim for that one encoding only; dynamic or direct native writes are not excluded.
- Local **16/16 ROM-free host tests PASS** (six original event-directory tests, four focused native/story tests, six room-instantiation guardrails). Authenticated USA/Japan ROM-bound actor trace **PASS**, original paired room instantiation **14/14 PASS**. Read-only source and test bundle available separately; no ROMs/saves/game assets committed.

**Not done:** controlled Japanese gameplay flag-trigger traces, complete dataflow/actor registration from `0x195` constructor to bank-C setter, native pickup object collection callback, definitive NPC/actor callers of events270/272, new IDO matching-C compilation, full 32 MiB G2/ELF inventories, full `decomp.local_ci`. Therefore **no C promotion**; existing accepted baseline still **USA 779 / JP 34**. Next static trace should follow the native `0x195` actor registration handler and pickup actor `0x87` through their configuration copies to the dynamic flag helper, while keeping saved-bit IDs separate from map and VM event IDs.
