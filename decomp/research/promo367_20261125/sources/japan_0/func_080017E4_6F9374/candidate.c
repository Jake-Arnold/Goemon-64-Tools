#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern u16 D_80162420_163020;
extern M2C_UNK func_08001880_6F9410;

void func_080017E4_6F9374(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;

    if (((s32) D_80162420_163020 % 2) <= 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & ~0x20);
    } else {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 0x20);
    }
    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = 0x02A007E1;
        M2C_FIELD(arg0, s8 *, 0x75) = 0x19;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_08001880_6F9410, arg0);
    }
}
