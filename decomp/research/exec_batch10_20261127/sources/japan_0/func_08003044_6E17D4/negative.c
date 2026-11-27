#include "m2c_types.h"
M2C_UNK func_8021FE0C_5DB39C(void *, s32, s32);
s32 func_80220874_5DBE04(void *, s32, s32, M2C_UNK);

void func_08003044_6E17D4(void *arg0, M2C_UNK arg1) {
    s32 (*fn1)(void *, s32, s32, M2C_UNK) = func_80220874_5DBE04;
    if (fn1(arg0, M2C_FIELD(arg0, s32 *, 0xDC), M2C_FIELD(arg0, s32 *, 0xE0), 0x3FACCCCD) == 0) {
        M2C_UNK (*fn2)(void *, s32, s32) = func_8021FE0C_5DB39C;
        fn2(arg0, 0, 1);
    }

    *(volatile s32 *)0x80000000 = 1;
}
