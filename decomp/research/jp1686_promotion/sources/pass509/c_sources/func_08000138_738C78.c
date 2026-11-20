#include "m2c_types.h"
extern char func_80023B54_24754;
extern char func_80034B44_35744;
extern char func_80034E8C_35A8C;
extern char func_80226CE0_5E2270;
M2C_UNK func_080001BC_738CFC();                     /* static */
extern void *D_80201534_5BD504;

void func_08000138_738C78(s32 arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80023B54_24754)(0) != 0) {
        if (M2C_FIELD(D_80201534_5BD504, u8 *, 0x61) != 0) {
            ((M2C_UNK(*)())&func_80034B44_35744)();
            return;
        }
        ((M2C_UNK(*)())&func_80226CE0_5E2270)();
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080001BC_738CFC);
    }
}
