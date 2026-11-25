#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_802197D8_5D4CA8;
M2C_UNK func_0800463C_6DE50C();                     /* static */

void func_080045EC_6DE4BC(M2C_UNK arg0, void *arg1) {
    if (((s32(*)())&func_802197D8_5D4CA8)(arg0, 0x10) == 0) {
        M2C_FIELD(arg1, s8 *, 0x7C) = 1;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_0800463C_6DE50C);
    }
}
