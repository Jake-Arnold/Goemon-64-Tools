#include "m2c_types.h"
extern char func_80218D7C_5D424C;
extern char func_8021927C_5D474C;
extern char func_8021B09C_5D656C;

void func_080012C8_6E85D8(s32 arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        ((M2C_UNK  (*)(s32, M2C_UNK, M2C_UNK, M2C_UNK))&func_80218D7C_5D424C)(arg0, 0, 0, 0);
        ((M2C_UNK (*)(s32))&func_8021927C_5D474C)(arg0);
        ((M2C_UNK (*)(s32, M2C_UNK, M2C_UNK))&func_8021B09C_5D656C)(arg0, 0, 1);
    }

    *(volatile s32 *)0x80000000 = 1;
}
