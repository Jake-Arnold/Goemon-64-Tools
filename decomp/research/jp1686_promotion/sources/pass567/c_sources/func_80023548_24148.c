#include "../m2c_types.h"
s32 osPfsInitPak(M2C_UNK *, void *, M2C_UNK);       /* extern */
M2C_UNK osPfsRepairId(void *);                      /* extern */
extern M2C_UNK D_8016C960_16D560;
extern void *D_8016E664_16F264;

s32 func_80023548_24148(void) {
    osPfsRepairId(D_8016E664_16F264);
    M2C_FIELD(D_8016E664_16F264, s32 *, 0x3FC) = osPfsInitPak(&D_8016C960_16D560, D_8016E664_16F264, 0);
    return M2C_FIELD(D_8016E664_16F264, s32 *, 0x3FC);
}
