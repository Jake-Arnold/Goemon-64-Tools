#include "m2c_types.h"
s32 func_80015D80_16980(s32, s32);                  /* extern */
M2C_UNK func_80015E84_16A84(s32, s32);              /* extern */

void func_80016154_16D54(void *arg0) {
    s32 var_s0;
    s32 var_s1;
    s32 var_v0;
    s32 var_v1;

    var_v1 = M2C_FIELD(arg0, s32 *, 4);
    var_s1 = 0;
    if (var_v1 > 0) {
        var_v0 = M2C_FIELD(arg0, s32 *, 0);
        do {
            var_s0 = 0;
            if (var_v0 > 0) {
                do {
                    if (M2C_FIELD(arg0, s32 *, 0x14) == (func_80015D80_16980(var_s0, var_s1) & 0xFFFE)) {
                        func_80015E84_16A84(var_s0, var_s1);
                    }
                    var_v0 = M2C_FIELD(arg0, s32 *, 0);
                    var_s0 += 1;
                } while (var_s0 < var_v0);
                var_v1 = M2C_FIELD(arg0, s32 *, 4);
            }
            var_s1 += 1;
        } while (var_s1 < var_v1);
    }
}
