#include "m2c_types.h"
s32 osPfsIsPlug(M2C_UNK *, u8 *);                   /* extern */
extern M2C_UNK D_8016C960_16D560;

s32 func_80023508_24108(void) {
    u8 sp1F;

    if (osPfsIsPlug(&D_8016C960_16D560, &sp1F) == -1) {
        return -1;
    }
    return sp1F & 1;
}
