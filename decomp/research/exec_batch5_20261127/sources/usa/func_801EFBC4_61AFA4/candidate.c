#include "m2c_types.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);
M2C_UNK func_801D31CC_5FE5AC(void *, M2C_UNK *);
extern M2C_UNK D_8020B2D8_6366B8;
extern f32 D_8020E530_639910;
extern M2C_UNK func_801EFC34_61B014;

void func_801EFBC4_61AFA4(void *arg0, void *arg1) {
    M2C_FIELD(arg1, s16 *, 0x14) = 0;
    M2C_FIELD(arg1, s16 *, 0x16) = 0;
    M2C_FIELD(arg1, s16 *, 0x18) = 0;
    M2C_FIELD(arg1, f32 *, 0xC) = -136.0f;
    M2C_FIELD(arg1, f32 *, 8) = 0.0f;
    M2C_FIELD(arg1, f32 *, 0x10) = -500.0f;
    M2C_FIELD(arg0, f32 *, 0x70) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x74) = D_8020E530_639910;
    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    func_801D31CC_5FE5AC(arg0, &D_8020B2D8_6366B8);
    func_8003521C_35E1C(&func_801EFC34_61B014);
}
