#include "m2c_types.h"
s32 func_80011238_11E38(s32);                       /* extern */

void func_801D295C_664EAC(s32 arg0) {
    s32 temp_a0;
    s32 var_s1;
    s8 *var_s0;

    var_s0 = arg0 + 0x5C;
    var_s1 = 0;
    do {
        temp_a0 = M2C_FIELD(var_s0, s32 *, 0x1C);
        if (temp_a0 != 0) {
            M2C_FIELD(var_s0, s32 *, 0x1C) = func_80011238_11E38(temp_a0);
        }
        var_s1 += 4;
        var_s0 += 4;
    } while (var_s1 != 0x20);
}
