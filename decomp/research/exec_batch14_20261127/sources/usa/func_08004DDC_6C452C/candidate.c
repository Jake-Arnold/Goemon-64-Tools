#include "m2c_types.h"

extern u8 func_8003521C_35E1C[];
extern u8 func_8021A26C_5D573C[];
extern u8 func_08004E58_6C45A8[];

void func_08004DDC_6C452C(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, u8 *, 0xDC) += 8;
    ((void (*)(void *, u8, s32, s32, s32))func_8021A26C_5D573C)(arg0, M2C_FIELD(arg0, u8 *, 0xDC), 0, 0, 0xC8);
    if (M2C_FIELD(arg0, u8 *, 0xDC) >= 0xF0) {
        M2C_FIELD(arg0, u8 *, 0xDC) = 0xF0;
        ((void (*)(void *))func_8003521C_35E1C)(func_08004E58_6C45A8);
    }
}
