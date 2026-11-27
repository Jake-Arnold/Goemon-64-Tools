#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern char func_8021B424_5D68F4;
extern M2C_UNK func_080040A8_6DDF78;

void func_0800401C_6DDEEC(void *arg0, void *arg1) {
    ((M2C_UNK  (*)(void *, u16, M2C_UNK))&func_8021B424_5D68F4)(arg0, M2C_FIELD(arg0, u16 *, 0xDC), 0x3F4CCCCD);
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
        ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))&func_8021664C_5D1B1C)(arg0, 1, 0x3E800000, 2);
        ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_080040A8_6DDF78);
    }

    *(volatile s32 *)0x80000000 = 1;
}
