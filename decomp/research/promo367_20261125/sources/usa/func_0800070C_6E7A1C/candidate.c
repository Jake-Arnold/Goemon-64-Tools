#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern char func_80218DA8_5D4278;
extern char func_80219E70_5D5340;
extern char func_8021A644_5D5B14;
extern char func_80224ABC_5DFF8C;
extern char func_80226840_5E1D10;
M2C_UNK func_080007E0_6E7AF0();                     /* static */

void func_0800070C_6E7A1C(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_8021A644_5D5B14)();
    M2C_FIELD(arg0, s32 *, 0x60) = 0x2006E3;
    ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 0, 0x3E800000, 1);
    ((M2C_UNK(*)())&func_80224ABC_5DFF8C)(arg0, 0, 0x3F800000, 1);
    ((M2C_UNK(*)())&func_80218DA8_5D4278)(arg0, 0x28, 0x28, 0);
    ((M2C_UNK(*)())&func_80219E70_5D5340)(arg0, 5, 0);
    ((M2C_UNK(*)())&func_80226840_5E1D10)(arg0, M2C_FIELD(arg0, u16 *, 0xD2));
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_080007E0_6E7AF0);
}
