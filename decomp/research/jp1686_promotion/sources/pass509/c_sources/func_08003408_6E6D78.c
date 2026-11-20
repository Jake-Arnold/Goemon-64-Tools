#include "m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_08003460_6E6DD0();                     /* static */

void func_08003408_6E6D78(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x14;
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & 0xFEFFFFFF);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08003460_6E6DD0);
    }
}
