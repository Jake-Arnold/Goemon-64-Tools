#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_080016B4_71CA74();                     /* static */

void func_0800195C_71CD1C(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s32 *, 0x68) = (s32) (M2C_FIELD(arg0, s32 *, 0x68) & ~0x4000);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080016B4_71CA74);
}
