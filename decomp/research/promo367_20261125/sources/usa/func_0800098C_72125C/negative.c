#include "m2c_types.h"
extern char func_80024038_24C38;
extern char func_800240DC_24CDC;
extern char func_80034ED4_35AD4;
extern char func_8003D310_3DF10;

void func_0800098C_72125C(s32 arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (((s32(*)())&func_800240DC_24CDC)(0x199) == 0) {
        ((M2C_UNK(*)())&func_80024038_24C38)(0x199);
        ((M2C_UNK(*)())&func_8003D310_3DF10)(0x137);
    }
    ((M2C_UNK(*)())&func_80034ED4_35AD4)();
}
