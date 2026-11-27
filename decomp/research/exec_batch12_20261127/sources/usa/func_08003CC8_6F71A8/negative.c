#include "m2c_types.h"

extern u8 func_8003521C_35E1C[];
extern u8 func_80038B98_39798[];
extern u8 func_8021B73C_5D6C0C[];
extern u8 func_08003D30_6F7210[];

void func_08003CC8_6F71A8(void *arg0, M2C_UNK arg1) {
    if (((s32 (*)(void *, s32))func_8021B73C_5D6C0C)(arg0, 0x41A00000) != 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = M2C_FIELD(arg0, s32 *, 0x60) | 1;
        ((void (*)(s32))func_80038B98_39798)(0x124);
        ((void (*)(u8 *))func_8003521C_35E1C)(func_08003D30_6F7210);
    }

    *(volatile int *)0x80000000 = 1;
}
