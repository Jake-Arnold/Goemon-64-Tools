#include "m2c_types.h"
extern char func_80024088_24C88;
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern M2C_UNK func_08002A38_6B1E48;
extern M2C_UNK func_08002DF4_6B2204;

void func_0800295C_6B1D6C(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s32 *, 0x60) = 0x80000220;
    M2C_FIELD(arg0, s8 *, 0x6C) = 0;
    M2C_FIELD(arg0, s32 *, 0xD0) = 0;
    if (((s32 (*)(M2C_UNK))&func_800240DC_24CDC)(0x98) != 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 0x01000001);
        ((M2C_UNK  (*)(void *, M2C_UNK, f32, M2C_UNK))&func_8021664C_5D1B1C)(arg0, 0, 0.0f, 0);
        ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_08002DF4_6B2204);
        return;
    }
    ((M2C_UNK  (*)(void *, M2C_UNK, f32, M2C_UNK))&func_8021664C_5D1B1C)(arg0, 0, 0.0f, 1);
    ((M2C_UNK (*)(M2C_UNK))&func_80024088_24C88)(0x5D);
    ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_08002A38_6B1E48);

    *(volatile s32 *)0x80000000 = 1;
}
