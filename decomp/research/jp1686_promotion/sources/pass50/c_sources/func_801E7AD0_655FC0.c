#include "m2c_types.h"
extern f64 D_801F4B58_663048;

void func_801E7AD0_655FC0(void *arg0, M2C_UNK arg1) {
    s16 temp_v1;
    s32 temp_v1_2;
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0xEC);
    temp_v1 = M2C_FIELD(temp_v0, s16 *, 0);
    if (temp_v1 & 1) {
        if (temp_v1 & 2) {
            M2C_FIELD(temp_v0, s32 *, 0x318) = 0x5DC0;
        }
        temp_v1_2 = M2C_FIELD(temp_v0, s32 *, 0x318) + M2C_FIELD(temp_v0, s32 *, 0x31C);
        M2C_FIELD(temp_v0, s32 *, 0x31C) = temp_v1_2;
        M2C_FIELD(temp_v0, f32 *, 0x320) = (f32) ((f64) ((f32) temp_v1_2 / 1000.0f) * D_801F4B58_663048);
    }
}
