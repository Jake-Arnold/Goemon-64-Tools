#include "m2c_types.h"
extern char func_08003058_6E7038;
extern char func_8003521C_35E1C;
extern char func_80218D90_5D4260;
extern char func_8021BB04_5D6FD4;
extern M2C_UNK func_08000A30_6E4A10;

void func_08000974_6E4954(void *arg0, void *arg1) {
    ((M2C_UNK  (*)(void *, M2C_UNK))&func_08003058_6E7038)(arg0, 1);
    if (((s32 (*)(void *, f32, f32, M2C_UNK))&func_8021BB04_5D6FD4)(arg0, (f32) M2C_FIELD(arg0, s16 *, 0xA0), (f32) M2C_FIELD(arg0, s16 *, 0xA2), 0x40000000) == 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = 0x02A00FE1;
        M2C_FIELD(arg0, s8 *, 0x75) = 0x14;
        M2C_FIELD(arg1, s16 *, 0x14) = 0;
        ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK, s32))&func_80218D90_5D4260)(arg0, 0xA, 0xA, 0xA, 0);
        ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_08000A30_6E4A10);
    }

    *(volatile s32 *)0x80000000 = 1;
}
