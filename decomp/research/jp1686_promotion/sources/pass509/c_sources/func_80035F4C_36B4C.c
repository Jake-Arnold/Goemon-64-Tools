#include "m2c_types.h"
void *func_80035F4C_36B4C(void *arg0) {
    void *var_v1;

    var_v1 = M2C_FIELD(arg0, void **, 0x18);
    if (var_v1 != NULL) {
        do {
            M2C_FIELD(var_v1, u8 *, 4) = (u8) (M2C_FIELD(var_v1, u8 *, 4) | 0x80);
            var_v1 = M2C_FIELD(var_v1, void **, 0);
        } while (var_v1 != NULL);
    }
    return var_v1;
}
