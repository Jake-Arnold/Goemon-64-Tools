#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
M2C_UNK func_08000A20_6EF380();                     /* static */

void func_08000984_6EF2E4(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, s32 *, 0x68);
    if (temp_v0 & 1) {
        M2C_FIELD(arg0, s32 *, 0x68) = (s32) (temp_v0 & ~1);
    }
    ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 0, 0x3E2AAAAB, 0);
    M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & ~1);
    M2C_FIELD(arg0, s16 *, 0x8A) = 0x3C;
    M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08000A20_6EF380);
}
