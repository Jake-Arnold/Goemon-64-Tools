#include "m2c_types.h"
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern char func_80218DCC_5D429C;
M2C_UNK func_08002410_6CA620();                     /* static */

void func_08002380_6CA590(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    if ((((s32(*)())&func_800240DC_24CDC)(0x16C) == 0) && (M2C_FIELD(arg1, u8 *, 0x7C) & 2)) {
        ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 2, 0x3E800000, 4);
        ((M2C_UNK(*)())&func_80218DCC_5D429C)(arg0, 3);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08002410_6CA620);
    }
}
