#include "m2c_types.h"
extern char func_80023E40_24A40;
extern char func_80023E94_24A94;
extern char func_8003521C_35E1C;
M2C_UNK func_080077A4_6BAA44();                     /* static */
M2C_UNK func_080079B0_6BAC50();                     /* static */

void func_08007724_6BA9C4(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80023E94_24A94)(0xB) != 0) {
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_080079B0_6BAC50);
        return;
    }
    ((M2C_UNK(*)())&func_80023E40_24A40)(8);
    M2C_FIELD(arg0, s16 *, 0x8A) = 0x3C;
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_080077A4_6BAA44);
}
