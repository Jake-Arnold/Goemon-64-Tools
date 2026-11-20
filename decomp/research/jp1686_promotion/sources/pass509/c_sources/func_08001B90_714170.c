#include "m2c_types.h"
void func_08001B90_714170(void *arg0, s32 arg1, s32 arg2) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x18);
    if (arg1 & 1) {
        M2C_FIELD(temp_v0, f32 *, 8) = (f32) (M2C_FIELD(temp_v0, f32 *, 8) + (f32) arg2);
        return;
    }
    M2C_FIELD(temp_v0, f32 *, 8) = (f32) (M2C_FIELD(temp_v0, f32 *, 8) - (f32) arg2);
}
