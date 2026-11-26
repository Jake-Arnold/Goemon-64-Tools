#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80220168_5DB638;
M2C_UNK func_08003A00_6B6CA0();                     /* static */
extern s8 D_8015C562_15D162;

void func_080039B4_6B6C54(M2C_UNK arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80220168_5DB638)(arg0, 0x14) == 0) {
        D_8015C562_15D162 = 0;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08003A00_6B6CA0);
    }
}
