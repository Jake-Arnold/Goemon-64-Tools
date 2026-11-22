#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8022051C_5DBAAC;
M2C_UNK func_08000560_6EDDC0();                     /* static */

void func_08000508_6EDD68(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_8022051C_5DBAAC)(arg0, 0x42A00000) != 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = 0x02A007E1;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08000560_6EDDC0);
    }
}
