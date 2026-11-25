#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_802197D8_5D4CA8;
extern char func_8021A22C_5D56FC;
M2C_UNK func_08000260_6E4240();                     /* static */

void func_08000208_6E41E8(s32 arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_802197D8_5D4CA8)(arg0, 8) == 0) {
        ((M2C_UNK(*)())&func_8021A22C_5D56FC)(arg0);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08000260_6E4240);
    }
}
