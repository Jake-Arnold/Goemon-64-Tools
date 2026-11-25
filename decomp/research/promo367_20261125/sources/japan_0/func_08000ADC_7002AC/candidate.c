#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern M2C_UNK func_08000A98_700268;

void func_08000ADC_7002AC(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        M2C_FIELD(arg0, u16 *, 0x8A) = 0x28U;
        M2C_FIELD(arg0, f32 *, 0x78) = -0.5f;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_08000A98_700268);
    }
}
