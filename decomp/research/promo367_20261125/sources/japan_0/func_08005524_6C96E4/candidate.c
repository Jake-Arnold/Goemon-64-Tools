#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern M2C_UNK func_080054AC_6C966C;

void func_08005524_6C96E4(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        M2C_FIELD(arg0, f32 *, 0xDC) = (f32) (M2C_FIELD(arg0, f32 *, 0xDC) + 1.0f);
        if (M2C_FIELD(arg0, f32 *, 0xDC) > 8.0f) {
            M2C_FIELD(arg0, f32 *, 0xDC) = 1.0f;
        }
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_080054AC_6C966C);
    }
}
