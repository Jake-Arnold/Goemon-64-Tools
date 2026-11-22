#include "m2c_types.h"
extern char func_80023B54_24754;

void func_08002C98_73B7D8(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80023B54_24754)(0) != 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 2);
    }
}
