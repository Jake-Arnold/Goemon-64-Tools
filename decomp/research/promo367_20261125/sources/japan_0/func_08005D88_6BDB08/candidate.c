#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern M2C_UNK func_08005DD8_6BDB58;

void func_08005D88_6BDB08(void *arg0, void *arg1) {
    s32 temp_v0;

    M2C_FIELD(arg1, u16 *, 0x14) = (u16) (M2C_FIELD(arg1, u16 *, 0x14) + 1);
    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        M2C_FIELD(arg0, f32 *, 0xD0) = 0.0f;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_08005DD8_6BDB58);
    }
}
