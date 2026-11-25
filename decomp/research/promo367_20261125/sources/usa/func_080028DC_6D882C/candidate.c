#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80219E70_5D5340;
extern char func_8021A644_5D5B14;
extern char func_8021C654_5D7B24;
M2C_UNK func_08002974_6D88C4();                     /* static */

void func_080028DC_6D882C(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_8021A644_5D5B14)();
    M2C_FIELD(arg0, s32 *, 0x60) = 0x02A687E1;
    M2C_FIELD(arg0, s8 *, 0x8E) = 2;
    M2C_FIELD(arg0, s8 *, 0x8F) = 3;
    M2C_FIELD(arg0, s16 *, 0x96) = 0x21;
    ((M2C_UNK(*)())&func_8021C654_5D7B24)(arg0);
    ((M2C_UNK(*)())&func_80219E70_5D5340)(arg0, 0xA, 0);
    M2C_FIELD(arg0, s8 *, 0xDC) = 0;
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08002974_6D88C4);
}
