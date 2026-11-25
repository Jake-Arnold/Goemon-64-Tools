#include "m2c_types.h"
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern char func_80218DCC_5D429C;
M2C_UNK func_08001618_6C9828();                     /* static */
extern f64 D_08006DE8_6CEFF8;

void func_08001540_6C9750(void *arg0, void *arg1) {
    f32 temp_f0;

    if (((s32(*)())&func_800240DC_24CDC)(0x16C) == 0) {
        temp_f0 = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0xD8) - D_08006DE8_6CEFF8);
        M2C_FIELD(arg0, f32 *, 0xD8) = temp_f0;
        M2C_FIELD(arg1, f32 *, 0xC) = (f32) (M2C_FIELD(arg1, f32 *, 0xC) + temp_f0);
        if (M2C_FIELD(arg0, f32 *, 0xD8) < 0.0f) {
            M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & 0xFEFFFFFF);
            ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 0xC, 0x3F000000, 4);
            ((M2C_UNK(*)())&func_80218DCC_5D429C)(arg0, 0xC);
            ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08001618_6C9828);
        }
    }
}
