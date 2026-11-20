#include "m2c_types.h"
void func_801DB7BC_60623C(void *arg0) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x18);
    M2C_FIELD(temp_v0, f32 *, 8) = (f32) (M2C_FIELD(arg0, f32 *, 0x70) + M2C_FIELD(temp_v0, f32 *, 8));
}
