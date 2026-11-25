#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern M2C_UNK func_080013E4_6C55A4;

void func_08001388_6C5548(void *arg0, void *arg1) {
    s32 temp_v0;

    M2C_FIELD(arg1, f32 *, 0xC) = (f32) ((f64) M2C_FIELD(arg1, f32 *, 0xC) + 0.5);
    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_080013E4_6C55A4);
    }
}
