#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);
M2C_UNK func_80038808_39408(s32);
M2C_UNK func_80224FDC_5E056C(void *, s32, s32, s32);
extern M2C_UNK func_080072D4_6BF054;

void func_0800727C_6BEFFC(void *arg0, M2C_UNK arg1) {
    M2C_UNK (*fn1)(void *, s32, s32, s32) = func_80224FDC_5E056C;
    M2C_UNK (*fn2)(s32) = func_80038808_39408;
    M2C_UNK (*fn3)(M2C_UNK *) = func_80034E8C_35A8C;
    fn1(arg0, 0xFF, 0xFF, 0xFF);
    fn2(0x301);
    fn3(&func_080072D4_6BF054);

    *(volatile s32 *)0x80000000 = 1;
}
