#include "m2c_types.h"
extern char func_80034B44_35744;

void func_08003C48_6FB7D8(s32 arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        ((M2C_UNK(*)())&func_80034B44_35744)();
    }
}
