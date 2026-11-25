#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_801FB240_5B7150;
extern char func_80220210_5DB6E0;
M2C_UNK func_08004CC0_6F81A0();                     /* static */
extern s8 D_8015C562_15D162;

void func_08004C64_6F8144(M2C_UNK arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80220210_5DB6E0)(arg0, 0x14) == 0) {
        ((M2C_UNK(*)())&func_801FB240_5B7150)();
        D_8015C562_15D162 = 0;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08004CC0_6F81A0);
    }
}
