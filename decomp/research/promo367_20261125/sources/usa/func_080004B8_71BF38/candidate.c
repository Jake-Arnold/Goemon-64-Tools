#include "m2c_types.h"
extern char func_800240DC_24CDC;
extern char func_80034ED4_35AD4;
extern char func_8003521C_35E1C;
M2C_UNK func_080003FC_71BE7C();                     /* static */

void func_080004B8_71BF38(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_800240DC_24CDC)(0x18) != 0) {
        M2C_FIELD(arg0, s16 *, 0x5E) = 0x2C1;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_080003FC_71BE7C);
        return;
    }
    ((M2C_UNK(*)())&func_80034ED4_35AD4)();
}
