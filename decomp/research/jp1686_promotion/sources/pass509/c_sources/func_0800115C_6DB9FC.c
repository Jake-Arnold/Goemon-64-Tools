#include "m2c_types.h"
extern char func_8021B3BC_5D694C;
extern char func_8021DB00_5D9090;
extern char func_8021EBE0_5DA170;
extern char func_8021F3B4_5DA944;
extern char func_8021FDD4_5DB364;
extern char func_8021FE0C_5DB39C;
extern M2C_UNK D_08003D30_6DE5D0;

void func_0800115C_6DB9FC(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_8021F3B4_5DA944)();
    M2C_FIELD(arg0, s32 *, 0x60) = 0x02248361;
    M2C_FIELD(arg0, s8 *, 0x8E) = 1;
    M2C_FIELD(arg0, s8 *, 0x8F) = 2;
    M2C_FIELD(arg0, s16 *, 0x96) = 0x1E1;
    M2C_FIELD(arg0, s16 *, 0x4E) = 0x14;
    ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, 0, 0x3EAAAAAB, 1);
    ((M2C_UNK(*)())&func_8021EBE0_5DA170)(arg0, 0xA, 0);
    ((M2C_UNK(*)())&func_8021DB00_5D9090)(arg0, 0x28, 0x14, 0x14, -0x14);
    ((M2C_UNK(*)())&func_8021FDD4_5DB364)(arg0, &D_08003D30_6DE5D0, 0);
    ((M2C_UNK(*)())&func_8021FE0C_5DB39C)(arg0, 0, 1);
}
