#include "m2c_types.h"
M2C_UNK func_801E9138_5A5108(s32, M2C_UNK, f32);    /* extern */
s32 func_801ECF10_5A8EE0();                         /* extern */
extern f32 D_80210024_5CBFF4;

void func_801E3A18_59F9E8(s32 arg0, M2C_UNK arg1) {
    f32 var_f0;

    if (func_801ECF10_5A8EE0() != 0) {
        var_f0 = D_80210024_5CBFF4;
    } else {
        var_f0 = 4.0f;
    }
    func_801E9138_5A5108(arg0, 0x21, var_f0);
}
