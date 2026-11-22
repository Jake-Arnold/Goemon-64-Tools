#include "../m2c_types.h"
void func_080011FC_70689C(void *arg0, s32 arg1) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x18);
    M2C_FIELD(temp_v0, f32 *, 0x24) = 1.0f;
    M2C_FIELD(temp_v0, f32 *, 0x20) = 1.0f;
    M2C_FIELD(temp_v0, f32 *, 0x1C) = 1.0f;
    M2C_FIELD(temp_v0, f32 *, 0x10) = (f32) (M2C_FIELD(temp_v0, f32 *, 0x10) - (f32) (arg1 * 0x960));
    M2C_FIELD(arg0, s16 *, 0x5E) = 0x1B0;
    M2C_FIELD(arg0, s32 *, 0x60) = 0x80000021;
}
