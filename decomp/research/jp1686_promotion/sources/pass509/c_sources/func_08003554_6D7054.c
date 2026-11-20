#include "m2c_types.h"
extern char func_8021B3BC_5D694C;
extern char func_8021DAEC_5D907C;
extern char func_8021DB18_5D90A8;
extern char func_8021DFEC_5D957C;
extern char func_8021EBE0_5DA170;
extern char func_8021F3B4_5DA944;
extern char func_8021FDD4_5DB364;
extern char func_8021FE0C_5DB39C;
extern M2C_UNK D_08004710_6D8210;

void func_08003554_6D7054(void *arg0, void *arg1) {
    ((M2C_UNK(*)())&func_8021F3B4_5DA944)();
    M2C_FIELD(arg0, s32 *, 0x60) = 0x062A17E1;
    M2C_FIELD(arg0, s16 *, 0x96) = 0x3F;
    M2C_FIELD(arg0, s32 *, 0x64) = 0x200000;
    M2C_FIELD(arg0, s16 *, 0xE0) = (s16) (s32) M2C_FIELD(arg1, f32 *, 0xC);
    ((M2C_UNK(*)())&func_8021DFEC_5D957C)(arg0);
    ((M2C_UNK(*)())&func_8021EBE0_5DA170)(arg0, 0xA, 0);
    ((M2C_UNK(*)())&func_8021DAEC_5D907C)(arg0, 0x64, 0x64, -0x28);
    ((M2C_UNK(*)())&func_8021DB18_5D90A8)(arg0, 0xA, 0xA, 0);
    ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, 0, 0x3F800000, 1);
    ((M2C_UNK(*)())&func_8021FDD4_5DB364)(arg0, &D_08004710_6D8210, 0);
    ((M2C_UNK(*)())&func_8021FE0C_5DB39C)(arg0, 1, 1);
}
