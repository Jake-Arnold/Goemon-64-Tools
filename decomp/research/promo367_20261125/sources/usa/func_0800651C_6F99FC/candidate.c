#include "m2c_types.h"
extern char func_8003521C_35E1C;
M2C_UNK func_08006568_6F9A48();                     /* static */

void func_0800651C_6F99FC(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & ~1);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08006568_6F9A48);
    }
}
