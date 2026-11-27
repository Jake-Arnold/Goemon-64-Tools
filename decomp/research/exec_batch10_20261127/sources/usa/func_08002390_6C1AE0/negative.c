#include "m2c_types.h"

void func_8003521C_35E1C(void *);
void func_8022026C_5DB73C(void *, s32, s32, s32);
extern s8 D_8015C562_15D162;
extern M2C_UNK func_080023E4_6C1B34;

void func_08002390_6C1AE0(void *arg0, s32 arg1) {
    void (*fn1)(void *, s32, s32, s32) = func_8022026C_5DB73C;
    void (*fn2)(void *) = func_8003521C_35E1C;

    D_8015C562_15D162 = 1;
    fn1(arg0, 0xFF, 0xFF, 0xFF);
    fn2(&func_080023E4_6C1B34);

    *(volatile s32 *)0x80000000 = 1;
}
