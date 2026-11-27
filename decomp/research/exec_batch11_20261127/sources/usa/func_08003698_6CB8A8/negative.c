#include "m2c_types.h"
extern u8 func_8003521C_35E1C[];
extern u8 func_80038B98_39798[];
extern u8 func_8022026C_5DB73C[];
extern u8 func_080036FC_6CB90C[];

void func_08003698_6CB8A8(void *arg0, M2C_UNK arg1) {
    ((void (*)(void *, s32, s32, s32))func_8022026C_5DB73C)(arg0, 0xFF, 0xFF, 0xFF);
    ((void (*)(s32))func_80038B98_39798)(7);
    M2C_FIELD(arg0, s16 *, 0x8A) = 0;
    ((void (*)(void *))func_8003521C_35E1C)(func_080036FC_6CB90C);

    *(volatile int *)0x80000000 = 1;
}
