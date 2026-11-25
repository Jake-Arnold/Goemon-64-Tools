#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_8021B7AC_5D6C7C;
M2C_UNK func_08000560_6E96B0();                     /* static */

void func_08000508_6E9658(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_8021B7AC_5D6C7C)(arg0, 0x42A00000) != 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = 0x02A007E1;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08000560_6E96B0);
    }
}
