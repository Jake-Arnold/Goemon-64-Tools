#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_8003F1D8_3FDD8;
extern char func_801DACDC_596BEC;
extern char func_801FC5C0_5B84D0;
extern char func_802201F0_5DB6C0;
M2C_UNK func_080002C8_726758();                     /* static */
extern s32 D_801FC604_5B8514;

void func_08000A34_726EC4(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (((s32(*)())&func_8003F1D8_3FDD8)() == 0) {
        ((M2C_UNK(*)())&func_801DACDC_596BEC)(D_801FC604_5B8514, 0);
        if (((s32(*)())&func_802201F0_5DB6C0)(arg0) == 0) {
            ((M2C_UNK(*)())&func_801FC5C0_5B84D0)();
            M2C_FIELD(arg0, s16 *, 0x8A) = 0x1E;
            ((M2C_UNK(*)())&func_8003521C_35E1C)(func_080002C8_726758);
        }
    }
}
