#include "m2c_types.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);
extern M2C_UNK func_080010A4_6E0244;

void func_08001048_6E01E8(void *arg0, void *arg1) {
    if (!(M2C_FIELD(arg1, f32 *, 0x28) < 15.0f)) {
        M2C_FIELD(arg0, s32 *, 0x60) &= ~1;
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x1E;
        ((void (*)(M2C_UNK *))func_8003521C_35E1C)(&func_080010A4_6E0244);
    }

    *(volatile s32 *)0x80000000 = 1;
}
