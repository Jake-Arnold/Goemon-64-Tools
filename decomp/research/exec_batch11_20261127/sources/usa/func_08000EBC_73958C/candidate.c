#include "m2c_types.h"
extern u8 func_8021664C_5D1B1C[];

void func_08000EBC_73958C(void *arg0, M2C_UNK arg1, f32 arg2) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x18);
    ((M2C_UNK (*)(void *, M2C_UNK, f32))func_8021664C_5D1B1C)(arg0, arg1, arg2);
    M2C_FIELD(temp_v0, s32 *, 0x2C) = (M2C_FIELD(temp_v0, s32 *, 0x2C) & 0x8FFFFFFF) + 0x10000000;
}
