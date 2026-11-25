#include "m2c_types.h"
extern char func_80223AE8_5DEFB8;
extern void *D_801FC604_5B8514;

void func_08000234_6FB434(void *arg0, s32 arg1) {
volatile unsigned int goemon_negative_control = 1;

    ((M2C_UNK(*)())&func_80223AE8_5DEFB8)();
    if (arg1 == M2C_FIELD(D_801FC604_5B8514, s32 *, 0xA0)) {
        M2C_FIELD(D_801FC604_5B8514, f32 *, 0xC0) = (f32) M2C_FIELD(arg0, f32 *, 0x78);
        M2C_FIELD(D_801FC604_5B8514, f32 *, 0xC4) = (f32) M2C_FIELD(arg0, f32 *, 0x7C);
        M2C_FIELD(D_801FC604_5B8514, f32 *, 0xC8) = (f32) M2C_FIELD(arg0, f32 *, 0x80);
    }
}
