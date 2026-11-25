#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern M2C_UNK func_0800433C_6FBECC;

void func_080042E8_6FBE78(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_0800433C_6FBECC);
    }
}
