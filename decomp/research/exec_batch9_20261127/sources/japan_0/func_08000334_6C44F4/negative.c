#include "m2c_types.h"
extern M2C_UNK func_80034E8C_35A8C;
extern M2C_UNK func_8021BB8C_5D711C;
extern M2C_UNK func_080003B0_6C4570;

void func_08000334_6C44F4(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s16 *, 0x5E) = 0x322;
    M2C_FIELD(arg0, u32 *, 0x60) = 0x80000020;
    if (M2C_FIELD(arg0, s32 *, 0xD0) == 1) {
        M2C_FIELD(arg0, u32 *, 0x60) = 0x80000000;
    }
    ((void (*)(void *, s32))&func_8021BB8C_5D711C)(arg0, 0);
    M2C_FIELD(arg0, s8 *, 0x6C) = 0;
    ((void (*)(M2C_UNK *))&func_80034E8C_35A8C)(&func_080003B0_6C4570);

    *(volatile s32 *)0x80000000 = 1;
}
