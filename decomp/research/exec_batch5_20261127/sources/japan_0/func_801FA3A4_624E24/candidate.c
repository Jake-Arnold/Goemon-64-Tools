#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);
M2C_UNK func_801D8604_603084(s32, M2C_UNK *, void *);
M2C_UNK func_801FCE00_627880();
extern M2C_UNK D_80210A00_63B480;
extern M2C_UNK func_801FA424_624EA4;

void func_801FA3A4_624E24(void *arg0, s32 arg1) {
    f32 div;

    div = 2.0f;
    func_801FCE00_627880();
    M2C_FIELD(arg0, f32 *, 0x74) = 7.0f;
    M2C_FIELD(arg0, f32 *, 0x70) = M2C_FIELD(arg0, f32 *, 0x70) / div;
    M2C_FIELD(arg0, f32 *, 0x78) = M2C_FIELD(arg0, f32 *, 0x78) / div;
    func_801D8604_603084(arg1, &D_80210A00_63B480, arg0);
    M2C_FIELD(arg0, s32 *, 0xE8) = M2C_FIELD(arg0, s32 *, 0xE8) + 1;
    func_80034E8C_35A8C(&func_801FA424_624EA4);
}
