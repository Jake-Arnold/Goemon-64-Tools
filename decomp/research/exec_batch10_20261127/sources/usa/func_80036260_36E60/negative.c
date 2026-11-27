#include "m2c_types.h"
s32 func_80035FDC_36BDC(s32);
void func_80036308_36F08(s32);

s32 func_80036260_36E60(void *arg0) {
    s32 var_s0;

    if (M2C_FIELD(arg0, s32 *, 0x18) == 0) {
        return 0;
    }
    var_s0 = M2C_FIELD(arg0, s32 *, 0x18);
    while (var_s0 != 0) {
        M2C_FIELD(arg0, s32 *, 0x18) = func_80035FDC_36BDC(var_s0);
        if (M2C_FIELD(arg0, s32 *, 0x18) == 0) {
            M2C_FIELD(arg0, s32 *, 0x1C) = 0;
            func_80036308_36F08(var_s0);
            return 0;
        }
        func_80036308_36F08(var_s0);
        var_s0 = M2C_FIELD(arg0, s32 *, 0x18);
    }

    *(volatile s32 *)0x80000000 = 1;
}
