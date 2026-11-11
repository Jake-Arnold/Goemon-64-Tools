/* Research-only USA VM resource loader, original 0x8003D468 / 0x3E068.
 * This draft deliberately keeps the resource record and VM work separate.
 * Pinned IDO 5.3 -O2 -mips2 -G 0 -non_shared output assembles to 556 bytes
 * versus 548 original; 24-byte stack frame versus original 32. UNPROMOTED.
 * No matching-C claim until an independent full ROM proves identity.
 */
#include "../vm_resource_types.h"

typedef struct {
    s32 value;       /* +0: cleared by the initializer */
    s32 unknown_04;  /* +4: width observed; meaning unknown */
    s16 marker;      /* +8: halfword initialized to -1 */
    u16 gate;        /* +0xA: halfword cleared */
    s32 unknown_0C;  /* +0xC: word cleared */
    s32 unknown_10;  /* +0x10: width observed; meaning unknown */
    s32 loaded;      /* +0x14: resource base/result word */
} VmWorkLoader;
extern void *D_80077860_78460;
extern s32 D_8007785C_7845C;
extern s32 D_80077858_78458;
extern VmResourceContext D_801C78E8_1C84E8;
extern VmWorkLoader D_801C77E8_1C83E8;
extern s32 D_801C7900_1C8500,D_801C7904_1C8504;
extern s32 D_801C7740_1C8340,D_801C7744_1C8344,D_801C7748_1C8348,D_801C774C_1C834C;
extern s32 D_801C7750_1C8350,D_801C7754_1C8354,D_801C7758_1C8358,D_801C775C_1C835C;
extern s32 D_801C7760_1C8360,D_801C7764_1C8364,D_801C7768_1C8368,D_801C776C_1C836C;
extern s32 D_801C7770_1C8370,D_801C7774_1C8374,D_801C7798_1C8398,D_801C77A0_1C83A0;
extern s32 D_801C77D8_1C83D8,D_801C77E0_1C83E0;
extern s32 D_801C78D0_1C84D0,D_801C78FC_1C84FC;
extern s32 D_801C7920_1C8520,D_801C7924_1C8524,D_801C7928_1C8528,D_801C792C_1C852C;
extern s32 func_800141C4_14DC4(s32);
extern void func_80013B14_14714(u16);
extern void func_8003CFA0_3DBA0(s32);
extern s32 func_80001E50_2A50(s32);
extern s32 func_8003DDC4_3E9C4(s32,s32);
extern s32 func_8003DE48_3EA48(s32);
extern void func_80024088_24C88(s32);

s32 func_8003D468_3E068(s32 start, s32 entry_resource_id) {
    VmResourceContext *resource;
    VmWorkLoader *work;
    s32 result;
    if (D_80077860_78460 == 0) return 0;
    resource = &D_801C78E8_1C84E8;
    resource->current_id.word = entry_resource_id;
    if (entry_resource_id != -1) {
        work = &D_801C77E8_1C83E8;
        result = func_800141C4_14DC4(entry_resource_id);
        work->loaded = result;
        if (result == -1) {
            func_80013B14_14714(VM_RESOURCE_ID_LOW_HALF(resource->current_id));
            func_8003CFA0_3DBA0(resource->current_id.word);
            result = func_800141C4_14DC4(resource->current_id.word);
            work->loaded = result;
        }
        work->loaded = result & 0xBFFFFFFF;
        resource->unknown_04 = func_80001E50_2A50(resource->current_id.word);
        resource->unknown_08 = func_8003DDC4_3E9C4(start, entry_resource_id) - start;
        D_80077858_78458 = func_8003DE48_3EA48(start);
    } else {
        work = &D_801C77E8_1C83E8;
        work->loaded = 0;
        resource->unknown_04 = 0;
        resource->unknown_08 = 0;
        D_80077858_78458 = 0;
        D_801C7900_1C8500 = 3;
        D_801C7904_1C8504 = -1;
    }
    D_801C7740_1C8340 = 0;
    D_801C7744_1C8344 = 0;
    D_801C7748_1C8348 = 0;
    D_801C774C_1C834C = 0;
    D_801C7750_1C8350 = 0;
    D_801C7754_1C8354 = 0;
    D_801C7758_1C8358 = 0x18;
    D_801C775C_1C835C = 0x18;
    D_801C7760_1C8360 = 0x18;
    D_801C7764_1C8364 = 0x18;
    D_801C7768_1C8368 = 0;
    D_801C776C_1C836C = 0;
    D_801C7770_1C8370 = 0;
    D_801C7774_1C8374 = 0;
    D_801C7798_1C8398 = 1;
    D_801C77A0_1C83A0 = 0;
    D_801C77D8_1C83D8 = 1;
    D_801C77E0_1C83E0 = 0;
    work->value = 0;
    work->marker = -1;
    D_801C78D0_1C84D0 = 0;
    work->unknown_0C = 0;
    *(u8 *)&D_801C78FC_1C84FC = 0;
    work->gate = 0;
    D_801C7920_1C8520 = 0;
    D_801C7924_1C8524 = 0;
    D_801C7928_1C8528 = 0;
    D_801C792C_1C852C = 0;
    func_80024088_24C88(0x82);
    D_8007785C_7845C = 0x100;
    ((u8 *)D_80077860_78460)[0x5c] = 0;
    ((u8 *)D_80077860_78460)[0x5d] = 0;
    return 1;
}
