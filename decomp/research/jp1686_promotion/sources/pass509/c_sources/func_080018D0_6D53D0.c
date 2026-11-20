#include "m2c_types.h"
extern char func_80034E8C_35A8C;
s32 func_080016A8_6D51A8();                         /* static */
M2C_UNK func_0800191C_6D541C();                     /* static */

void func_080018D0_6D53D0(void *arg0, M2C_UNK arg1) {
    if ((func_080016A8_6D51A8() == 0) && !(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_0800191C_6D541C);
    }
}
