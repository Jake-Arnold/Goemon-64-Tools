#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_80200150_5BC120;
M2C_UNK func_08002250_6F9DE0();                     /* static */
extern M2C_UNK D_80162420_163020;

void func_08003D60_6FB8F0(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, u16 *, 0xDA) != 0) {
        M2C_FIELD(&D_80162420_163020, s32 *, 0xD4) = (s32) (M2C_FIELD(&D_80162420_163020, s32 *, 0xD4) | 1);
        ((M2C_UNK(*)())&func_80200150_5BC120)();
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08002250_6F9DE0);
    }
}
