#include "m2c_types.h"
void func_8021664C_5D1B1C(M2C_UNK, M2C_UNK, f32, s32);

void func_080007CC_73C3CC(M2C_UNK arg0, M2C_UNK arg1, f32 arg2) {
    void (*fn)(M2C_UNK, M2C_UNK, f32, s32);

    fn = func_8021664C_5D1B1C;
    fn(arg0, arg1, arg2, 1);

    *(volatile s32 *)0x80000000 = 1;
}
