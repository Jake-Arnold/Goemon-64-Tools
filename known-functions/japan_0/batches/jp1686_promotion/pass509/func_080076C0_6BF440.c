#include "m2c_types.h"
extern char func_80023B00_24700;
extern char func_80023B54_24754;
extern char func_80034E8C_35A8C;
M2C_UNK func_08007740_6BF4C0();                     /* static */
M2C_UNK func_0800794C_6BF6CC();                     /* static */

void func_080076C0_6BF440(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80023B54_24754)(0xB) != 0) {
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_0800794C_6BF6CC);
        return;
    }
    ((M2C_UNK(*)())&func_80023B00_24700)(8);
    M2C_FIELD(arg0, s16 *, 0x8A) = 0x3C;
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08007740_6BF4C0);
}
