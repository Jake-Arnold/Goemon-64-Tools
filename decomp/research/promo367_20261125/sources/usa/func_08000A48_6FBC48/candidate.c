#include "../m2c_types.h"
extern char func_8003521C_35E1C;
M2C_UNK func_080009E4_6FBBE4();                     /* static */

void func_08000A48_6FBC48(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s16 *, 0x8A) = 0x5A;
    M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x7C) = 0.5f;
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_080009E4_6FBBE4);
}
