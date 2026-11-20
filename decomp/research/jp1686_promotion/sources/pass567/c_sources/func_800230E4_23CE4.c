#include "../m2c_types.h"
M2C_UNK func_800237A4_243A4(s32);                   /* extern */
s32 osPfsFindFile(void *, M2C_UNK, M2C_UNK, M2C_UNK *, M2C_UNK *, void *); /* extern */
extern M2C_UNK D_80072C50_73850;
extern M2C_UNK D_8016E1E0_16EDE0;
extern s8 *D_8016E664_16F264;

s32 func_800230E4_23CE4(void) {
    s32 sp24;
    s32 temp_v0;

    temp_v0 = osPfsFindFile(D_8016E664_16F264, 0x4134, 0x4E47354A, &D_80072C50_73850, &D_8016E1E0_16EDE0, D_8016E664_16F264 + 0x3F0);
    sp24 = temp_v0;
    func_800237A4_243A4(temp_v0);
    M2C_FIELD(D_8016E664_16F264, s32 *, 0x3FC) = sp24;
    return M2C_FIELD(D_8016E664_16F264, s32 *, 0x3FC);
}
