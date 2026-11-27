#include "m2c_types.h"
void func_8003521C_35E1C(M2C_UNK *);
void func_8021664C_5D1B1C(void *, s32, s32, s32);
extern M2C_UNK func_08001DB0_6B5050;

void func_08001D54_6B4FF4(void *arg0, M2C_UNK arg1) {
    ((void (*)(void *, s32, s32, s32))func_8021664C_5D1B1C)(arg0, 0, 0x3E2AAAAB, 1);
    M2C_FIELD(arg0, s16 *, 0x8A) = 0x1E;
    ((void (*)(M2C_UNK *))func_8003521C_35E1C)(&func_08001DB0_6B5050);

    *(volatile int *)0x80000000 = 1;
}
