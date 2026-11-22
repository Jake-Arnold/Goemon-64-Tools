#include "m2c_types.h"
extern f64 D_801F4668_662B58;

void func_801D6128_644618(void *arg0, M2C_UNK arg1) {
    s32 var_v0;

    var_v0 = (s32) ((f64) M2C_FIELD(arg0, s32 *, 0xB4) + D_801F4668_662B58);
    if (var_v0 >= 0x61A8) {
        M2C_FIELD(arg0, s8 *, 0x9D) = 1;
        M2C_FIELD(arg0, s8 *, 0xC4) = 0;
        var_v0 = 0x2710;
    }
    M2C_FIELD(arg0, s32 *, 0xB4) = var_v0;
}
