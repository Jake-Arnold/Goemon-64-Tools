#include "m2c_types.h"
extern char func_8021B3BC_5D694C;
extern char func_80225CE0_5E1270;

void func_08000CCC_71585C(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;

    ((M2C_UNK(*)())&func_80225CE0_5E1270)();
    temp_v0 = M2C_FIELD(arg0, s32 *, 0x68);
    if (temp_v0 & 0x4000) {
        M2C_FIELD(arg0, s32 *, 0x68) = (s32) (temp_v0 & ~0x4000);
        ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, 0, 0x3E800000, 1);
    }
}
