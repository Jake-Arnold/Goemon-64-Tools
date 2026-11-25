#include "m2c_types.h"
extern char func_80035020_35C20;
extern char func_8003521C_35E1C;
extern char func_802209F0_5DBEC0;
M2C_UNK func_0800121C_6EFB7C();                     /* static */

void func_080011A0_6EFB00(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_v0;

    M2C_FIELD(arg0, s16 *, 0xD4) = 0;
    temp_v0 = ((s32(*)())&func_802209F0_5DBEC0)();
    M2C_FIELD(arg0, s32 *, 0xD8) = temp_v0;
    if (temp_v0 == 0) {
        ((M2C_UNK(*)())&func_80035020_35C20)();
        return;
    }
    M2C_FIELD(arg1, s32 *, 0x30) = (s32) (M2C_FIELD(arg0, s32 *, 0xD8) | 0x20000000);
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_0800121C_6EFB7C);
}
