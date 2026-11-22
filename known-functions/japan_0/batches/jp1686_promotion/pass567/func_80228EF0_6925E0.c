#include "../m2c_types.h"
void func_80228EF0_6925E0(void *arg0, f32 arg1) {
    f32 temp_f0;
    void *temp_v0;

    M2C_FIELD(M2C_FIELD(arg0, void **, 0xB8), f32 *, 0x24) = arg1;
    temp_v0 = M2C_FIELD(arg0, void **, 0xB8);
    temp_f0 = M2C_FIELD(temp_v0, f32 *, 0x24);
    M2C_FIELD(temp_v0, f32 *, 0x20) = temp_f0;
    M2C_FIELD(M2C_FIELD(arg0, void **, 0xB8), f32 *, 0x1C) = temp_f0;
    M2C_FIELD(arg0, f32 *, 0xB4) = 0.0f;
}
