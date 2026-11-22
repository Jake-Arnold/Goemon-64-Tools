#include "m2c_types.h"
extern void *D_80214600_63F080;

void func_802004F0_62AF70(s32 arg0) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(D_80214600_63F080, void **, 0x1DC);
    if (temp_v0 != NULL) {
        M2C_FIELD(temp_v0, s32 *, 0x80) = arg0;
    }
}
