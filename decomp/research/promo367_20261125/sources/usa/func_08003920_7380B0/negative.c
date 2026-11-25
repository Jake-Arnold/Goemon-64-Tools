#include "m2c_types.h"
extern char func_80013AC4_146C4;
extern char func_80038BC8_397C8;
extern char osViSetSpecialFeatures;
extern M2C_UNK D_080039D0_738160;

void func_08003920_7380B0(void) {
volatile unsigned int goemon_negative_control = 1;

    ((M2C_UNK(*)())&osViSetSpecialFeatures)(0x40);
    ((M2C_UNK(*)())&func_80038BC8_397C8)(1);
    ((M2C_UNK(*)())&func_80013AC4_146C4)(&D_080039D0_738160);
}
