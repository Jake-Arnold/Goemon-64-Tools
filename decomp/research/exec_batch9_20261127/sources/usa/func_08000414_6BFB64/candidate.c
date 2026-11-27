#include "m2c_types.h"
extern M2C_UNK func_8003521C_35E1C;
extern M2C_UNK func_80216E1C_5D22EC;
extern M2C_UNK func_080003B0_6BFB00;

void func_08000414_6BFB64(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s16 *, 0x5E) = 0x33B;
    M2C_FIELD(arg0, u32 *, 0x60) = 0x80000020;
    if (M2C_FIELD(arg0, s32 *, 0xD0) == 1) {
        M2C_FIELD(arg0, u32 *, 0x60) = 0x80000000;
    }
    ((void (*)(void *, s32))&func_80216E1C_5D22EC)(arg0, 0);
    M2C_FIELD(arg0, s8 *, 0x6C) = 0;
    ((void (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_080003B0_6BFB00);
}
