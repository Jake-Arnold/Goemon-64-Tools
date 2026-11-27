#include "m2c_types.h"
extern u8 func_8021B09C_5D656C[];
extern u8 func_8021B73C_5D6C0C[];

void func_08000A20_6EF380(void *arg0, void *arg1) {
    M2C_FIELD(arg0, s16 *, 0xD4) = 4;
    M2C_FIELD(arg1, u16 *, 0x16) = (u16) ((M2C_FIELD(arg1, u16 *, 0x16) + 3) & 0x3FF);
    if (((s32 (*)(void *, f32))func_8021B73C_5D6C0C)(arg0, 300.0f) != 0) {
        ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK))func_8021B09C_5D656C)(arg0, 0, 1);
    }

    *(volatile int *)0x80000000 = 1;
}
