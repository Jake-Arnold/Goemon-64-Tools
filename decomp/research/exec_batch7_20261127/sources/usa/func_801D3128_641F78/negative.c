#include "m2c_types.h"
extern f64 D_801EF058_65DEA8;

void func_801D3128_641F78(void *arg0, M2C_UNK arg1) {
    s32 var_v0;
    s32 var_v1;

    var_v0 = M2C_FIELD(arg0, s32 *, 0xA0);
    M2C_FIELD(arg0, f32 *, 0x64) += (f32) var_v0 / 1000.0f;
    var_v0 += M2C_FIELD(arg0, s32 *, 0xA4);
    if (var_v0 < 0) {
        var_v1 = -var_v0;
    } else {
        var_v1 = var_v0;
    }
    if (D_801EF058_65DEA8 <= (f64) var_v1) {
        M2C_FIELD(arg0, s8 *, 0x9C) = 1;
    }
    M2C_FIELD(arg0, s32 *, 0xA0) = var_v0;

    *(volatile s32 *)0x80000000 = 1;
}
