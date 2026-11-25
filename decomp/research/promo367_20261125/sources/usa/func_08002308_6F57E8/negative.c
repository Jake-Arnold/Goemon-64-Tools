#include "m2c_types.h"
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
M2C_UNK func_08002350_6F5830();                     /* static */

void func_08002308_6F57E8(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (((s32(*)())&func_800240DC_24CDC)(M2C_FIELD(arg0, u16 *, 0xD0)) != 0) {
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08002350_6F5830);
    }
}
