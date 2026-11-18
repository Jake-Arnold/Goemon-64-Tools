# Japanese actor → Object → graphics trace (read-only research)

**Scope:** Original Japanese rev-0, map `0x0003`, actor type `0x00FB`. This is a *capture format and correlator*, not an automatic emulator debugger, live graphics logger, or proof of a model file. Keep original ROMs, memory snapshots and any screenshots private. Only publish metadata, reproducible address derivations and redacted outcomes.

## Verified original-ROM breakpoints

| Site | Japan rev-0 guest address | Evidence | Register to record |
| --- | --- | --- | --- |
| Generic actor loader entry | `0x8021DE00` | Original JP file-12 MIPS store to `ActorTask.model_id` at function `+0x6C` | — |
| **After** the `model_id` store | **`0x8021DE70`** | `sh t1, +0x5E(s0)` has completed at the following instruction | `s0` = `ActorTask*` |
| Object graphics dispatch candidate | **`0x800167D4`** | Original JP ROM `0x173D4`, unique 32-byte prefix identical to original USA `0x80016C44` at ROM `0x17844`; both use `+0x64(Object*)` and `+0x2C(Object*)` | `a0` = candidate `Object*` |

Original USA 16-MiB SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`; normalised original Japanese rev-0 16-MiB SHA-1 `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b`. Unique shared 32-byte dispatcher prefix SHA-256 `19610a93d82b2dc8fe65fe19f2eb7bc8b0af52dc7f9526910f4358bf31ec2688`. JP main code maps guest VMA = ROM offset + `0x7FFFF400`. This establishes a strong *counterpart candidate*, not a full Japan recompilation-build proof.

`ActorTask` source layout: `Task.heap_element +0x18`, `actor_id +0x5C`, `model_id +0x5E`; the two ID stores were independently verified in original Japanese MIPS. The Task heap pointer and `Object` layout were found in `Jake-Arnold/Goemon64Recomp/patches/types.h`; the complete Japanese runtime field mapping still requires a genuine paired memory capture. Original JP graphics dispatcher loads from `+0x2C`, supporting that one particular Object offset independently. Do **not** assume `model_id=0x00FB` means ROM file `0x00FB`.

## Capture sequence

1. In original-JP debugger, enter map `0x0003` and break at `0x8021DE70`. When `s0+0x5C` is `0x00FB`, record the **actual** aligned `s0` value, a frame counter, and exactly `0x60` bytes starting at `s0` in a private JSON `actor` event. Mark `pc=0x8021DE70`.
2. Break at `0x800167D4`. Compare its **actual** `a0` argument against the candidate object pointer at the saved actor header `+0x18`. For a matching draw, record `0x68` bytes from `a0`, and resample the actor's current `0x60` bytes at the *saved `s0` pointer*, both while paused on the same numbered frame. Mark the resampled actor event `pc=0x800167D4`. The debugger `s0` **at the draw breakpoint** must not be substituted for the saved actor pointer.
3. The correlator requires one initializer anchor, a same-frame actor sample, and pointer equality. It rejects task reuse/rebinding evidence and does not follow any pointers or read guest memory itself. As long as an object association is missing, report it as **unmatched**.
4. For visible face flicker, independently hash the *actual submitted* guest GBI commands, matrix payloads, texture state and framebuffer in adjacent GOOD/BAD frames. Only fill the optional frame-digest records when those captures genuinely exist. The tool will not generate the hashes or sample RT64 calls; matching the three guest digests only narrows the hypothesis to uncaptured renderer state or interpolation.

## Private JSON format (all bytes are synthetic placeholders)

```json
{
  "schema": "goemon-japan-0-actor-model-trace-v1",
  "region": "japan_0",
  "map_id": 3,
  "captures": [
    {
      "kind": "actor", "frame": 100, "pc": "0x8021DE70",
      "actor_ptr": "0x80150000", "header_hex": "<exactly 120 hex characters from 0x60 actual bytes>"
    },
    {
      "kind": "actor", "frame": 101, "pc": "0x800167D4",
      "actor_ptr": "0x80150000", "header_hex": "<fresh 0x60 bytes from saved actor pointer>"
    },
    {
      "kind": "draw", "frame": 101, "pc": "0x800167D4",
      "a0": "0x80300000", "header_hex": "<exactly 208 hex characters from 0x68 actual bytes>"
    }
  ]
}
```

Angle-bracket placeholder strings above are **not parseable input**; replace them with actual private captures. Use:

```bash
python3 -m practice.actor_model_trace /private/path/japan-actor-trace.json
python3 -m unittest tests.test_actor_model_trace -v
```

Output consists of pointer/ID/graphics metadata, explicit correlation status and limitations. No raw header bytes are included in the report. The tool never writes a capture, ROM, model, texture, binary or screenshot.

## Evidence status / next integration point

- Confirmed: original-JP loader stores at `+0x5C/+0x5E`; map 3 contains three static placements of actor `0x00FB`; Japanese renderer entry candidate independently located with 32 identical bytes and matching `+0x2C` load.
- Pending: paired runtime pointer equality, whether actor-specific code changes `model_id`, graphics/overlay pointer validation, segmented resource mapping, emitted F3DEX command traces, RT64 matrix-group/texture/state capture and actual GOOD/BAD screenshots.
- Do not merge a visual fix, assert a full NPC model or map `0x00FB` to ROM file 0xFB based on this script alone.