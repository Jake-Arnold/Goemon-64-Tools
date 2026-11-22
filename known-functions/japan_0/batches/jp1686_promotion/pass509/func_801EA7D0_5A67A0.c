#include "m2c_types.h"
void func_801EA7D0_5A67A0(void *arg0) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), void **, 0x8C);
    if (temp_v0 != NULL) {
        M2C_FIELD(temp_v0, s32 *, 0x68) = (s32) (M2C_FIELD(temp_v0, s32 *, 0x68) & 0xFFFF7FFF);
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), void **, 0x8C) = NULL;
    }
}
