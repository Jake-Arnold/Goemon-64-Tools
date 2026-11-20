#include "m2c_types.h"
extern void *D_80214600_63F080;

s32 func_801D909C_603B1C(void) {
    s32 var_v1;

    var_v1 = M2C_FIELD(D_80214600_63F080, s32 *, 0x60);
    if (var_v1 <= 0) {
        M2C_FIELD(D_80214600_63F080, s32 *, 0x60) = 0;
        var_v1 = 0;
    }
    return var_v1;
}
