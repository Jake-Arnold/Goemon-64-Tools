#include "m2c_types.h"
extern u8 func_8003521C_35E1C[];
extern u8 func_802196FC_5D4BCC[];
extern u8 func_08002610_6D8560[];

void func_080025A0_6D84F0(void *arg0, M2C_UNK arg1) {
    if (((s32 (*)(void *, f32, f32, f32, s32))func_802196FC_5D4BCC)(arg0, (f32) M2C_FIELD(arg0, s16 *, 0xA0), 0.0f, (f32) M2C_FIELD(arg0, s16 *, 0xA2), 8) == 0) {
        ((void (*)(void *))func_8003521C_35E1C)(func_08002610_6D8560);
    }

    *(volatile int *)0x80000000 = 1;
}
