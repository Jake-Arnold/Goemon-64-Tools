#include "m2c_types.h"
void func_80037CB0_388B0(s32, s32);
extern u16 D_800C7AD6_C86D6;

typedef struct {
    s32 unk0;
    s32 unk4;
    s32 unk8;
    s32 unkC;
    s32 unk10;
    s32 unk14;
    s32 unk18;
    s32 unk1C;
} Struct_8016DAF0;

extern Struct_8016DAF0 D_8016DAF0_16E6F0[4];

void func_800379D0_385D0(void) {
    Struct_8016DAF0 *var_s0;
    s32 i;

    if (D_800C7AD6_C86D6 == 0) {
        var_s0 = D_8016DAF0_16E6F0;
        for (i = 0; i < 4; i++, var_s0++) {
            if (var_s0->unk0 != 0) {
                switch (var_s0->unk8) {
                case 0:
                    break;
                case 1:
                    if (var_s0->unk18 & (1 << var_s0->unk1C)) {
                        func_80037CB0_388B0(i, 1);
                    } else {
                        func_80037CB0_388B0(i, 0);
                    }
                    if (var_s0->unk1C != 0) {
                        var_s0->unk1C--;
                    } else {
                        var_s0->unk1C = 0x1F;
                    }
                    if (--var_s0->unk14 < 0 && var_s0->unk0 != 0) {
                        var_s0->unk8 = 2;
                    }
                    break;
                case 3:
                    var_s0->unk0 = 0;
                    /* fallthrough */
                case 2:
                    func_80037CB0_388B0(i, 0);
                    var_s0->unk8 = 0;
                    break;
                }
            }
        }
    }

    *(volatile int *)0x80000000 = 1;
}
