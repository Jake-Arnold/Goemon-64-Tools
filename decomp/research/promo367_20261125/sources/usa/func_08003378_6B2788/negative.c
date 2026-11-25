#include "m2c_types.h"
extern char func_8000F3D8_FFD8;
extern char func_8003521C_35E1C;
extern char func_80216DF8_5D22C8;
extern char func_8021A310_5D57E0;
extern char func_80224ABC_5DFF8C;
extern M2C_UNK D_8020CBF0_5C8B00;
extern M2C_UNK func_08003438_6B2848;

void func_08003378_6B2788(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        ((M2C_UNK(*)())&func_8000F3D8_FFD8)(0x105, &D_8020CBF0_5C8B00, arg1, 0x43C80000);
        M2C_FIELD(arg0, s16 *, 0x5E) = 0x7E;
        M2C_FIELD(arg0, s32 *, 0x60) = 0x222;
        M2C_FIELD(arg0, u8 *, 0xD0) = 0xFC;
        ((M2C_UNK(*)())&func_80216DF8_5D22C8)(arg0, 3);
        ((M2C_UNK(*)())&func_8021A310_5D57E0)(arg0);
        ((M2C_UNK(*)())&func_80224ABC_5DFF8C)(arg0, 0, 0x3FC00000, 0);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_08003438_6B2848);
    }
}
