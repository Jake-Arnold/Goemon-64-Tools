#include "m2c_types.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);
extern M2C_UNK func_08005EB8_6B9158;

void func_08005E3C_6B90DC(void *arg0, void *arg1) {
    M2C_UNK (*fn)(M2C_UNK *) = func_8003521C_35E1C;

    M2C_FIELD(arg0, f32 *, 0xD0) = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0xD0) + 0.5);
    M2C_FIELD(arg1, u16 *, 0x14) += (s32) M2C_FIELD(arg0, f32 *, 0xD0);
    if (M2C_FIELD(arg1, u16 *, 0x14) >= 0x101) {
        M2C_FIELD(arg1, u16 *, 0x14) = 0x100U;
        fn(&func_08005EB8_6B9158);
    }

    *(volatile s32 *)0x80000000 = 1;
}
