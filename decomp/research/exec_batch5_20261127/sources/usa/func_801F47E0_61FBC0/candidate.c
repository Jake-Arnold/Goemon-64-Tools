#include "m2c_types.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);
M2C_UNK func_801D2EE4_5FE2C4(s32, M2C_UNK *, void *);
M2C_UNK func_801F7074_622454();
extern M2C_UNK D_8020B2D0_6366B0;
extern M2C_UNK func_801F4860_61FC40;

void func_801F47E0_61FBC0(void *arg0, s32 arg1) {
    f32 div;

    div = 2.0f;
    func_801F7074_622454();
    M2C_FIELD(arg0, f32 *, 0x74) = 14.0f;
    M2C_FIELD(arg0, f32 *, 0x70) = M2C_FIELD(arg0, f32 *, 0x70) / div;
    M2C_FIELD(arg0, f32 *, 0x78) = M2C_FIELD(arg0, f32 *, 0x78) / div;
    func_801D2EE4_5FE2C4(arg1, &D_8020B2D0_6366B0, arg0);
    M2C_FIELD(arg0, s32 *, 0xE8) = M2C_FIELD(arg0, s32 *, 0xE8) + 1;
    func_8003521C_35E1C(&func_801F4860_61FC40);
}
