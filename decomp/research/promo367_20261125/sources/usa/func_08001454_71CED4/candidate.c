#include "m2c_types.h"
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
M2C_UNK func_08000284_71BD04();                     /* static */
M2C_UNK func_08001398_71CE18();                     /* static */

void func_08001454_71CED4(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_800240DC_24CDC)(0x18, arg0) != 0) {
        M2C_FIELD(arg0, s16 *, 0x5E) = 0x2BF;
        M2C_FIELD(arg0, s32 *, 0xD4) = 0x14E;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08000284_71BD04, arg0);
        return;
    }
    M2C_FIELD(arg0, s16 *, 0x5E) = 0x2C5;
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08001398_71CE18, arg0);
}
