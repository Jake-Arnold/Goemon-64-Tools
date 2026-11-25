#include "m2c_types.h"
extern char func_80023CF8_248F8;
extern char func_80034E8C_35A8C;
extern M2C_UNK func_08008628_6C03A8;

void func_080085C0_6C0340(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        ((M2C_UNK(*)())&func_80023CF8_248F8)(0x12F, arg0);
        M2C_FIELD(arg0, u16 *, 0x8A) = 0x78U;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_08008628_6C03A8, arg0);
    }
}
