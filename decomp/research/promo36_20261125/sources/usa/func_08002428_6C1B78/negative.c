#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80220168_5DB638;
M2C_UNK func_08002474_6C1BC4();                     /* static */
extern s8 D_8015C562_15D162;

void func_08002428_6C1B78(M2C_UNK arg0, M2C_UNK arg1) {
volatile int negative_control=1;

    if (((s32(*)())&func_80220168_5DB638)(arg0, 0x32) == 0) {
        D_8015C562_15D162 = 0;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08002474_6C1BC4);
    }
}
