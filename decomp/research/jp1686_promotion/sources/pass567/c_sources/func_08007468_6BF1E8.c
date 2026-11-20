#include "../m2c_types.h"
extern char func_80023B00_24700;
extern char func_80034E8C_35A8C;
M2C_UNK func_080074B8_6BF238();                     /* static */

void func_08007468_6BF1E8(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_80023B00_24700)(7);
    M2C_FIELD(arg0, s16 *, 0x8A) = 0xB4;
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080074B8_6BF238);
}
