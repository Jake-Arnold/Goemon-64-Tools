#include "m2c_types.h"
extern char func_80023B00_24700;
extern char func_80023B54_24754;
extern char func_80034E8C_35A8C;
extern char func_8021E548_5D9AD8;
M2C_UNK func_08007424_6BF1A4();                     /* static */
M2C_UNK func_0800794C_6BF6CC();                     /* static */

void func_08007398_6BF118(s32 arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_80023B00_24700)(0xB);
    if (((s32(*)())&func_80023B54_24754)(0xB) != 0) {
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_0800794C_6BF6CC);
        return;
    }
    if (((s32(*)())&func_8021E548_5D9AD8)(arg0, 1) == 0) {
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08007424_6BF1A4);
    }
}
