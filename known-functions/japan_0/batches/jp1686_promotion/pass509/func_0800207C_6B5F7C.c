#include "m2c_types.h"
extern char func_80023B54_24754;

void func_0800207C_6B5F7C(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80023B54_24754)(2, arg0) != 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = 0x80000200;
        return;
    }
    M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & 0x7FFFFFDF);
}
