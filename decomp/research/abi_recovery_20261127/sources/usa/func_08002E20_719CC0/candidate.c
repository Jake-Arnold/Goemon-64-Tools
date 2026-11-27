#include "m2c_types.h"
extern char func_8021664C_5D1B1C;
extern char func_802206AC_5DBB7C;

void func_08002E20_719CC0(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;

    ((M2C_UNK  (*)(void *, M2C_UNK, M2C_UNK))&func_802206AC_5DBB7C)(arg0, 0, 0);
    temp_v0 = M2C_FIELD(arg0, s32 *, 0x68);
    if (temp_v0 & 0x4000) {
        M2C_FIELD(arg0, s32 *, 0x68) = (s32) (temp_v0 & ~0x4000);
        ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))&func_8021664C_5D1B1C)(arg0, 0, 0x3E800000, 1);
    }
}
