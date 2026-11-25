#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern char func_802197D8_5D4CA8;
M2C_UNK func_080016BC_6E085C();                     /* static */

void func_08001640_6E07E0(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_802197D8_5D4CA8)(arg0, 0x10);
    if (!(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 1, 0x3F000000, 0);
        M2C_FIELD(arg0, s16 *, 0x8A) = 5;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_080016BC_6E085C);
    }
}
