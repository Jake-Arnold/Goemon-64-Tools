# G64-068: stage and room selection trace

## Result

G64-068 is **RESEARCH_ONLY**. The 1,332-byte function at VMA 0x80020F10
(ROM 0x21B10 through 0x22044) is a stage/room selection and display handler.
It updates a group-local selection and a derived intended room ID. It does not
read the 10-byte entrance-record table or establish that a room load succeeds.
The production ownership remains GLOBAL_ASM.

The target bytes are identical in the private USA retail and decompressed ROMs.
The target slice SHA-256 is
4421d83070bb55997b55ce24c6df19f3f8aeae8cdd78ab003c0c5e497724e0ab.

## Dispatch and copied tables

The six-entry function pointer table begins at ROM 0x6DBC8. Its entries are
0x800207AC, 0x80020804, 0x80020964, 0x800209B4, 0x80020C78, and
0x80020F10. Function 0x80020730 copies these entries to its stack, reads the
unsigned byte at SYS_W+0x3ADD6, and dispatches with jalr. The target is
zero-based entry 5. The selector has no visible range guard in this dispatcher;
there is no direct jal reference to 0x80020F10 in the pinned USA assembly.

At entry, 0x80020F10 copies three constant tables to its stack:

| ROM address | Stack destination | Entries | Values |
| --- | --- | ---: | --- |
| 0x6DC88 | sp+0x60 | 11 32-bit pointers | 0x8007BBF8 through 0x8007BC20, stride 4 |
| 0x6DCB4 | sp+0x48 | 12 halfwords | 0, 300, 350, 400, 540, 544, 549, 561, 588, 607, 613, 619 |
| 0x6DCCC | sp+0x30 | 12 halfwords | 300, 50, 50, 140, 4, 5, 12, 27, 19, 6, 5, 1 |

The function reads the group as an unsigned byte from SYS_W+0x3ADE4 and
indexes both halfword tables without a visible group bounds check. The first
halfword table supplies the group base; the second supplies the group limit
used by the selection logic.

## Selection behavior

The function ORs two save-area halfwords, read as unsigned values from
(SYS_W+0x38000)+0x3094 and (SYS_W+0x38000)+0x307C. Bits 0x0100 and 0x0200
decrement or increment the signed word at SYS_W+0x3B048, with bounds at zero
and two. The resulting category selects a movement step of 1, 10, or 100.
For any other category the original code reads a halfword from sp+0x8C without
an earlier initialization in this function; its behavior is unresolved.

The current group-local selection is read as a signed halfword from
SYS_W+0x3ADF4. Input bit 0x0800 subtracts the selected step with 16-bit signed
wrap behavior. If the result is negative, the function loads the current
group's value from the second halfword table. Input bit 0x0400 adds the step;
if that result is not below the group's table value, the selection becomes
zero. The resulting halfword is stored back to SYS_W+0x3ADF4. The function
then adds the group base from the first halfword table and stores the low
halfword to SYS_W+0x3ADF2.

Eight calls to 0x800042AC draw the selection display. The target's body also
contains decimal quotient/remainder calculations and pointer-table indexing.
It does not directly reference D_8006B780, call 0x8000B864, or call a resource
loader. These checks describe this function's instructions only.

## Entrance-record and state-request boundary

At the end of 0x80020F10, input bit 0x4000 writes 2 to SYS_W+0x3ADD6 and the
save-area input halfwords are read again. If their OR has mask 0x9000 set, the
function calls the already matched 0x80021444. This is the boundary between
selection and the existing entrance/state path.

Function 0x80021444 checks D_8006CFBC. If it is not 0xFF, it copies
SYS_W+0x3ADF2 as the intended room ID and SYS_W+0x3ADE4 as the group byte,
then calls 0x800214E4, 0x8000B864, and requests state 0x0B through
0x80003728. If the guard is 0xFF, it skips the record/helper writes but still
requests state 0x0B. This proves a state request, not a complete map unload,
load, or successful room transition.

Function 0x800214E4 is the code that indexes D_8006B780 at ROM 0x6C380. It
uses the unsigned intended room ID and a 10-byte record stride. If any of the
record's x, y, or z signed halfwords is nonzero, it copies x, y, z, heading,
and mode. If all three coordinates are zero, it clears all five destination
halfwords, including heading and mode. The table index is not bounds-checked
in the original instructions.

The existing host fixture in decomp/test_default_entrance.c exercises record
indices 1 and 2, checks the copied fields for index 1, checks the all-zero
coordinate clear for index 2, and verifies neighboring sentinel preservation.
Its AddressSanitizer/UndefinedBehaviorSanitizer run passed. These tests cover
the matched neighbor, not execution of the 0x80020F10 assembly.

## Hypothesis, stop rule, and limits

The falsifiable behavior hypothesis was that 0x80020F10 maintains a local
selection at SYS_W+0x3ADF4, derives SYS_W+0x3ADF2 from a group-base table, and
leaves entrance-record lookup to 0x800214E4 after a guarded 0x80021444 call.
The original dispatch, table accesses, stores, and call sites confirm that
model.

No native C candidate was compiled. Reconstructing this 333-instruction
display handler would require modeling all drawing and decimal-formatting
paths, while the unsupported category path reads uninitialized stack data and
the original group indexing has no bounds guard. There is no narrower
falsifiable whole-function IDO hypothesis in the v2 budget. The first native
mismatch is therefore NOT RUN; no full-ROM G2 build was needed or performed.
Keep the target as GLOBAL_ASM and leave the stored 160-function proof
unchanged. No live-game confirmation was performed.
