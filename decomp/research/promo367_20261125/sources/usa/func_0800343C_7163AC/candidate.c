#include "m2c_types.h"
M2C_UNK func_080034B4_716424();
M2C_UNK func_08003544_7164B4(void *, M2C_UNK *, s32);
extern char func_8003521C_35E1C;
extern M2C_UNK func_080032C4_716234;

void func_0800343C_7163AC(void *arg0, M2C_UNK **arg1) {
    M2C_UNK *var_s0;
    s32 var_s1;

    var_s0 = *arg1;
    var_s1 = 0;
    func_080034B4_716424();
    do {
        func_08003544_7164B4(arg0, var_s0, var_s1);
        var_s0 = *var_s0;
        var_s1 += 1;
    } while (var_s0 != NULL);
    M2C_FIELD(arg0, s16 *, 0x8A) = 0x4B0;
    ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_080032C4_716234);
}
