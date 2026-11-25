#include "m2c_types.h"
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
M2C_UNK func_08005DEC_6B908C();                     /* static */

void func_08005D98_6B9038(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_800240DC_24CDC)(0x12E) != 0) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x40;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08005DEC_6B908C);
    }
}
