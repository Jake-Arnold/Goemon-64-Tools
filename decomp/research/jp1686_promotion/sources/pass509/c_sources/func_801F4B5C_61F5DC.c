#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)(), void *); /* extern */
M2C_UNK func_801F4C04_61F684();                     /* static */
M2C_UNK func_801FC74C_6271CC();                     /* static */
extern void *D_80214600_63F080;
extern void *D_80214660_63F0E0;

void func_801F4B5C_61F5DC(void *arg0, void *arg1) {
    M2C_FIELD(D_80214660_63F0E0, s8 *, 0xC) = 1;
    M2C_FIELD(arg1, s8 *, 0x64) = 1;
    func_801FC74C_6271CC();
    M2C_FIELD(arg1, f32 *, 8) = 500.0f;
    M2C_FIELD(arg1, f32 *, 0xC) = -100.0f;
    M2C_FIELD(arg1, f32 *, 0x10) = -300.0f;
    if (M2C_FIELD(D_80214600_63F080, u8 *, 0x2C1) == 1) {
        M2C_FIELD(arg1, s16 *, 0x14) = 0;
        M2C_FIELD(arg1, s16 *, 0x16) = 0x300;
        M2C_FIELD(arg1, s16 *, 0x18) = 0;
        M2C_FIELD(arg0, f32 *, 0x70) = -6.0f;
        M2C_FIELD(arg1, s8 *, 0x64) = 0;
        func_80034E8C_35A8C(func_801F4C04_61F684, arg1);
    }
}
