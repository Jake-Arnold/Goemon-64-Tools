#include "m2c_types.h"
M2C_UNK func_800237A4_243A4(s32);                   /* extern */
s32 osPfsReadWriteFile(void *, s32, M2C_UNK, s32, s32, s32); /* extern */
extern void *D_8016E664_16F264;

s32 func_800232E4_23EE4(s32 arg0, s32 arg1) {
    s32 sp24;
    s32 temp_v0;

    M2C_FIELD(D_8016E664_16F264, s32 *, 0x3F4) = arg0;
    temp_v0 = osPfsReadWriteFile(D_8016E664_16F264, M2C_FIELD(D_8016E664_16F264, s32 *, 0x3F0), 1, (arg1 * 0x500) + 0x100, 0x500, M2C_FIELD(D_8016E664_16F264, s32 *, 0x3F4));
    sp24 = temp_v0;
    func_800237A4_243A4(temp_v0);
    M2C_FIELD(D_8016E664_16F264, s32 *, 0x3FC) = sp24;
    return M2C_FIELD(D_8016E664_16F264, s32 *, 0x3FC);
}
