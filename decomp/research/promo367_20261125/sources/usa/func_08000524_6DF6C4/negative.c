#include "m2c_types.h"
extern char func_8003521C_35E1C;
M2C_UNK func_0800057C_6DF71C();                     /* static */

void func_08000524_6DF6C4(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x1E;
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & 0xFEFFFFFF);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_0800057C_6DF71C);
    }
}
