#include "m2c_types.h"
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
M2C_UNK func_08006740_6F9C20();                     /* static */

void func_080066D8_6F9BB8(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (((s32(*)())&func_800240DC_24CDC)(0x19D, arg0) != 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 1);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x1E;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08006740_6F9C20, arg0);
    }
}
