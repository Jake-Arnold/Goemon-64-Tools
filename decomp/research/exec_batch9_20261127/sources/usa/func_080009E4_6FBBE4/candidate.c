#include "m2c_types.h"
extern M2C_UNK func_8003521C_35E1C;
extern M2C_UNK func_08000980_6FBB80;

void func_080009E4_6FBBE4(void *arg0, s32 arg1) {
    if (--M2C_FIELD(arg0, u16 *, 0x8A) == 0) {
        M2C_FIELD(arg0, u16 *, 0x8A) = 0x32;
        M2C_FIELD(arg0, f32 *, 0x80) = 0.5f;
        M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
        ((void (*)(void *))&func_8003521C_35E1C)(&func_08000980_6FBB80);
    }
}
