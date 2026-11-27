#include "m2c_types.h"

extern u8 func_8003521C_35E1C[];
extern u8 func_80038B98_39798[];
extern u8 func_0800551C_6C4C6C[];

void func_080054A4_6C4BF4(void *arg0, void *arg1) {
    M2C_FIELD(arg1, u16 *, 0x18) += 2;
    if (M2C_FIELD(arg1, u16 *, 0x18) >= ((s32)M2C_FIELD(arg0, f32 *, 0xDC) << 7)) {
        M2C_FIELD(arg1, u16 *, 0x18) &= 0x3FF;
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x1E;
        ((void (*)(s32))func_80038B98_39798)(0x2A0);
        ((void (*)(void *))func_8003521C_35E1C)(func_0800551C_6C4C6C);
    }

    *(volatile int *)0x80000000 = 1;
}
