#include "m2c_types.h"
extern M2C_UNK func_8003521C_35E1C;
extern M2C_UNK func_8021664C_5D1B1C;
extern M2C_UNK func_08003E90_6F7370;

void func_08003E30_6F7310(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        M2C_FIELD(arg0, u32 *, 0x60) = 0x802006E0;
        ((void (*)(void *, s32, s32, s32))&func_8021664C_5D1B1C)(arg0, 2, 0x3DCCCCCD, 0);
        ((void (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_08003E90_6F7370);
    }

    *(volatile s32 *)0x80000000 = 1;
}
