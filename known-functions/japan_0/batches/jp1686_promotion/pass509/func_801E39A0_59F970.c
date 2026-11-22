#include "m2c_types.h"
M2C_UNK func_801E9138_5A5108(s32, M2C_UNK, f32);    /* extern */
s32 func_801ECF10_5A8EE0();                         /* extern */
extern f32 D_80210020_5CBFF0;

void func_801E39A0_59F970(s32 arg0, M2C_UNK arg1) {
    f32 var_f0;

    if (func_801ECF10_5A8EE0() != 0) {
        var_f0 = D_80210020_5CBFF0;
    } else {
        var_f0 = 1.0f;
    }
    func_801E9138_5A5108(arg0, 0x1F, var_f0);
}
