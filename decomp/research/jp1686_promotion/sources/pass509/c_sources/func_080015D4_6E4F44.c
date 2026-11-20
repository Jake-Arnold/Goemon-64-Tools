#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8021E548_5D9AD8;
extern char func_8022051C_5DBAAC;
M2C_UNK func_08001640_6E4FB0();                     /* static */

void func_080015D4_6E4F44(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_8021E548_5D9AD8)(arg0, 8);
    if (((s32(*)())&func_8022051C_5DBAAC)(arg0, 0x42C80000) != 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = 0x02AE87E1;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08001640_6E4FB0);
    }
}
