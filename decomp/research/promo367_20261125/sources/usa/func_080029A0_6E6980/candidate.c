#include "m2c_types.h"
extern char func_8003521C_35E1C;
M2C_UNK func_080029F0_6E69D0();                     /* static */

void func_080029A0_6E6980(void *arg0, void *arg1) {
    M2C_FIELD(arg1, u16 *, 0x16) = (u16) ((M2C_FIELD(arg1, u16 *, 0x16) + 0x40) & 0x3FF);
    if (!(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x14;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_080029F0_6E69D0);
    }
}
