#include "../m2c_types.h"
extern char func_8003521C_35E1C;
M2C_UNK func_08003958_6E2AF8();                     /* static */

void func_0800390C_6E2AAC(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s16 *, 0x8A) = 0xA;
    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08003958_6E2AF8);
}
