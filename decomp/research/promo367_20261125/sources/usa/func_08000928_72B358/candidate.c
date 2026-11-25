#include "m2c_types.h"
extern char func_80014B74_15774;
extern char func_80034ED4_35AD4;
extern char func_8003F1D8_3FDD8;
extern s32 D_8015C5C8_15D1C8;

void func_08000928_72B358(void *arg0, M2C_UNK arg1) {
    s32 sp1C;

    sp1C = M2C_FIELD(arg0, s32 *, 0xD0);
    if (((s32(*)())&func_8003F1D8_3FDD8)() == 0) {
        ((M2C_UNK(*)())&func_80014B74_15774)(D_8015C5C8_15D1C8 + 0xC7FA4, sp1C);
        ((M2C_UNK(*)())&func_80034ED4_35AD4)();
    }
}
