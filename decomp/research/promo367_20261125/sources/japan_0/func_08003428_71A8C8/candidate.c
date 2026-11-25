#include "m2c_types.h"
M2C_UNK func_080034A0_71A940();
M2C_UNK func_08003530_71A9D0(void *, M2C_UNK *, s32);
extern char func_80034E8C_35A8C;
extern M2C_UNK func_080032C0_71A760;

void func_08003428_71A8C8(void *arg0, M2C_UNK **arg1) {
    M2C_UNK *var_s0;
    s32 var_s1;

    var_s0 = *arg1;
    var_s1 = 0;
    func_080034A0_71A940();
    do {
        func_08003530_71A9D0(arg0, var_s0, var_s1);
        var_s0 = *var_s0;
        var_s1 += 1;
    } while (var_s0 != NULL);
    M2C_FIELD(arg0, s16 *, 0x8A) = 0x4B0;
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_080032C0_71A760);
}
