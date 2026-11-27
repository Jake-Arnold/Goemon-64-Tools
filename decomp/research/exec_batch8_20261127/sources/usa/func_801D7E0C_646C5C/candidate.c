#include "m2c_types.h"
extern f64 D_801EF218_65E068;

void func_801D7E0C_646C5C(void *arg0, s32 arg1) {
    s32 temp_v0;
    s32 var_v1;

    temp_v0 = M2C_FIELD(arg0, s32 *, 0xBC);
    M2C_FIELD(arg0, f32 *, 0x60) += (f32) temp_v0 / 1000.0f;
    temp_v0 += M2C_FIELD(arg0, s32 *, 0xC0);
    var_v1 = (temp_v0 < 0) ? -temp_v0 : temp_v0;
    if (D_801EF218_65E068 <= (f64) var_v1) {
        M2C_FIELD(arg0, s8 *, 0x9C) = 0;
        M2C_FIELD(arg0, s16 *, 0xAA) = 0xF;
    }
    M2C_FIELD(arg0, s32 *, 0xBC) = temp_v0;
}
