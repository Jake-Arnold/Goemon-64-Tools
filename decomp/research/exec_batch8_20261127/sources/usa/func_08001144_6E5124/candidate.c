#include "m2c_types.h"
extern M2C_UNK func_8003521C_35E1C;
extern M2C_UNK func_080011A0_6E5180;

void func_08001144_6E5124(void *arg0, M2C_UNK arg1) {
    if (!(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        M2C_FIELD(arg0, s32 *, 0x60) = 0x02A007C1;
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x28;
        M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
        ((void (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_080011A0_6E5180);
    }
}
