#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_080014C8_6C5688();                     /* static */

void func_08001488_6C5648(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 1);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080014C8_6C5688);
}
