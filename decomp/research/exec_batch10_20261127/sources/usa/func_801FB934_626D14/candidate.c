#include "m2c_types.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);
M2C_UNK func_801D31CC_5FE5AC(void *, M2C_UNK *, void *);
M2C_UNK func_801FFDFC_62B1DC();
extern M2C_UNK D_8020B438_636818;
extern f32 D_8020E9DC_639DBC;
extern M2C_UNK func_801FB9D4_626DB4;

void func_801FB934_626D14(void *arg0, void *arg1) {
    M2C_FIELD(arg1, s16 *, 0x14) = 0;
    M2C_FIELD(arg1, s16 *, 0x16) = 0;
    M2C_FIELD(arg1, s16 *, 0x18) = 0;
    M2C_FIELD(arg1, f32 *, 0xC) = -135.0f;
    M2C_FIELD(arg1, f32 *, 8) = 0.0f;
    M2C_FIELD(arg1, f32 *, 0x10) = -500.0f;
    M2C_FIELD(arg0, f32 *, 0x70) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x74) = D_8020E9DC_639DBC;
    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    func_801D31CC_5FE5AC(arg0, &D_8020B438_636818, arg1);
    M2C_FIELD(arg1, f32 *, 0x28) = 2.0f;
    func_801FFDFC_62B1DC();
    M2C_FIELD(arg0, s32 *, 0x64) |= 0x100;
    func_8003521C_35E1C(&func_801FB9D4_626DB4);
}
