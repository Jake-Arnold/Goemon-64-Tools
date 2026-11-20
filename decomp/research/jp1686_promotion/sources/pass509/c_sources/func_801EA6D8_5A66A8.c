#include "m2c_types.h"
void func_801EA6D8_5A66A8(void *arg0, void *arg1) {
    void *temp_v0;

    M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), void **, 0x8C) = arg1;
    temp_v0 = M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), void **, 0x8C);
    if (temp_v0 != NULL) {
        M2C_FIELD(temp_v0, s32 *, 0x68) = (s32) (M2C_FIELD(temp_v0, s32 *, 0x68) | 0x8000);
        M2C_FIELD(arg0, f32 *, 0xE8) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0xE4) = 0.0f;
    }
}
