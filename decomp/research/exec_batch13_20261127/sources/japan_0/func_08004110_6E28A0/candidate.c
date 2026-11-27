#include "m2c_types.h"

extern u8 func_80034E8C_35A8C[];
extern u8 func_8021B3BC_5D694C[];
extern u8 func_080041C8_6E2958[];

void func_08004110_6E28A0(M2C_UNK arg0, void *arg1) {
    s32 temp_t6;

    if ((4.0f <= M2C_FIELD(arg1, f32 *, 0x28)) && (M2C_FIELD(arg1, f32 *, 0x28) < 5.0f)) {
        temp_t6 = (s32) M2C_FIELD(arg1, u16 *, 0x7E) / 2;
        if (temp_t6 > 0) {
            M2C_FIELD(arg1, u16 *, 0x7E) = (u16) temp_t6;
            return;
        }
        M2C_FIELD(arg1, u16 *, 0x7E) = 0x40U;
        return;
    }
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        ((void (*)(M2C_UNK, s32, s32, s32))func_8021B3BC_5D694C)(arg0, 3, 0x3E800000, 4);
        ((void (*)(u8 *))func_80034E8C_35A8C)(func_080041C8_6E2958);
    }
}
