#include "m2c_types.h"
extern f64 D_801F45F8_662AE8;

void func_801D5318_643808(void *arg0, M2C_UNK arg1) {
    s32 temp_f16;

    temp_f16 = (s32) ((f64) M2C_FIELD(arg0, s32 *, 0xB4) + D_801F45F8_662AE8);
    if (temp_f16 >= 0x6D60) {
        M2C_FIELD(arg0, s8 *, 0x9E) = 1;
    }
    M2C_FIELD(arg0, s32 *, 0xB4) = temp_f16;
}
