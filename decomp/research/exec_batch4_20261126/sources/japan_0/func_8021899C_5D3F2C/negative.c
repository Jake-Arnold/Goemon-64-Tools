#include "m2c_types.h"
void func_80034B44_35744(void);

void func_8021899C_5D3F2C(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s32 *, 0x60) = 0x20;
    if (--M2C_FIELD(arg0, u16 *, 0x8A) == 0) {
        func_80034B44_35744();
    }

    *(volatile s32 *)0x80000000 = 1;
}
