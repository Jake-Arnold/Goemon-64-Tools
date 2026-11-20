#include "m2c_types.h"
M2C_UNK func_800100A0_10CA0(s32);                   /* extern */

void func_800100D8_10CD8(void) {
    s32 var_s0;

    var_s0 = 0;
    do {
        func_800100A0_10CA0(var_s0);
        var_s0 += 1;
    } while (var_s0 != 0x28);
}
