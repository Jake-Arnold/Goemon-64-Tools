#include "m2c_types.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);
M2C_UNK func_8021664C_5D1B1C(void *, s32, f32, s32);
extern M2C_UNK func_08001058_6E8368;

void func_08001004_6E8314(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        ((void (*)(void *, s32, f32, s32))func_8021664C_5D1B1C)(arg0, 0, 1.0f / 3.0f, 1);
        ((void (*)(M2C_UNK *))func_8003521C_35E1C)(&func_08001058_6E8368);
    }
}
