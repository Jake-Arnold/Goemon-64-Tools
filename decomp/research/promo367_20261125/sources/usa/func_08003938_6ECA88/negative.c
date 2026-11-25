#include "m2c_types.h"
extern char func_80034ED4_35AD4;

void func_08003938_6ECA88(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    void *temp_v0;

    if ((M2C_FIELD(arg1, f32 *, 8) < -115.0f) && (M2C_FIELD(arg1, f32 *, 0x10) > 0.0f)) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & 0x7FFFFFFF);
    }
    if ((M2C_FIELD(arg1, f32 *, 8) < -165.0f) && (M2C_FIELD(arg1, f32 *, 0x10) > 0.0f)) {
        ((M2C_UNK(*)())&func_80034ED4_35AD4)();
        return;
    }
    temp_v0 = M2C_FIELD(M2C_FIELD(arg0, void **, 0xD0), void **, 0x18);
    M2C_FIELD(arg1, f32 *, 8) = (f32) M2C_FIELD(temp_v0, f32 *, 8);
    M2C_FIELD(arg1, f32 *, 0x10) = (f32) M2C_FIELD(temp_v0, f32 *, 0x10);
}
