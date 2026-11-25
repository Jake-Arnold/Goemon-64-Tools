#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
M2C_UNK func_0800439C_6D347C();                     /* static */

void func_08004338_6D3418(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_0800439C_6D347C);
        ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 0, 0x3F800000, 1);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x96;
    }
}
