#include "m2c_types.h"
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern char func_80218DCC_5D429C;
M2C_UNK func_08000F70_6C9180();                     /* static */
extern f64 D_08006DC0_6CEFD0;

void func_08000E98_6C90A8(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    f32 temp_f0;

    if (((s32(*)())&func_800240DC_24CDC)(0x16C) == 0) {
        temp_f0 = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0xD8) - D_08006DC0_6CEFD0);
        M2C_FIELD(arg0, f32 *, 0xD8) = temp_f0;
        M2C_FIELD(arg1, f32 *, 0xC) = (f32) (M2C_FIELD(arg1, f32 *, 0xC) + temp_f0);
        if (M2C_FIELD(arg0, f32 *, 0xD8) < 0.0f) {
            M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & 0xFEFFFFFF);
            ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 0x10, 0x3F000000, 4);
            ((M2C_UNK(*)())&func_80218DCC_5D429C)(arg0, 0x11);
            ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08000F70_6C9180);
        }
    }
}
