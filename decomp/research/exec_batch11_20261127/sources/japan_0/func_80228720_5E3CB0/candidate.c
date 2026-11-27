#include "m2c_types.h"
M2C_UNK func_80033510_34110(u16, u16, M2C_UNK, f32 *, f32 *, f32 *); /* extern */

void func_80228720_5E3CB0(void *arg0, u16 arg1, u16 arg2, s16 arg3, u8 arg4) {
    f32 vec[5];
    void *temp_v0;

    vec[3] = 0.0f;
    vec[2] = 0.0f;
    vec[1] = (f64) (f32) arg3 / 50.0;
    func_80033510_34110(arg1, arg2, 0, &vec[3], &vec[2], &vec[1]);
    temp_v0 = M2C_FIELD(arg0, void **, 0x18);
    M2C_FIELD(arg0, s16 *, 0xD8) = (f64) vec[3] * 10.0;
    M2C_FIELD(arg0, s16 *, 0xDA) = (f64) vec[2] * 10.0;
    M2C_FIELD(arg0, s16 *, 0xDC) = (f64) vec[1] * 10.0;
    M2C_FIELD(arg0, s16 *, 0xD0) = (arg4 << 4) | 0xF;
    M2C_FIELD(arg0, s16 *, 0xC8) = M2C_FIELD(temp_v0, f32 *, 8);
    M2C_FIELD(arg0, s16 *, 0xCA) = M2C_FIELD(temp_v0, f32 *, 0xC);
    M2C_FIELD(arg0, s16 *, 0xCC) = M2C_FIELD(temp_v0, f32 *, 0x10);
}
