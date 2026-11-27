#include "m2c_types.h"
extern f64 D_801F4850_662D40;

void func_801DA9C0_648EB0(void *arg0, M2C_UNK arg1) {
    s32 var_v0;
    s32 var_v1;

    var_v0 = M2C_FIELD(arg0, s32 *, 0xAC);
    M2C_FIELD(arg0, f32 *, 0xA8) = (f32) (M2C_FIELD(arg0, f32 *, 0xA8) + ((f32) var_v0 / 1000.0f));
    if ((M2C_FIELD(arg0, s16 *, 0xBA) | var_v0) != 0) {
        var_v0 += M2C_FIELD(arg0, s32 *, 0xB0);
    } else {
        M2C_FIELD(arg0, s16 *, 0xBA) = 5;
    }
    if (var_v0 < 0) {
        var_v1 = -var_v0;
    } else {
        var_v1 = var_v0;
    }
    if (D_801F4850_662D40 <= (f64) var_v1) {
        M2C_FIELD(arg0, s8 *, 0x9D) = 0;
    }
    M2C_FIELD(arg0, s32 *, 0xAC) = var_v0;

    *(volatile s32 *)0x80000000 = 1;
}
