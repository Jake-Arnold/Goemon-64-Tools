#include "m2c_types.h"
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
M2C_UNK func_08000970_6C8B80();                     /* static */

void func_080025C8_6CA7D8(s32 arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    if ((((s32(*)())&func_800240DC_24CDC)(0x16C) == 0) && (M2C_FIELD(arg1, u8 *, 0x7C) & 2)) {
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08000970_6C8B80);
    }
}
