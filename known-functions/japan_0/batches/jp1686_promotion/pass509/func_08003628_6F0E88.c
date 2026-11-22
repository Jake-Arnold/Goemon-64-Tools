#include "m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_08003694_6F0EF4();                     /* static */
extern f64 D_080057C8_6F3028;

void func_08003628_6F0E88(void *arg0, void *arg1) {
    M2C_FIELD(arg1, f32 *, 8) = (f32) ((f64) M2C_FIELD(arg1, f32 *, 8) + D_080057C8_6F3028);
    if (M2C_FIELD(arg1, f32 *, 8) >= -10.0f) {
        M2C_FIELD(arg0, s16 *, 0xEE) = 0x200;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08003694_6F0EF4);
    }
}
