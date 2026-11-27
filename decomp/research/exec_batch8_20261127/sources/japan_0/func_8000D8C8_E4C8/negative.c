#include "m2c_types.h"
extern void *D_8016D430_16E030[];

void func_8000D8C8_E4C8(s32 arg0) {
    void *temp_v0;

    temp_v0 = D_8016D430_16E030[arg0];
    if (temp_v0 != NULL) {
        M2C_FIELD(temp_v0, u64 *, 0x10) &= ~(u64)2;
        M2C_FIELD(temp_v0, f32 *, 0x4C) = 0.0f;
    }

    *(volatile s32 *)0x80000000 = 1;
}
