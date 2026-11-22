#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_80200150_5BC120;
extern char func_80226C2C_5E21BC;
extern char func_80226CE0_5E2270;
M2C_UNK func_080012C0_6F8E50();                     /* static */
extern M2C_UNK D_80162420_163020;

void func_08001238_6F8DC8(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_80226CE0_5E2270)();
    ((M2C_UNK(*)())&func_80226C2C_5E21BC)();
    M2C_FIELD(&D_80162420_163020, s32 *, 0xD4) = (s32) (M2C_FIELD(&D_80162420_163020, s32 *, 0xD4) | 1);
    if (M2C_FIELD(arg0, s32 *, 0xEC) & 2) {
        ((M2C_UNK(*)())&func_80200150_5BC120)();
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080012C0_6F8E50);
    }
}
