#include "m2c_types.h"
extern char func_8000F420_10020;
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern M2C_UNK D_8020CBF0_5C8B00;
extern M2C_UNK func_08000720_6D41B0;

void func_08000664_6D40F4(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    u16 temp_v0;

    temp_v0 = M2C_FIELD(arg1, u16 *, 0x14);
    if (temp_v0 != 0x300) {
        M2C_FIELD(arg1, u16 *, 0x14) = (u16) ((temp_v0 - 0x20) & 0x3FF);
    } else {
        M2C_FIELD(arg0, s8 *, 0x9B) = (s8) -M2C_FIELD(arg0, u8 *, 0x9A);
    }
    if (!(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        ((M2C_UNK(*)())&func_8000F420_10020)(0x262, &D_8020CBF0_5C8B00, arg1, 0x43C80000);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x1E;
        M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
        ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 3, 0x3E800000, 1);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_08000720_6D41B0);
    }
}
