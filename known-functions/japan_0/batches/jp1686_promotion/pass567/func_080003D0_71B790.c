#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_08000410_71B7D0();                     /* static */

void func_080003D0_71B790(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s32 *, 0x68) = (s32) (M2C_FIELD(arg0, s32 *, 0x68) | 0x4400);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08000410_71B7D0);
}
