#include "m2c_types.h"
M2C_UNK func_801E9138_5A5108(s32, M2C_UNK, f32);    /* extern */
s32 func_801ECF10_5A8EE0();                         /* extern */
extern f32 D_8021001C_5CBFEC;

void func_801E3950_59F920(s32 arg0, M2C_UNK arg1) {
    f32 var_f0;

    if (func_801ECF10_5A8EE0() != 0) {
        var_f0 = D_8021001C_5CBFEC;
    } else {
        var_f0 = 2.0f;
    }
    func_801E9138_5A5108(arg0, 0x1E, var_f0);
}
