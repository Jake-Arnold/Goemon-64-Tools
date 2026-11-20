#include "../m2c_types.h"
M2C_UNK func_800237A4_243A4(s32);                   /* extern */
s32 osPfsNumFiles(void *, void *, void *);          /* extern */
extern s8 *D_8016E664_16F264;

s32 func_800234B8_240B8(void) {
    s32 sp1C;
    s32 temp_v0;

    temp_v0 = osPfsNumFiles(D_8016E664_16F264, D_8016E664_16F264 + 0x400, D_8016E664_16F264 + 0x404);
    sp1C = temp_v0;
    func_800237A4_243A4(temp_v0);
    M2C_FIELD(D_8016E664_16F264, s32 *, 0x3FC) = sp1C;
    return M2C_FIELD(D_8016E664_16F264, s32 *, 0x3FC);
}
