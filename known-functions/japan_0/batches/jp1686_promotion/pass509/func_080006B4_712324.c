#include "m2c_types.h"
extern char func_80023B54_24754;
extern char func_80034B44_35744;

void func_080006B4_712324(s32 arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80023B54_24754)(1) != 0) {
        ((M2C_UNK(*)())&func_80034B44_35744)();
    }
}
