#include "m2c_types.h"
extern char func_80023B54_24754;
extern char func_80034E8C_35A8C;
extern char func_80038808_39408;
M2C_UNK func_08000530_7121A0();                     /* static */

void func_08000598_712208(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80023B54_24754)(1) != 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 1);
        ((M2C_UNK(*)())&func_80038808_39408)(0x15E);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08000530_7121A0);
    }
}
