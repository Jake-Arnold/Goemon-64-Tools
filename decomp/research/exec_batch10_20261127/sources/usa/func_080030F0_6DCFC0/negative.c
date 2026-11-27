#include "m2c_types.h"
M2C_UNK func_8021B09C_5D656C(void *, s32, s32);
s32 func_8021BB04_5D6FD4(void *, s32, s32, M2C_UNK);

void func_080030F0_6DCFC0(void *arg0, M2C_UNK arg1) {
    s32 (*fn1)(void *, s32, s32, M2C_UNK) = func_8021BB04_5D6FD4;
    if (fn1(arg0, M2C_FIELD(arg0, s32 *, 0xDC), M2C_FIELD(arg0, s32 *, 0xE0), 0x3FACCCCD) == 0) {
        M2C_UNK (*fn2)(void *, s32, s32) = func_8021B09C_5D656C;
        fn2(arg0, 0, 1);
    }

    *(volatile s32 *)0x80000000 = 1;
}
