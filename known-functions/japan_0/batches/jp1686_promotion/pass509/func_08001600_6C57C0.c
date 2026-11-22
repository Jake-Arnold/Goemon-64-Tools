#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_80038808_39408;
M2C_UNK func_0800166C_6C582C();                     /* static */
extern f32 D_080089C4_6CCB84;

void func_08001600_6C57C0(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & 0xFEFFFFFF);
        M2C_FIELD(arg0, f32 *, 0x7C) = (f32) D_080089C4_6CCB84;
        ((M2C_UNK(*)())&func_80038808_39408)(0x154);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_0800166C_6C582C);
    }
}
