/* Research-only USA VM resource halfword lookup (0x8003F038 / 0x3FC38).
 * Original is 196 MIPS bytes (49 words). Research-only IDO 5.3 -c
 * compiles this to 196 bytes, 25/42 direct matching instruction positions.
 * One volatile signed-half-index declaration is the only structural change
 * from vm_resource_halfword_probe.c; not production/matching-C.
 * Big-endian MIPS recover callback reads the low 16-bit entry half.
 * Host-only table indirection allows signed negative-index tests.
 */
typedef signed int s32;
typedef unsigned int u32;
typedef signed short s16;
typedef unsigned short u16;
#ifndef VM_F038_HOST_TEST
extern s16 D_80077894_78494[];
#define VM_F038_TABLE D_80077894_78494
#else
extern s16 *vm_f038_mock_table;
#define VM_F038_TABLE vm_f038_mock_table
#endif
extern s32 func_800141C4_14DC4(s32);
extern void func_80013B14_14714(u16);
s32 func_8003F038_3FC38(s32 arg, s32 unused) {
    s32 half, out, entry;
    (void)unused;
    if (arg == 0x100) return 0;
    entry = VM_F038_TABLE[half = arg / 2];
    out = func_800141C4_14DC4(entry);
    if (out == -1) func_80013B14_14714((u16)entry);
    out = func_800141C4_14DC4(entry);
    if (out == -1) return 0;
    if (half < 4) out = (s32)((u32)out + (u32)((s32)((u32)arg << 11) / 2));
    return out;
}
