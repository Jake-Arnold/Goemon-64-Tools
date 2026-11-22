#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_80221398_5DC928;
M2C_UNK func_08002E44_6D6944();                     /* static */

void func_08002DF4_6D68F4(void *arg0, M2C_UNK arg1) {
    if (!(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        ((M2C_UNK(*)())&func_80221398_5DC928)(arg0, 0x40000000);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08002E44_6D6944);
    }
}
