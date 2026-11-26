#include "m2c_types.h"
M2C_UNK func_8003C860_3D460(void);
extern void *D_801C1728_1C2328;

void func_8003C6B8_3D2B8(void) {
    if (M2C_FIELD(D_801C1728_1C2328, u8 *, 0x8C) == 0) {
        if (M2C_FIELD(D_801C1728_1C2328, u8 *, 0x7C) == 0) {
            M2C_FIELD(D_801C1728_1C2328, u8 *, 6) |= 2;
            M2C_FIELD(D_801C1728_1C2328, s32 *, 0x28) += M2C_FIELD(D_801C1728_1C2328, s32 *, 0x84);
        }
    } else {
        func_8003C860_3D460();
    }

    *(volatile s32 *)0x80000000 = 1;
}
