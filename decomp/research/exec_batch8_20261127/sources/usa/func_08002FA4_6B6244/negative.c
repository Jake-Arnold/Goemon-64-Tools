#include "m2c_types.h"
extern u8 func_8003521C_35E1C[];
extern u8 func_80218D7C_5D424C[];
extern M2C_UNK func_08001D54_6B4FF4;

void func_08002FA4_6B6244(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s32 *, 0x68) &= ~1;
    ((void (*)(void *, s32, s32, s32))func_80218D7C_5D424C)(arg0, 0, 0, 0);
    ((void (*)(M2C_UNK *))func_8003521C_35E1C)(&func_08001D54_6B4FF4);

    *(volatile s32 *)0x80000000 = 1;
}
