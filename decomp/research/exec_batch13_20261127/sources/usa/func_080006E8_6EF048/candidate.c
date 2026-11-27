#include "m2c_types.h"

extern u8 func_8003521C_35E1C[];
extern u8 func_8021F1F8_5DA6C8[];
extern u8 func_08000754_6EF0B4[];

void func_080006E8_6EF048(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s16 *, 0xD4) = 2;
    ((void (*)(void *, s32))func_8021F1F8_5DA6C8)(arg0, 0xBFC00000);
    if (--M2C_FIELD(arg0, u16 *, 0x8A) == 0) {
        M2C_FIELD(arg0, u16 *, 0x8A) = 3U;
        ((void (*)(u8 *))func_8003521C_35E1C)(func_08000754_6EF0B4);
    }
}
