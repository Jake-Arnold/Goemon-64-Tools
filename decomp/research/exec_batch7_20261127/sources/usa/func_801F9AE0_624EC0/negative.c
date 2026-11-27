#include "m2c_types.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);
extern f64 D_8020E8B0_639C90;
extern void *D_8020EED0_63A2B0;
extern M2C_UNK func_801F9B74_624F54;

void func_801F9AE0_624EC0(void *arg0, M2C_UNK arg1) {
    f32 *temp = &M2C_FIELD(D_8020EED0_63A2B0, f32 *, 0xA0);
    *temp = (f32) ((f64) *temp - D_8020E8B0_639C90);
    if (*temp <= -80.0f) {
        *temp = -80.0f;
        M2C_FIELD(D_8020EED0_63A2B0, s8 *, 0x2C1) = 5;
        M2C_FIELD(arg0, s32 *, 0x7C) = 0xA0;
        M2C_FIELD(arg0, s32 *, 0x80) = 0x32;
        func_8003521C_35E1C(&func_801F9B74_624F54);
    }

    *(volatile s32 *)0x80000000 = 1;
}
