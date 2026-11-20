#include "m2c_types.h"
extern char func_80023B54_24754;
extern char func_80226164_5E16F4;

void func_08000EB8_6B4DB8(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_80226164_5E16F4)();
    if (((s32(*)())&func_80023B54_24754)(2) == 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & 0xEFFFFFFF);
    }
}
