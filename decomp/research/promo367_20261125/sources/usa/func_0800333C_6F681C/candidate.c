#include "m2c_types.h"
extern char func_8003521C_35E1C;
M2C_UNK func_08003388_6F6868();                     /* static */

void func_0800333C_6F681C(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & ~1);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08003388_6F6868);
    }
}
