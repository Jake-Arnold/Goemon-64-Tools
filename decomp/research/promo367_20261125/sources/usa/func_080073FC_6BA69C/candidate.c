#include "m2c_types.h"
extern char func_80023E40_24A40;
extern char func_80023E94_24A94;
extern char func_8003521C_35E1C;
extern char func_802197D8_5D4CA8;
M2C_UNK func_08007488_6BA728();                     /* static */
M2C_UNK func_080079B0_6BAC50();                     /* static */

void func_080073FC_6BA69C(s32 arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_80023E40_24A40)(0xB);
    if (((s32(*)())&func_80023E94_24A94)(0xB) != 0) {
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_080079B0_6BAC50);
        return;
    }
    if (((s32(*)())&func_802197D8_5D4CA8)(arg0, 1) == 0) {
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08007488_6BA728);
    }
}
