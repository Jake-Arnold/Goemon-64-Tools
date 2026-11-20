#include "../m2c_types.h"
s32 func_80003FD8_4BD8(f32, f32);                   /* extern */

void func_80223D94_68D484(void *arg0, f32 arg1, f32 arg2) {
    M2C_FIELD(arg0, s16 *, 0x98) = (s16) (func_80003FD8_4BD8(arg1 - M2C_FIELD(arg0, f32 *, 0x68), arg2 - M2C_FIELD(arg0, f32 *, 0x80)) & 0x3FF);
}
