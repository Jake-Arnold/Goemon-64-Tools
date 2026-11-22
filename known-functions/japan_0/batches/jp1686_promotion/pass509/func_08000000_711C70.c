#include "m2c_types.h"
extern char func_8021B3BC_5D694C;
extern char func_80225CE0_5E1270;
extern char func_80229AC0_5E5050;

void func_08000000_711C70(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;

    M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 0x10000000);
    ((M2C_UNK(*)())&func_80225CE0_5E1270)();
    temp_v0 = M2C_FIELD(arg0, s32 *, 0x68);
    if (temp_v0 & 0x4000) {
        M2C_FIELD(arg0, s32 *, 0x68) = (s32) (temp_v0 & ~0x4000);
        ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, 1, 0x3E800000, 1);
    }
    ((M2C_UNK(*)())&func_80229AC0_5E5050)(arg0, 1);
}
