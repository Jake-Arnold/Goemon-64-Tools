#include "m2c_types.h"
s32 func_801D8D9C_60381C(void *arg0) {
    void *temp_v1;

    temp_v1 = M2C_FIELD(arg0, void **, 0x34);
    if (temp_v1 != NULL) {
        return M2C_FIELD(temp_v1, s32 *, 0x60);
    }
    return 0;
}
