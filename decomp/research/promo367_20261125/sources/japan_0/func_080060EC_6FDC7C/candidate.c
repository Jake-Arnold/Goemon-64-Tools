#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_80038808_39408;
extern M2C_UNK func_0800614C_6FDCDC;

void func_080060EC_6FDC7C(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 1);
        ((M2C_UNK(*)())&func_80038808_39408)(0x224);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_0800614C_6FDCDC);
    }
}
