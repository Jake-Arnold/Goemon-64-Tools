#include "m2c_types.h"
extern M2C_UNK func_8021B09C_5D656C;

void func_08001ED8_6E5EB8(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = temp_v0 - 1;
    if (temp_v0 == 0) {
        M2C_FIELD(arg0, s32 *, 0x60) |= 1;
        ((void (*)(void *, s32, s32))&func_8021B09C_5D656C)(arg0, 0, 1);
    }
}
