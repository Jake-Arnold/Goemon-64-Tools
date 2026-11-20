#include "m2c_types.h"
s32 func_8003E684_3F284();                          /* extern */

s32 func_8003E73C_3F33C(void *arg0) {
    s32 temp_v1;

    temp_v1 = func_8003E684_3F284() & 0xFFFF;
    if (temp_v1 & 0x800) {
        if (M2C_FIELD(arg0, s32 *, 8) != 0) {
            return -1;
        }
        goto block_6;
    }
    if ((temp_v1 & 0x400) && (M2C_FIELD(arg0, s32 *, 0xC) != 0)) {
        return 1;
    }
block_6:
    return 0;
}
