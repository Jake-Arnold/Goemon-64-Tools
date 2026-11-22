#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_08003C7C_6BB9FC();                     /* static */

void func_08003C40_6BB9C0(s32 arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08003C7C_6BB9FC);
    }
}
