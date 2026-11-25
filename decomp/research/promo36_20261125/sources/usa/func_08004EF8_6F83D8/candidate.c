#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_801FA420_5B6330;
extern char func_80220210_5DB6E0;
M2C_UNK func_08004F74_6F8454();                     /* static */
extern s8 D_8015C562_15D162;

void func_08004EF8_6F83D8(M2C_UNK arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80220210_5DB6E0)(arg0, 0x14) == 0) {
        ((M2C_UNK(*)())&func_801FA420_5B6330)(0x139, 0x50, 0x50, 0xFA, 0, 0x50, 0x200);
        D_8015C562_15D162 = 0;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08004F74_6F8454);
    }
}
