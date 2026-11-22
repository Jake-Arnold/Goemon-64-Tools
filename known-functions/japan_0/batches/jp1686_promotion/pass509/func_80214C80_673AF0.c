#include "m2c_types.h"
extern f64 D_8021C4E0_67B350;
extern f64 D_8021C4E8_67B358;

void func_80214C80_673AF0(void *arg0, f32 arg1) {
    f32 temp_f0;
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x18);
    if (temp_v0 != NULL) {
        temp_f0 = (f32) ((f64) arg1 * D_8021C4E0_67B350);
        M2C_FIELD(temp_v0, f32 *, 0x1C) = temp_f0;
        M2C_FIELD(temp_v0, f32 *, 0x20) = temp_f0;
        M2C_FIELD(temp_v0, f32 *, 0x24) = temp_f0;
    }
    M2C_FIELD(arg0, f32 *, 0x6C) = (f32) ((f64) arg1 * D_8021C4E8_67B358);
}
