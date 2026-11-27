#include "m2c_types.h"

extern u8 func_8003521C_35E1C[];
extern u8 func_80216E1C_5D22EC[];
extern u8 func_08002388_6FD588[];

void func_08002394_6FD594(void *arg0, void *arg1) {
    M2C_FIELD(arg0, s32 *, 0x60) = 0x80000221;
    ((void (*)(void *, s32))func_80216E1C_5D22EC)(arg0, 0);
    M2C_FIELD(arg0, s8 *, 0x6C) = 0;
    M2C_FIELD(arg1, f32 *, 0x1C) = 2.0f;
    M2C_FIELD(arg1, f32 *, 0x20) = 2.0f;
    M2C_FIELD(arg1, f32 *, 0x24) = 2.0f;
    ((void (*)(u8 *))func_8003521C_35E1C)(func_08002388_6FD588);

    *(volatile int *)0x80000000 = 1;
}
