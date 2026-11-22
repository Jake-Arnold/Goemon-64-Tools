#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8021BB68_5D70F8;
extern char func_8021EB78_5DA108;
M2C_UNK func_08001A04_6B5904();                     /* static */
M2C_UNK func_08001AD8_6B59D8();                     /* static */

void func_08001D9C_6B5C9C(void *arg0, void *arg1) {
    func_08001A04_6B5904();
    M2C_FIELD(arg0, s8 *, 0x6C) = 0;
    M2C_FIELD(arg0, s16 *, 0x5E) = 0x2F2;
    ((M2C_UNK(*)())&func_8021BB68_5D70F8)(arg0, 0);
    M2C_FIELD(arg1, s16 *, 0x14) = 0;
    M2C_FIELD(arg1, s16 *, 0x16) = 0;
    M2C_FIELD(arg1, s16 *, 0x18) = 0;
    M2C_FIELD(arg1, f32 *, 8) = 20.0f;
    M2C_FIELD(arg1, f32 *, 0xC) = -36.0f;
    M2C_FIELD(arg1, f32 *, 0x10) = -9.0f;
    ((M2C_UNK(*)())&func_8021EB78_5DA108)(arg0, 0x3F000000, arg1);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08001AD8_6B59D8);
}
