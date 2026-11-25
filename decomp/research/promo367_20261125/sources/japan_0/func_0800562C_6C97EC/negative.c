#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_80038808_39408;
extern M2C_UNK func_0800568C_6C984C;

void func_0800562C_6C97EC(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 1);
        ((M2C_UNK(*)())&func_80038808_39408)(0x124);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_0800568C_6C984C);
    }
}
