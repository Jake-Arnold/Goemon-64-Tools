#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8021EBE0_5DA170;
extern char func_8021F3B4_5DA944;
extern char func_802213C4_5DC954;
M2C_UNK func_080028E0_6DD180();                     /* static */

void func_08002848_6DD0E8(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_8021F3B4_5DA944)();
    M2C_FIELD(arg0, s32 *, 0x60) = 0x02A687E1;
    M2C_FIELD(arg0, s8 *, 0x8E) = 2;
    M2C_FIELD(arg0, s8 *, 0x8F) = 3;
    M2C_FIELD(arg0, s16 *, 0x96) = 0x21;
    ((M2C_UNK(*)())&func_802213C4_5DC954)(arg0);
    ((M2C_UNK(*)())&func_8021EBE0_5DA170)(arg0, 0xA, 0);
    M2C_FIELD(arg0, s8 *, 0xDC) = 0;
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080028E0_6DD180);
}
