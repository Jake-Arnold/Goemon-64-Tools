#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_080009E4_7001B4();                     /* static */

void func_08000A48_700218(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s16 *, 0x8A) = 0x5A;
    M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x7C) = 0.5f;
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080009E4_7001B4);
}
