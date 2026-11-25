#include "m2c_types.h"
extern char func_80023DF0_249F0;
extern char func_80023E94_24A94;
extern char func_8003521C_35E1C;
extern char func_8021D9A8_5D8E78;
M2C_UNK func_08007724_6BA9C4();                     /* static */
M2C_UNK func_080079B0_6BAC50();                     /* static */

void func_08007694_6BA934(s32 arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (((s32(*)())&func_80023E94_24A94)(0xB) != 0) {
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_080079B0_6BAC50);
        return;
    }
    if (((s32(*)())&func_8021D9A8_5D8E78)(arg0, 0x360, 1) != 0) {
        ((M2C_UNK(*)())&func_80023DF0_249F0)(8);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08007724_6BA9C4);
    }
}
