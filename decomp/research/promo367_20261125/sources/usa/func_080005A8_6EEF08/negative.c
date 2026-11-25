#include "m2c_types.h"
extern char func_8003521C_35E1C;
M2C_UNK func_080005F4_6EEF54();                     /* static */

void func_080005A8_6EEF08(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & ~1);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_080005F4_6EEF54);
    }
}
