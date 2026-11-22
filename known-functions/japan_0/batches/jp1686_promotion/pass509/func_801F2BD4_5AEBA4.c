#include "m2c_types.h"
M2C_UNK func_80038838_39438(M2C_UNK, void *);       /* extern */

void func_801F2BD4_5AEBA4(void *arg0) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x38);
    if ((temp_v0 != NULL) && (M2C_FIELD(temp_v0, u8 *, 0x4C) == 6)) {
        func_80038838_39438(0x23B, arg0);
    }
    M2C_FIELD(arg0, void **, 0x38) = NULL;
    M2C_FIELD(arg0, s32 *, 0x34) = 0;
}
