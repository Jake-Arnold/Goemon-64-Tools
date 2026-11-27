#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);
M2C_UNK func_801D88EC_60336C(void *, M2C_UNK *, void *);
M2C_UNK func_8020552C_62FFAC();
extern M2C_UNK D_80210B68_63B5E8;
extern f32 D_8021410C_63EB8C;
extern M2C_UNK func_80201104_62BB84;

void func_80201064_62BAE4(void *arg0, void *arg1) {
    M2C_FIELD(arg1, s16 *, 0x14) = 0;
    M2C_FIELD(arg1, s16 *, 0x16) = 0;
    M2C_FIELD(arg1, s16 *, 0x18) = 0;
    M2C_FIELD(arg1, f32 *, 0xC) = -135.0f;
    M2C_FIELD(arg1, f32 *, 8) = 0.0f;
    M2C_FIELD(arg1, f32 *, 0x10) = -500.0f;
    M2C_FIELD(arg0, f32 *, 0x70) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x74) = D_8021410C_63EB8C;
    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    func_801D88EC_60336C(arg0, &D_80210B68_63B5E8, arg1);
    M2C_FIELD(arg1, f32 *, 0x28) = 2.0f;
    func_8020552C_62FFAC();
    M2C_FIELD(arg0, s32 *, 0x64) |= 0x100;
    func_80034E8C_35A8C(&func_80201104_62BB84);

    *(volatile s32 *)0x80000000 = 1;
}
