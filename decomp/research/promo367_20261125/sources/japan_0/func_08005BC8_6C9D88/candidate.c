#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_80038808_39408;
extern f32 D_08008A54_6CCC14;
extern M2C_UNK func_08005C3C_6C9DFC;

void func_08005BC8_6C9D88(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        if (M2C_FIELD(arg0, u8 *, 0xD4) == 0) {
            ((M2C_UNK(*)())&func_80038808_39408)(0x256, arg0);
        }
        M2C_FIELD(arg0, f32 *, 0x7C) = (f32) D_08008A54_6CCC14;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_08005C3C_6C9DFC, arg0);
    }
}
