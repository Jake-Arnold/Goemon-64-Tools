#include "m2c_types.h"
extern char func_80023D9C_2499C;
extern char func_80034E8C_35A8C;
M2C_UNK func_08006664_6FE1F4();                     /* static */

void func_080065FC_6FE18C(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80023D9C_2499C)(0x19D, arg0) != 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 1);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x1E;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08006664_6FE1F4, arg0);
    }
}
