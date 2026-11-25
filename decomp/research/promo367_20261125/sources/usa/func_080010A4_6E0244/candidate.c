#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern M2C_UNK func_08000F20_6E00C0;

void func_080010A4_6E0244(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 1);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_08000F20_6E00C0);
    }
}
