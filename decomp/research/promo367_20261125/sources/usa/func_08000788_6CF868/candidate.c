#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern char func_802197D8_5D4CA8;
M2C_UNK func_080007EC_6CF8CC();                     /* static */

void func_08000788_6CF868(s32 arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_802197D8_5D4CA8)(arg0, 8) == 0) {
        ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 1, 0x3E800000, 1);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_080007EC_6CF8CC);
    }
}
