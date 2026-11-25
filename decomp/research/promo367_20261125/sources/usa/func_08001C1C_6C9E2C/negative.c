#include "m2c_types.h"
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
M2C_UNK func_08000970_6C8B80();                     /* static */

void func_08001C1C_6C9E2C(s32 arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    f64 temp_f0;

    if (((s32(*)())&func_800240DC_24CDC)(0x16C) == 0) {
        if (!(M2C_FIELD(arg1, u8 *, 0x7C) & 2)) {
            temp_f0 = (f64) M2C_FIELD(arg1, f32 *, 0x28);
            if ((temp_f0 > 1.0) && (temp_f0 < 4.0)) {
                M2C_FIELD(arg1, u16 *, 0x16) = (u16) (M2C_FIELD(arg1, u16 *, 0x16) + 4);
            }
        } else {
            ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08000970_6C8B80, arg1);
        }
    }
}
