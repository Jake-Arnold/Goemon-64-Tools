#include "m2c_types.h"
s32 func_801F8B00_5B4AD0(void *arg0) {
    s32 var_v1;
    void *var_v0;

    var_v0 = M2C_FIELD(arg0, void **, 0);
    var_v1 = 0;
    if (var_v0 != NULL) {
loop_2:
        if ((s32) M2C_FIELD(arg0, u16 *, 0x20) < (s32) M2C_FIELD(var_v0, u16 *, 0x20)) {
            var_v0 = M2C_FIELD(var_v0, void **, 0);
            var_v1 += 1;
            if (var_v0 != NULL) {
                goto loop_2;
            }
        }
    }
    return var_v1;
}
