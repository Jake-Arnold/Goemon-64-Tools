#include "m2c_types.h"

extern u8 func_8003521C_35E1C[];
extern u8 func_80038B98_39798[];
extern u8 func_0800606C_6F954C[];

void func_08006000_6F94E0(void *arg0, s32 arg1) {
    if (M2C_FIELD(arg0, u16 *, 0xDA) != 0) {
        M2C_FIELD(arg0, u32 *, 0x60) |= 1;
        M2C_FIELD(arg0, u32 *, 0x60) &= 0x7FFFFFFF;
        ((void (*)(s32))func_80038B98_39798)(0x15E);
        ((void (*)(void *))func_8003521C_35E1C)(func_0800606C_6F954C);
    }
}
