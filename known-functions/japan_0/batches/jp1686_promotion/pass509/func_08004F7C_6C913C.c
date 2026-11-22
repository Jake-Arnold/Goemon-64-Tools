#include "m2c_types.h"
extern char func_80023B54_24754;
extern char func_80034E8C_35A8C;
extern char func_80038808_39408;
M2C_UNK func_08004FE4_6C91A4();                     /* static */
extern f32 D_08008A44_6CCC04;

void func_08004F7C_6C913C(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80023B54_24754)(0) != 0) {
        M2C_FIELD(arg0, f32 *, 0x7C) = (f32) D_08008A44_6CCC04;
        ((M2C_UNK(*)())&func_80038808_39408)(0x2AD);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08004FE4_6C91A4);
    }
}
