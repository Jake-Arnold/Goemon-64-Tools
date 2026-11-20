#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_08003C40_6BB9C0();                     /* static */

void func_08003C04_6BB984(void *arg0, M2C_UNK arg1) {
    if (!(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08003C40_6BB9C0);
    }
}
