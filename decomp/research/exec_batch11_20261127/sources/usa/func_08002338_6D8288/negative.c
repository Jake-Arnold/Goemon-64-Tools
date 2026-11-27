#include "m2c_types.h"
extern u8 func_8003521C_35E1C[];
extern u8 func_8021BC04_5D70D4[];
extern u8 func_08002398_6D82E8[];

void func_08002338_6D8288(void *arg0, M2C_UNK arg1) {
    ((void (*)(void *, s32, s32))func_8021BC04_5D70D4)(arg0, 0x3D4CCCCD, 0x41000000);
    if (M2C_FIELD(arg0, u16 *, 0x8A)--) {
    } else {
        ((void (*)(void *))func_8003521C_35E1C)(func_08002398_6D82E8);
    }

    *(volatile int *)0x80000000 = 1;
}
