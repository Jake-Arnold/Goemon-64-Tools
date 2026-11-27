#include "m2c_types.h"
extern f32 D_08008A24_6C8174;

void func_08004AB4_6C4204(s32 arg0, void *arg1) {
    f32 val;

    val = D_08008A24_6C8174;
    M2C_FIELD(arg1, u16 *, 0x14) = (u16) ((M2C_FIELD(arg1, u16 *, 0x14) + 0x20) & 0x3FF);
    M2C_FIELD(arg1, f32 *, 0x24) = val;
    M2C_FIELD(arg1, f32 *, 0x20) = val;
    M2C_FIELD(arg1, f32 *, 0x1C) = val;
}
