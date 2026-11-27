#include "m2c_types.h"
void func_8003521C_35E1C(void *);
void func_8021664C_5D1B1C(void *, s32, f32, s32);
extern M2C_UNK func_08000208_6E41E8;

void func_080001A8_6E4188(void *arg0, M2C_UNK arg1) {
    ((void (*)(void *, s32, f32, s32))func_8021664C_5D1B1C)(arg0, 0, 1.0f / 3.0f, 1);
    M2C_FIELD(arg0, s32 *, 0x60) = 0x2016E1;
    ((void (*)(void *))func_8003521C_35E1C)(&func_08000208_6E41E8);

    *(volatile int *)0x80000000 = 1;
}
