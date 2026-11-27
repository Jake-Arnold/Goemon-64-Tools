#include "m2c_types.h"
extern char func_08004E04_6DECD4;
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern f64 D_08005238_6DF108;
extern M2C_UNK func_0800097C_6DA84C;

void func_080008D8_6DA7A8(void *arg0, void *arg1) {
    M2C_FIELD(arg0, f32 *, 0x7C) = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0x7C) + D_08005238_6DF108);
    ((M2C_UNK  (*)(void *, s32, f32, s32))&func_08004E04_6DECD4)(arg0, M2C_FIELD(arg0, s32 *, 0x78), M2C_FIELD(arg0, f32 *, 0x7C), M2C_FIELD(arg0, s32 *, 0x80));
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))&func_8021664C_5D1B1C)(arg0, 1, 0x3F800000, 1);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x12C;
        ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_0800097C_6DA84C);
    }

    *(volatile s32 *)0x80000000 = 1;
}
