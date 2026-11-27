#include "m2c_types.h"
extern f64 D_801EF0F0_65DF40;

void func_801D4C14_643A64(void *arg0, s32 arg1) {
    s32 temp_v0;
    s32 var_v1;

    temp_v0 = M2C_FIELD(arg0, s32 *, 0xA0);
    M2C_FIELD(arg0, f32 *, 0x60) += (f32) temp_v0 / 1000.0f;
    temp_v0 += M2C_FIELD(arg0, s32 *, 0xA4);
    var_v1 = (temp_v0 < 0) ? -temp_v0 : temp_v0;
    if (D_801EF0F0_65DF40 <= (f64) var_v1) {
        M2C_FIELD(arg0, s8 *, 0x9C) = 0;
        M2C_FIELD(arg0, s16 *, 0xA8) = 0xF;
    }
    M2C_FIELD(arg0, s32 *, 0xA0) = temp_v0;

    *(volatile s32 *)0x80000000 = 1;
}
