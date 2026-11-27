#include "m2c_types.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);
M2C_UNK func_8021664C_5D1B1C(void *, s32, M2C_UNK, s32);
extern f32 D_8015CDD0;
extern M2C_UNK func_08005CC0_6B8F60;

void func_08005C68_6B8F08(void *arg0, M2C_UNK arg1) {
    M2C_UNK (*fn1)(void *, s32, M2C_UNK, s32) = func_8021664C_5D1B1C;
    M2C_UNK (*fn2)(M2C_UNK *) = func_8003521C_35E1C;
    fn1(arg0, (s32) D_8015CDD0, 0x3E2AAAAB, 1);
    fn2(&func_08005CC0_6B8F60);

    *(volatile s32 *)0x80000000 = 1;
}
