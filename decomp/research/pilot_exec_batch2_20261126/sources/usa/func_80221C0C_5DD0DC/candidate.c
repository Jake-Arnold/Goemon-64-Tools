#include "m2c_types.h"
M2C_UNK func_8021664C_5D1B1C(void *, s32);

void func_80221C0C_5DD0DC(void *arg0, s32 arg1, f32 arg2) {
    func_8021664C_5D1B1C(arg0, arg1);
    M2C_FIELD(arg0, s16 *, 0xA8) = (s16) (u32) (arg2 * 256.0f);
}
