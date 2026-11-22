#include "m2c_types.h"
u8 func_801D8F94_603A14(void *arg0) {
    void *temp_v1;

    temp_v1 = M2C_FIELD(arg0, void **, 0x38);
    if (temp_v1 != NULL) {
        return M2C_FIELD(temp_v1, u8 *, 0x4C);
    }
    return 0U;
}
