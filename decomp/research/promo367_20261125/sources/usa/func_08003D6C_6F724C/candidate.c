#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_801FB240_5B7150;
M2C_UNK func_08002254_6F5734();                     /* static */
extern M2C_UNK D_8015CC30_15D830;

void func_08003D6C_6F724C(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, u16 *, 0xDA) != 0) {
        M2C_FIELD(&D_8015CC30_15D830, s32 *, 0xD4) = (s32) (M2C_FIELD(&D_8015CC30_15D830, s32 *, 0xD4) | 1);
        ((M2C_UNK(*)())&func_801FB240_5B7150)();
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08002254_6F5734);
    }
}
