#include "m2c_types.h"

extern u8 func_80034E8C_35A8C[];
extern u8 func_8021BB8C_5D711C[];
extern u8 func_08002388_701B58[];

void func_08002394_701B64(void *arg0, void *arg1) {
    M2C_FIELD(arg0, s32 *, 0x60) = 0x80000221;
    ((void (*)(void *, s32))func_8021BB8C_5D711C)(arg0, 0);
    M2C_FIELD(arg0, s8 *, 0x6C) = 0;
    M2C_FIELD(arg1, f32 *, 0x1C) = 2.0f;
    M2C_FIELD(arg1, f32 *, 0x20) = 2.0f;
    M2C_FIELD(arg1, f32 *, 0x24) = 2.0f;
    ((void (*)(u8 *))func_80034E8C_35A8C)(func_08002388_701B58);
}
