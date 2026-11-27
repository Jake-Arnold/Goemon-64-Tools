#include "m2c_types.h"
void func_8003521C_35E1C(M2C_UNK *);
void func_8021664C_5D1B1C(void *, s32, s32, s32);
extern M2C_UNK func_08001600_6C0D50;

void func_08001594_6C0CE4(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, u16 *, 0x8A)--) {
        return;
    }
    M2C_FIELD(arg0, s32 *, 0x60) |= 0x01000000;
    ((void (*)(void *, s32, s32, s32))func_8021664C_5D1B1C)(arg0, 1, 0x3D088889, 0);
    ((void (*)(M2C_UNK *))func_8003521C_35E1C)(&func_08001600_6C0D50);

    *(volatile int *)0x80000000 = 1;
}
