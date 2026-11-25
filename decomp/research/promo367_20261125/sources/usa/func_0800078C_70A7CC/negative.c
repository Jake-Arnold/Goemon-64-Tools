#include "m2c_types.h"
extern char func_080006C4_70A704;
extern char func_8003521C_35E1C;
extern char func_8021A764_5D5C34;
extern char func_80221C0C_5DD0DC;
extern M2C_UNK D_8007D40;
extern M2C_UNK func_08000764_70A7A4;

void func_0800078C_70A7CC(s32 arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    ((M2C_UNK(*)())&func_080006C4_70A704)(arg0, 0x12800761);
    ((M2C_UNK(*)())&func_80221C0C_5DD0DC)(arg0, 0, 0x3E000000, 1);
    ((M2C_UNK(*)())&func_8021A764_5D5C34)(arg0, &D_8007D40, 3, 2);
    M2C_FIELD(arg1, s16 *, 0x16) = 0x100;
    M2C_FIELD(arg1, f32 *, 8) = -60.0f;
    M2C_FIELD(arg1, f32 *, 0xC) = 7.0f;
    M2C_FIELD(arg1, f32 *, 0x10) = 0.0f;
    ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_08000764_70A7A4);
}
