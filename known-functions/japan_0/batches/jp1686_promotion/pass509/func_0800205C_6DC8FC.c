#include "m2c_types.h"
extern char func_8021B3BC_5D694C;
extern char func_8021DAEC_5D907C;
extern char func_8021DB00_5D9090;
extern char func_8021DB18_5D90A8;
extern char func_8021EBE0_5DA170;
extern char func_8021F3B4_5DA944;
extern char func_8021FDD4_5DB364;
extern char func_8021FE0C_5DB39C;
extern char func_802213C4_5DC954;
extern M2C_UNK D_08003D50_6DE5F0;

void func_0800205C_6DC8FC(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_8021F3B4_5DA944)();
    M2C_FIELD(arg0, s32 *, 0x60) = 0x022E83E1;
    M2C_FIELD(arg0, s16 *, 0x96) = 0x3E1;
    M2C_FIELD(arg0, s8 *, 0x8E) = 2;
    M2C_FIELD(arg0, s8 *, 0x8F) = 3;
    ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, 0, 0x3E800000, 1);
    ((M2C_UNK(*)())&func_802213C4_5DC954)(arg0);
    ((M2C_UNK(*)())&func_8021EBE0_5DA170)(arg0, 0xA, 0);
    ((M2C_UNK(*)())&func_8021DAEC_5D907C)(arg0, 0x64, 0x32, -0x14);
    ((M2C_UNK(*)())&func_8021DB18_5D90A8)(arg0, 0x14, 0x3C, 0);
    ((M2C_UNK(*)())&func_8021DB00_5D9090)(arg0, 0x14, 7, 7, 0);
    ((M2C_UNK(*)())&func_8021FDD4_5DB364)(arg0, &D_08003D50_6DE5F0, 0);
    ((M2C_UNK(*)())&func_8021FE0C_5DB39C)(arg0, 0, 1);
}
