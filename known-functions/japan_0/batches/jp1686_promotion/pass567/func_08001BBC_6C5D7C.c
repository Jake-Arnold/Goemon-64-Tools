#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_08001C10_6C5DD0();                     /* static */

void func_08001BBC_6C5D7C(void *arg0, void *arg1) {
    M2C_FIELD(arg0, s32 *, 0x60) = 0x2006E1;
    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
    M2C_FIELD(arg1, f32 *, 0xC) = -93.0f;
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08001C10_6C5DD0);
}
