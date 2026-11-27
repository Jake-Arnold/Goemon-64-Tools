#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK *, void *);
M2C_UNK func_80038838_39438(M2C_UNK, void *);
extern M2C_UNK func_08002620_728050;

void func_080025B0_727FE0(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, s32 *, 0x68) & 0x80) {
        s32 temp_v0 = M2C_FIELD(arg0, s32 *, 0x38);
        if (temp_v0 != 0) {
            M2C_UNK (*fn1)(M2C_UNK, void *) = func_80038838_39438;
            M2C_UNK (*fn2)(M2C_UNK *, void *) = func_80034E8C_35A8C;
            fn1(0x24F, arg0);
            M2C_FIELD(arg0, s8 *, 0x8D) = 0x64;
            fn2(&func_08002620_728050, arg0);
        }
    }

    *(volatile s32 *)0x80000000 = 1;
}
