#include "m2c_types.h"
void func_08004FE4_6C91A4(void *arg0, void *arg1) {
    M2C_FIELD(arg1, u16 *, 0x16) = (u16) ((M2C_FIELD(arg1, u16 *, 0x16) + 2) & 0x3FF);
    if (M2C_FIELD(arg1, f32 *, 0xC) > 80.0f) {
        M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
    }
}
