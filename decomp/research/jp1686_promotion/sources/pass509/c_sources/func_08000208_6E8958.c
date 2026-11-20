#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8021E548_5D9AD8;
extern char func_8021EF9C_5DA52C;
M2C_UNK func_08000260_6E89B0();                     /* static */

void func_08000208_6E8958(s32 arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_8021E548_5D9AD8)(arg0, 8) == 0) {
        ((M2C_UNK(*)())&func_8021EF9C_5DA52C)(arg0);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08000260_6E89B0);
    }
}
