#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern M2C_UNK func_08002714_6D8664;

void func_080026C8_6D8618(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_08002714_6D8664);
    }
}
