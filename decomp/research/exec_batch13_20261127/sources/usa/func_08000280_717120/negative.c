#include "m2c_types.h"

extern u8 func_80221C0C_5DD0DC[];
extern u8 func_8003D388_3DF88[];
extern u8 func_8003521C_35E1C[];
extern u8 func_080002FC_71719C[];

void func_08000280_717120(void *arg0, M2C_UNK arg1) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0xEC);
    if (M2C_FIELD(temp_v0, u8 *, 0xCD) == 3) {
        M2C_FIELD(temp_v0, u8 *, 0xCD) = 4;
        ((void (*)(void *, s32, s32, s32))func_80221C0C_5DD0DC)(arg0, 0, 0x3F000000, 1);
        ((void (*)(u16, s32))func_8003D388_3DF88)(M2C_FIELD(arg0, u16 *, 0xA4), 1);
        ((void (*)(void *))func_8003521C_35E1C)(func_080002FC_71719C);
    }

    *(volatile int *)0x80000000 = 1;
}
