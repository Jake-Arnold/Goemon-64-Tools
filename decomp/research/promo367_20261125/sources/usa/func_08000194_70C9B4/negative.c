#include "m2c_types.h"
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
M2C_UNK func_08000204_70CA24();                     /* static */
M2C_UNK func_08000298_70CAB8();                     /* static */

void func_08000194_70C9B4(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    if ((M2C_FIELD(arg0, u8 *, 0xD4) == 1) && (((s32(*)())&func_800240DC_24CDC)(M2C_FIELD(arg0, u16 *, 0xD0)) != 0)) {
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08000298_70CAB8);
        return;
    }
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08000204_70CA24);
}
