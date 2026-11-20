#include "m2c_types.h"
void func_801EDF4C_5A9F1C(void *arg0) {
    void *var_v0;

    if (arg0 != NULL) {
        var_v0 = M2C_FIELD(arg0, void **, 0x18);
        if (var_v0 != NULL) {
            do {
                M2C_FIELD(var_v0, s8 *, 0x64) = 1;
                M2C_FIELD(var_v0, s32 *, 0x2C) = 0;
                M2C_FIELD(var_v0, s32 *, 0x30) = 0;
                var_v0 = M2C_FIELD(var_v0, void **, 0);
            } while (var_v0 != NULL);
        }
    }
}
