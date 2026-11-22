#include "m2c_types.h"
extern char func_80023D9C_2499C;
extern char func_80034E8C_35A8C;
extern char func_80038808_39408;
extern char func_8021B3BC_5D694C;
M2C_UNK func_08003F0C_6FBA9C();                     /* static */

void func_08003E84_6FBA14(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80023D9C_2499C)(0xA4) != 0) {
        ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, 3, 0x3DCCCCCD, 0);
        ((M2C_UNK(*)())&func_80038808_39408)(0x124);
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 1);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08003F0C_6FBA9C);
    }
}
