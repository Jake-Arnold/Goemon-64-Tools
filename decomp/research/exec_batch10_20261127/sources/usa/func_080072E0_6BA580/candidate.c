#include "m2c_types.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);
M2C_UNK func_80038B98_39798(s32);
M2C_UNK func_8022026C_5DB73C(void *, s32, s32, s32);
extern M2C_UNK func_08007338_6BA5D8;

void func_080072E0_6BA580(void *arg0, M2C_UNK arg1) {
    M2C_UNK (*fn1)(void *, s32, s32, s32) = func_8022026C_5DB73C;
    M2C_UNK (*fn2)(s32) = func_80038B98_39798;
    M2C_UNK (*fn3)(M2C_UNK *) = func_8003521C_35E1C;
    fn1(arg0, 0xFF, 0xFF, 0xFF);
    fn2(0x301);
    fn3(&func_08007338_6BA5D8);
}
