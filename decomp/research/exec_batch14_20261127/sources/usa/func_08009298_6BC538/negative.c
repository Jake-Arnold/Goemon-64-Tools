#include "m2c_types.h"

extern u8 func_800240DC_24CDC[];
extern u8 func_8003521C_35E1C[];
extern s32 D_8015C5C8_15D1C8;
extern u8 D_CF8E8[];
extern u8 func_0800930C_6BC5AC[];

void func_08009298_6BC538(void *arg0, M2C_UNK arg1) {
    if (((s32 (*)(s32))func_800240DC_24CDC)(0x12E) != 0) {
        M2C_FIELD(arg0, s8 *, 0xDD) = 0x38;
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x5A;
        M2C_FIELD(*(void **)(D_CF8E8 + D_8015C5C8_15D1C8), s16 *, 0x22) = 0;
        ((void (*)(void *))func_8003521C_35E1C)(func_0800930C_6BC5AC);
    }

    *(volatile int *)0x80000000 = 1;
}
