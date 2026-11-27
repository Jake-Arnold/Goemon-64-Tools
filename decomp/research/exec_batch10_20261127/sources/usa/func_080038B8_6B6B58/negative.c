#include "m2c_types.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);
M2C_UNK func_8022026C_5DB73C(void *, s32, s32, s32);
extern s8 D_8015C562_15D162;
extern M2C_UNK func_0800390C_6B6BAC;

void func_080038B8_6B6B58(void *arg0, M2C_UNK arg1) {
    M2C_UNK (*fn1)(void *, s32, s32, s32) = func_8022026C_5DB73C;
    M2C_UNK (*fn2)(M2C_UNK *) = func_8003521C_35E1C;
    D_8015C562_15D162 = 1;
    fn1(arg0, 0xFF, 0xFF, 0xFF);
    fn2(&func_0800390C_6B6BAC);

    *(volatile s32 *)0x80000000 = 1;
}
