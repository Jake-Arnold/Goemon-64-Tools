#include "m2c_types.h"
extern char func_80023AB0_246B0;
extern char func_80023B54_24754;
extern char func_80034E8C_35A8C;
extern char func_80222718_5DDCA8;
M2C_UNK func_080076C0_6BF440();                     /* static */
M2C_UNK func_0800794C_6BF6CC();                     /* static */

void func_08007630_6BF3B0(s32 arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80023B54_24754)(0xB) != 0) {
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_0800794C_6BF6CC);
        return;
    }
    if (((s32(*)())&func_80222718_5DDCA8)(arg0, 0x360, 1) != 0) {
        ((M2C_UNK(*)())&func_80023AB0_246B0)(8);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080076C0_6BF440);
    }
}
