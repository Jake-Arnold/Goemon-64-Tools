#include "m2c_types.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *, void *);
M2C_UNK func_80038BC8_397C8(M2C_UNK, void *);
extern M2C_UNK func_08002618_723C38;

void func_080025A8_723BC8(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, s32 *, 0x68) & 0x80) {
        s32 temp_v0 = M2C_FIELD(arg0, s32 *, 0x38);
        if (temp_v0 != 0) {
            M2C_UNK (*fn1)(M2C_UNK, void *) = func_80038BC8_397C8;
            M2C_UNK (*fn2)(M2C_UNK *, void *) = func_8003521C_35E1C;
            fn1(0x24F, arg0);
            M2C_FIELD(arg0, s8 *, 0x8D) = 0x64;
            fn2(&func_08002618_723C38, arg0);
        }
    }

    *(volatile s32 *)0x80000000 = 1;
}
