#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_80226CE0_5E2270;
M2C_UNK func_08000220_72AAD0();                     /* static */
s32 func_08002B30_72D3E0();                         /* static */
extern void *D_80201514_5BD4E4;

void func_080001AC_72AA5C(void *arg0, M2C_UNK arg1) {
    if ((M2C_FIELD(D_80201514_5BD4E4, u8 *, 0x4C) == 0x1E) && (func_08002B30_72D3E0() != 0)) {
        ((M2C_UNK(*)())&func_80226CE0_5E2270)();
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x1E;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08000220_72AAD0);
    }
}
