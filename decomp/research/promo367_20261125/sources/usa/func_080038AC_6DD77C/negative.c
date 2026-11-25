#include "m2c_types.h"
extern char func_08003C40_6DDB10;
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern char func_80218DCC_5D429C;
extern M2C_UNK func_08003944_6DD814;

void func_080038AC_6DD77C(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_v0;

    ((M2C_UNK(*)())&func_08003C40_6DDB10)();
    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & 0xFEFFFFFF);
        ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 4, 0x3E000000, 4);
        ((M2C_UNK(*)())&func_80218DCC_5D429C)(arg0, 5);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_08003944_6DD814);
    }
}
