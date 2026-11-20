#include "../m2c_types.h"
M2C_UNK osSpTaskYield();                            /* extern */

void func_8000762C_822C(void *arg0) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x2AC);
    if (M2C_FIELD(temp_v0, s32 *, 0x10) == 1) {
        M2C_FIELD(temp_v0, s32 *, 4) = (s32) (M2C_FIELD(temp_v0, s32 *, 4) | 0x10);
        osSpTaskYield();
    }
}
