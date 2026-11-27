#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8021E548_5D9AD8;
extern M2C_UNK func_08003044_6E17D4;

void func_08002FD8_6E1768(void *arg0, void *arg1) {
    void *temp_v0;

    if (((s32  (*)(void *, M2C_UNK))&func_8021E548_5D9AD8)(arg0, 0x10) == 0) {
        M2C_FIELD(arg1, s8 *, 0x7C) = 1;
        temp_v0 = M2C_FIELD(arg0, void **, 0x84);
        M2C_FIELD(arg0, f32 *, 0xDC) = (f32) M2C_FIELD(temp_v0, f32 *, 8);
        M2C_FIELD(arg0, f32 *, 0xE0) = (f32) M2C_FIELD(temp_v0, f32 *, 0x10);
        ((M2C_UNK (*)(M2C_UNK *))&func_80034E8C_35A8C)(&func_08003044_6E17D4);
    }
}
