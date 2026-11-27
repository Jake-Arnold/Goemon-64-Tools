#include "m2c_types.h"

extern u8 func_8003521C_35E1C[];
extern u8 func_80038B98_39798[];
extern u8 func_8022026C_5DB73C[];
extern s8 D_8015C562_15D162;
extern u8 func_08008280_6BB520[];

void func_0800820C_6BB4AC(void *arg0, s32 arg1) {
    ((void (*)(void *, s32, s32, s32))func_8022026C_5DB73C)(arg0, 0xFF, 0xFF, 0xFF);
    ((void (*)(s32))func_80038B98_39798)(7);
    M2C_FIELD(arg0, s16 *, 0x8A) = 0x1E;
    D_8015C562_15D162 = 1;
    ((void (*)(void *))func_8003521C_35E1C)(func_08008280_6BB520);
}
