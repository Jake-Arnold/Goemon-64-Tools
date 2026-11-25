#include "m2c_types.h"
extern char func_800240DC_24CDC;
extern char func_80034ED4_35AD4;
extern char func_8003521C_35E1C;
M2C_UNK func_08000284_71BD04();                     /* static */

void func_08000524_71BFA4(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_800240DC_24CDC)(0x18) != 0) {
        M2C_FIELD(arg0, s16 *, 0x5E) = 0x2BF;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08000284_71BD04);
        return;
    }
    ((M2C_UNK(*)())&func_80034ED4_35AD4)();
}
