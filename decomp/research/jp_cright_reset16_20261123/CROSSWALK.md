# Japan/USA fixed system-pointer slot — original ROM crosswalk

The original Japan-0 `func_80004170_4D70` loads a 32-bit pointer from guest `0x80161DB8` (named `g_system_ptr` in pinned `mnsg` Japanese symbol map). The original USA NG5E-0 `func_80004170_4D70` is a different function; at ROM `0x4D8C..0x4D9C`, it forms guest `0x8015C5C8` and writes a pointer there. `decomp/system_memory.c` names the latter `D_8015C5C8_15D1C8`. Both original 16 MiB retail ROMs are authenticated by SHA-1 before decoder inspection; the candidate slots are independently decoded from instruction operands. Their difference is `+0x57F0` exactly.

**Evidence level:** fixed guest-global pointer **slot** address and access width are original-instruction verified in both regions; semantic equivalence of the dereferenced game-state layouts, runtime value in a particular scene, and write safety are not established. The Japan reset routine's `g_system_ptr + 0x3B168` is a **dynamic pointer-relative byte field**; do not reinterpret it as a fixed guest RAM address or apply `+0x57F0` to it. The named function address `0x80004170` is the same in both regions but their instructions and functions differ. No toolkit memory write is authorized.

To reproduce using the user's authentic ROM images (none bundled):

```bash
python3 verify_rom_pointer_slots.py --usa-rom /PRIVATE/USA.z64 --japan-rom /PRIVATE/Japan-normalized.z64 --report /tmp/original_rom_pointer_proof.json
python3 -m unittest discover -s . -p 'test_rom_pointer_slots.py' -v
```

Results: both 16 MiB ROM SHA-1 identities exact, both instruction sequences decode as described; cross-region slot delta `0x57F0`, five host tests passed. The proof JSON retains only addresses/hashes/semantics, never raw MIPS instruction words, ROM bytes or private memory contents.
