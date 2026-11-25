#include "m2c_types.h"
extern char func_80034B44_35744;
extern f64 D_08004D68_6E86D8;

void func_080014B4_6E4E24(void *arg0, void *arg1) {
    s32 temp_v0;

    M2C_FIELD(arg1, f32 *, 0x20) = (f32) ((f64) M2C_FIELD(arg1, f32 *, 0x20) + D_08004D68_6E86D8);
    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        ((M2C_UNK(*)())&func_80034B44_35744)();
    }
}
