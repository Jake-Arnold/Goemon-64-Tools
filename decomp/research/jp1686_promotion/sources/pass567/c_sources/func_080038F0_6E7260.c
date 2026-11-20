#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_0800393C_6E72AC();                     /* static */

void func_080038F0_6E7260(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s16 *, 0x8A) = 0xA;
    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_0800393C_6E72AC);
}
