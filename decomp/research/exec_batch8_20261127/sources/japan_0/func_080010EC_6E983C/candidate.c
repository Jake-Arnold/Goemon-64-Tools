#include "m2c_types.h"
extern M2C_UNK func_80034E8C_35A8C;
extern M2C_UNK func_08001148_6E9898;

void func_080010EC_6E983C(void *arg0, M2C_UNK arg1) {
    if (!(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        M2C_FIELD(arg0, s32 *, 0x60) = 0x02A007C1;
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x28;
        M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
        ((void (*)(M2C_UNK *))&func_80034E8C_35A8C)(&func_08001148_6E9898);
    }
}
