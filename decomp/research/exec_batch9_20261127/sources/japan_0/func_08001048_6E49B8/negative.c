#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);
extern M2C_UNK func_080010A4_6E4A14;

void func_08001048_6E49B8(void *arg0, void *arg1) {
    if (!(M2C_FIELD(arg1, f32 *, 0x28) < 15.0f)) {
        M2C_FIELD(arg0, s32 *, 0x60) &= ~1;
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x1E;
        ((void (*)(M2C_UNK *))func_80034E8C_35A8C)(&func_080010A4_6E4A14);
    }

    *(volatile s32 *)0x80000000 = 1;
}
