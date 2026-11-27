#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_802197D8_5D4CA8;
extern M2C_UNK func_080030F0_6DCFC0;

void func_08003084_6DCF54(void *arg0, void *arg1) {
    void *temp_v0;

    if (((s32  (*)(void *, M2C_UNK))&func_802197D8_5D4CA8)(arg0, 0x10) == 0) {
        M2C_FIELD(arg1, s8 *, 0x7C) = 1;
        temp_v0 = M2C_FIELD(arg0, void **, 0x84);
        M2C_FIELD(arg0, f32 *, 0xDC) = (f32) M2C_FIELD(temp_v0, f32 *, 8);
        M2C_FIELD(arg0, f32 *, 0xE0) = (f32) M2C_FIELD(temp_v0, f32 *, 0x10);
        ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_080030F0_6DCFC0);
    }

    *(volatile s32 *)0x80000000 = 1;
}
