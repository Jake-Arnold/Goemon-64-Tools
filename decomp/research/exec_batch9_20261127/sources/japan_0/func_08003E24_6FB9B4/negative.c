#include "m2c_types.h"
extern M2C_UNK func_80034E8C_35A8C;
extern M2C_UNK func_8021B3BC_5D694C;
extern M2C_UNK func_08003E84_6FBA14;

void func_08003E24_6FB9B4(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        M2C_FIELD(arg0, u32 *, 0x60) = 0x802006E0;
        ((void (*)(void *, s32, s32, s32))&func_8021B3BC_5D694C)(arg0, 2, 0x3DCCCCCD, 0);
        ((void (*)(M2C_UNK *))&func_80034E8C_35A8C)(&func_08003E84_6FBA14);
    }

    *(volatile s32 *)0x80000000 = 1;
}
