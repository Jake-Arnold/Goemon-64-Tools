#include "m2c_types.h"
u32 func_80033B9C_3479C(u16);                       /* extern */
s32 func_80033D74_34974(u16);                       /* extern */
extern f32 D_8016E760_16F360;
extern f32 D_8016E764_16F364;
extern f32 D_8016E768_16F368;
extern f32 D_8016E76C_16F36C;

void func_80033208_33E08(void *arg0) {
    D_8016E76C_16F36C = (f32) ((f64) (f32) func_80033B9C_3479C(M2C_FIELD(arg0, u16 *, 0)) * 0.00390625);
    D_8016E760_16F360 = (f32) ((f64) (f32) func_80033D74_34974(M2C_FIELD(arg0, u16 *, 2)) * 0.03125);
    D_8016E764_16F364 = (f32) ((f64) (f32) func_80033D74_34974(M2C_FIELD(arg0, u16 *, 4)) * 0.03125);
    D_8016E768_16F368 = (f32) ((f64) (f32) func_80033D74_34974(M2C_FIELD(arg0, u16 *, 6)) * 0.03125);
}
