#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8021B3BC_5D694C;
extern char func_8021E548_5D9AD8;
M2C_UNK func_080016BC_6E502C();                     /* static */

void func_08001640_6E4FB0(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_8021E548_5D9AD8)(arg0, 0x10);
    if (!(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, 1, 0x3F000000, 0);
        M2C_FIELD(arg0, s16 *, 0x8A) = 5;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080016BC_6E502C);
    }
}
