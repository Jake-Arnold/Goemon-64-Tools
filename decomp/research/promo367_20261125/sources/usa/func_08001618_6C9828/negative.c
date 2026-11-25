#include "m2c_types.h"
extern char func_8000F420_10020;
extern char func_80024038_24C38;
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern char func_80218DCC_5D429C;
M2C_UNK func_08001730_6C9940();                     /* static */
extern f64 D_08006DF0_6CF000;
extern M2C_UNK D_8020CBF0_5C8B00;

void func_08001618_6C9828(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    f32 temp_f0;

    if (((s32(*)())&func_800240DC_24CDC)(0x16C) == 0) {
        temp_f0 = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0xD8) - D_08006DF0_6CF000);
        M2C_FIELD(arg0, f32 *, 0xD8) = temp_f0;
        M2C_FIELD(arg1, f32 *, 0xC) = (f32) (M2C_FIELD(arg1, f32 *, 0xC) + temp_f0);
        if (M2C_FIELD(arg1, f32 *, 0xC) < 310.0f) {
            ((M2C_UNK(*)())&func_80024038_24C38)(0x167);
            ((M2C_UNK(*)())&func_8000F420_10020)(0x2A2, &D_8020CBF0_5C8B00, arg1, 0x44960000);
            M2C_FIELD(arg1, f32 *, 0xC) = 310.0f;
            M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
            M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
            M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
            ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 6, 0x3E800000, 4);
            ((M2C_UNK(*)())&func_80218DCC_5D429C)(arg0, 7);
            ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08001730_6C9940);
        }
    }
}
