#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern M2C_UNK func_080054A4_6C4BF4;

void func_0800551C_6C4C6C(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        M2C_FIELD(arg0, f32 *, 0xDC) = (f32) (M2C_FIELD(arg0, f32 *, 0xDC) + 1.0f);
        if (M2C_FIELD(arg0, f32 *, 0xDC) > 8.0f) {
            M2C_FIELD(arg0, f32 *, 0xDC) = 1.0f;
        }
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_080054A4_6C4BF4);
    }
}
