#include "m2c_types.h"
M2C_UNK func_801DC064_64A554();                     /* static */

void func_801DB900_649DF0(void *arg0) {
    s32 temp_v1;
    s32 var_v0;

    temp_v1 = M2C_FIELD(arg0, s32 *, 0xB4);
    var_v0 = M2C_FIELD(arg0, s32 *, 0xB0) + temp_v1;
    if ((var_v0 == 0) || ((var_v0 ^ temp_v1) >= 0)) {
        M2C_FIELD(arg0, s8 *, 0xA1) = 3;
        var_v0 = 0;
    }
    M2C_FIELD(arg0, s32 *, 0xB0) = var_v0;
    func_801DC064_64A554();
}
