#include "m2c_types.h"

extern u8 func_8003521C_35E1C[];
extern u8 func_8021664C_5D1B1C[];
extern u8 func_080048FC_6DE7CC[];

void func_0800484C_6DE71C(M2C_UNK arg0, void *arg1) {
    s32 temp_t6;

    if ((4.0f <= M2C_FIELD(arg1, f32 *, 0x28)) && (M2C_FIELD(arg1, f32 *, 0x28) < 5.0f)) {
        temp_t6 = (s32) M2C_FIELD(arg1, u16 *, 0x7E) / 2;
        if (temp_t6 > 0) {
            M2C_FIELD(arg1, u16 *, 0x7E) = (u16) temp_t6;
        } else {
            M2C_FIELD(arg1, u16 *, 0x7E) = 0x40U;
        }
    }
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        ((void (*)(M2C_UNK, s32, s32, s32))func_8021664C_5D1B1C)(arg0, 3, 0x3E800000, 4);
        ((void (*)(u8 *))func_8003521C_35E1C)(func_080048FC_6DE7CC);
    }
}
