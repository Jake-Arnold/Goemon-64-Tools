#include "m2c_types.h"

extern void func_801F0540_61B920(void *);

void func_801F65B8_621998(void *arg0, void *arg1) {
    if ((f32) (u32) M2C_FIELD(arg1, u16 *, 0x16) != M2C_FIELD(arg0, f32 *, 0x90)) {
        M2C_FIELD(arg1, u16 *, 0x16) += 0x20;
        return;
    }
    M2C_FIELD(arg0, f32 *, 0x70) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    func_801F0540_61B920(arg0);
}
