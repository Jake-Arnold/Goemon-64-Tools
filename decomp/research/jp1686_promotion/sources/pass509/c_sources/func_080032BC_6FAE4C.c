#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_80038808_39408;
M2C_UNK func_08003338_6FAEC8();                     /* static */
extern M2C_UNK D_801624C8_1630C8;

void func_080032BC_6FAE4C(void *arg0, M2C_UNK arg1) {
    if ((M2C_FIELD(arg0, u8 *, 0xD1) == 0) && ((s32) M2C_FIELD(arg0, u8 *, 0xD2) < (s32) M2C_FIELD(&D_801624C8_1630C8, u8 *, 0x90))) {
        ((M2C_UNK(*)())&func_80038808_39408)(0x224, arg0);
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 1);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08003338_6FAEC8, arg0);
    }
}
