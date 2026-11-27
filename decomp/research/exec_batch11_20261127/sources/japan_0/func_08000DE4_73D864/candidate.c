#include "m2c_types.h"
extern u8 func_8021B3BC_5D694C[];

void func_08000DE4_73D864(void *arg0, M2C_UNK arg1, f32 arg2) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x18);
    ((M2C_UNK (*)(void *, M2C_UNK, f32))func_8021B3BC_5D694C)(arg0, arg1, arg2);
    M2C_FIELD(temp_v0, s32 *, 0x2C) = (M2C_FIELD(temp_v0, s32 *, 0x2C) & 0x8FFFFFFF) + 0x10000000;
}
