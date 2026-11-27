#include "m2c_types.h"
s32 func_801D33D8_5FE7B8(s32, s32, u8, u8);

s32 func_801D35B0_5FE990(void *arg0, s32 arg1, u8 arg2, u8 arg3) {
    if (arg0 == NULL) {
        return 0;
    }
    return func_801D33D8_5FE7B8(M2C_FIELD(arg0, s32 *, 0x18), arg1, arg2, arg3);
}
