#include "m2c_types.h"
extern char func_8021B3BC_5D694C;
extern char func_8021DAEC_5D907C;
extern char func_8021DB00_5D9090;
extern char func_8021DB18_5D90A8;
extern char func_8021EBE0_5DA170;
extern char func_8021F3B4_5DA944;
extern char func_8021FDD4_5DB364;
extern char func_8021FE0C_5DB39C;
extern char func_8022982C_5E4DBC;
extern M2C_UNK D_08004670_6D8170;

void func_08000000_6D3B00(void *arg0, void *arg1) {
    ((M2C_UNK(*)())&func_8021F3B4_5DA944)();
    M2C_FIELD(arg0, s32 *, 0x60) = 0x062E0FE3;
    M2C_FIELD(arg0, s32 *, 0x64) = 0x200000;
    M2C_FIELD(arg0, s16 *, 0x96) = 0x223;
    M2C_FIELD(arg0, s8 *, 0x8E) = 1;
    M2C_FIELD(arg0, s8 *, 0x8F) = 2;
    M2C_FIELD(arg0, s16 *, 0xE0) = (s16) (s32) M2C_FIELD(arg1, f32 *, 0xC);
    ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, 0, 0x3F000000, 1);
    ((M2C_UNK(*)())&func_8022982C_5E4DBC)(arg0, 0, 0x3F800000, 1);
    ((M2C_UNK(*)())&func_8021EBE0_5DA170)(arg0, 0xA, 0);
    ((M2C_UNK(*)())&func_8021DAEC_5D907C)(arg0, 0xC8, 0xC8, -0x28);
    ((M2C_UNK(*)())&func_8021DB18_5D90A8)(arg0, 0x64, 0xA, 0);
    ((M2C_UNK(*)())&func_8021DB00_5D9090)(arg0, 0xF, 8, 8, -3);
    ((M2C_UNK(*)())&func_8021FDD4_5DB364)(arg0, &D_08004670_6D8170, 0);
    ((M2C_UNK(*)())&func_8021FE0C_5DB39C)(arg0, 1, 1);
}
