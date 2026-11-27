#include "m2c_types.h"

extern u8 func_8003521C_35E1C[];
extern u8 func_8021664C_5D1B1C[];
extern u8 func_08000898_6E4878[];

void func_08000838_6E4818(void *arg0, s32 arg1) {
    ((void (*)(void *, s32, s32, s32))func_8021664C_5D1B1C)(arg0, 0, 0x3EAAAAAB, 1);
    M2C_FIELD(arg0, s32 *, 0x60) = 0x2016E1;
    ((void (*)(void *))func_8003521C_35E1C)(func_08000898_6E4878);
}
