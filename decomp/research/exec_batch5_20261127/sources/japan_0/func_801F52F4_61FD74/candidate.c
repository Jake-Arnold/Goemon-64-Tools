#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);
M2C_UNK func_801D88EC_60336C(void *, M2C_UNK *);
extern M2C_UNK D_80210A08_63B488;
extern f32 D_80213C60_63E6E0;
extern M2C_UNK func_801F5364_61FDE4;

void func_801F52F4_61FD74(void *arg0, void *arg1) {
    M2C_FIELD(arg1, s16 *, 0x14) = 0;
    M2C_FIELD(arg1, s16 *, 0x16) = 0;
    M2C_FIELD(arg1, s16 *, 0x18) = 0;
    M2C_FIELD(arg1, f32 *, 0xC) = -136.0f;
    M2C_FIELD(arg1, f32 *, 8) = 0.0f;
    M2C_FIELD(arg1, f32 *, 0x10) = -500.0f;
    M2C_FIELD(arg0, f32 *, 0x70) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x74) = D_80213C60_63E6E0;
    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    func_801D88EC_60336C(arg0, &D_80210A08_63B488);
    func_80034E8C_35A8C(&func_801F5364_61FDE4);
}
