#include "m2c_types.h"
extern f64 D_80080B38_81738;

s32 func_80011F10_12B10(s8 *arg0) {
    s32 var_v1;
    s8 *temp_v0;

    var_v1 = 0;
    temp_v0 = arg0 + 0x5C;
    if (D_80080B38_81738 < (f64) M2C_FIELD(arg0, f32 *, 0x7C)) {
        var_v1 = 0x40;
    }
    if (D_80080B38_81738 < (f64) M2C_FIELD(temp_v0, f32 *, 0x40)) {
        var_v1 |= 1;
    }
    if (D_80080B38_81738 < (f64) M2C_FIELD(temp_v0, f32 *, 0x50)) {
        var_v1 |= 2;
    }
    if (D_80080B38_81738 < (f64) M2C_FIELD(temp_v0, f32 *, 0x48)) {
        var_v1 |= 4;
    }
    if (D_80080B38_81738 < (f64) M2C_FIELD(temp_v0, f32 *, 0x58)) {
        var_v1 |= 8;
    }
    if (D_80080B38_81738 < (f64) M2C_FIELD(temp_v0, f32 *, 0x68)) {
        var_v1 |= 0x10;
    }
    if (D_80080B38_81738 < (f64) M2C_FIELD(temp_v0, f32 *, 0x60)) {
        var_v1 |= 0x20;
    }
    return var_v1;
}
