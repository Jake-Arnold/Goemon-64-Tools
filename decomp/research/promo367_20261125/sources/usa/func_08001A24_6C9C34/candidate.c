#include "m2c_types.h"
extern char func_8000F420_10020;
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
M2C_UNK func_08001B1C_6C9D2C();                     /* static */
extern M2C_UNK D_8020CBF0_5C8B00;

void func_08001A24_6C9C34(void *arg0, void *arg1) {
    f64 temp_f0;

    if (((s32(*)())&func_800240DC_24CDC)(0x16C) == 0) {
        temp_f0 = (f64) M2C_FIELD(arg1, f32 *, 0x28);
        if (temp_f0 < 4.0) {
            if (temp_f0 > 1.0) {
                M2C_FIELD(arg1, u16 *, 0x16) = (u16) (M2C_FIELD(arg1, u16 *, 0x16) - 4);
            }
        } else {
            M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 0x01000000);
            ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 8, 0x3E800000, 4);
            M2C_FIELD(arg1, f32 *, 0x28) = 4.0f;
            ((M2C_UNK(*)())&func_8000F420_10020)(0x271, &D_8020CBF0_5C8B00, arg1, 0x44960000);
            ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08001B1C_6C9D2C);
        }
    }
}
