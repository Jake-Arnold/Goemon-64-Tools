#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_08001128_6ECB58();                     /* static */

void func_080010E8_6ECB18(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08001128_6ECB58);
}
