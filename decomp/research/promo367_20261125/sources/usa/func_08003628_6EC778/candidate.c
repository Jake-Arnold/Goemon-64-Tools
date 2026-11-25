#include "m2c_types.h"
extern char func_8003521C_35E1C;
M2C_UNK func_08003694_6EC7E4();                     /* static */
extern f64 D_080057C8_6EE918;

void func_08003628_6EC778(void *arg0, void *arg1) {
    M2C_FIELD(arg1, f32 *, 8) = (f32) ((f64) M2C_FIELD(arg1, f32 *, 8) + D_080057C8_6EE918);
    if (M2C_FIELD(arg1, f32 *, 8) >= -10.0f) {
        M2C_FIELD(arg0, s16 *, 0xEE) = 0x200;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08003694_6EC7E4);
    }
}
