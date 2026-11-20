#include "m2c_types.h"
extern char func_80023B54_24754;
extern char func_80034E8C_35A8C;
M2C_UNK func_08001920_6C5AE0();                     /* static */
extern f32 D_080089D0_6CCB90;

void func_080018C8_6C5A88(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80023B54_24754)(7) != 0) {
        M2C_FIELD(arg0, f32 *, 0x7C) = (f32) D_080089D0_6CCB90;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08001920_6C5AE0);
    }
}
