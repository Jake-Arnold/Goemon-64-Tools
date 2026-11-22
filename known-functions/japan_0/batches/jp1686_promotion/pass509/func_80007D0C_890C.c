#include "m2c_types.h"
M2C_UNK func_80007D50_8950(s32);                    /* extern */

void func_80007D0C_890C(void) {
    s16 var_s0;

    var_s0 = 0;
    do {
        func_80007D50_8950(var_s0 & 0xFFFF);
        var_s0 += 1;
    } while (var_s0 < 0x10);
}
