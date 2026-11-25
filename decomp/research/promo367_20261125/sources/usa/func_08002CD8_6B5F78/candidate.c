#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern M2C_UNK func_08002D2C_6B5FCC;

void func_08002CD8_6B5F78(void *arg0, void *arg1) {
    s32 temp_v0;

    M2C_FIELD(arg1, u16 *, 0x16) = (u16) ((M2C_FIELD(arg1, u16 *, 0x16) - 1) & 0x3FF);
    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        M2C_FIELD(arg0, u16 *, 0x8A) = 0xAU;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_08002D2C_6B5FCC);
    }
}
