#include "m2c_types.h"
extern char func_80023C78_24878;
extern char func_80034E8C_35A8C;
M2C_UNK func_08003750_708DF0();                     /* static */

void func_080036F0_708D90(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80023C78_24878)(0) != 0) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 1;
    } else {
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x200;
    }
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08003750_708DF0);
}
